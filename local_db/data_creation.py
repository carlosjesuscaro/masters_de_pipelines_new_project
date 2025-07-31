# data_creation.py
import os
import mysql.connector
from faker import Faker
import random
from datetime import date, timedelta

print("Python data population script started.")

# --- Configuration ---
# Database connection details are pulled from environment variables
# 'db' is the hostname for the MySQL service within the Docker Compose network
DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'db'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

NUM_USERS = 300
NUM_COMPANIES = 200
NUM_JOB_APPLICATIONS = 500

# Initialize Faker for generating fake data
fake = Faker()


# --- Database Connection Function ---
def get_db_connection():
    """
    Establishes and returns a database connection.
    Includes a retry mechanism for robustness, useful when services start up.
    """
    print(f"Attempting to connect to MySQL at {DB_CONFIG['host']}/{DB_CONFIG['database']} as {DB_CONFIG['user']}...")
    retries = 10
    delay = 5  # seconds

    for i in range(retries):
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            if conn.is_connected():
                print("Successfully connected to the database!")
                return conn
        except mysql.connector.Error as err:
            print(f"Connection attempt {i + 1}/{retries} failed: {err}")
            if i < retries - 1:
                print(f"Retrying in {delay} seconds...")
                import time
                time.sleep(delay)
    raise Exception("Could not connect to the database after multiple attempts. Is the 'db' service healthy?")


# --- Data Population Functions ---

def populate_users(cursor, num_records):
    """Inserts fake user data into the Users table."""
    print(f"Populating {num_records} users...")
    users_data = []
    for _ in range(num_records):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        password_hash = fake.md5()  # In a real app, use proper hashing like bcrypt
        country = fake.country()
        # Generate dates within a reasonable range (e.g., last 5 years)
        registration_date = fake.date_between(start_date='-5y', end_date='today')
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65)
        nationality = fake.country()  # Can be different from country of residence

        users_data.append(
            (first_name, last_name, email, password_hash, country, registration_date, birth_date, nationality))

    sql = """
          INSERT INTO Users (first_name, last_name, email, password_hash, country, registration_date, birth_date, \
                             nationality)
          VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
          """
    cursor.executemany(sql, users_data)
    print(f"Successfully inserted {cursor.rowcount} users.")


def populate_companies(cursor, num_records):
    """Inserts fake company data into the Companies table."""
    print(f"Populating {num_records} companies...")
    companies_data = []
    for _ in range(num_records):
        company_name = fake.unique.company()  # Ensure uniqueness for the UNIQUE constraint
        # Truncate if too long for VARCHAR(50)
        company_name = company_name[:50]
        industry = fake.job()  # Using 'job' as a proxy for industry, also truncate
        industry = industry[:50]
        website = fake.url()
        description = fake.text(max_nb_chars=200)

        companies_data.append((company_name, industry, website, description))

    sql = """
          INSERT INTO Companies (company_name, industry, website, description)
          VALUES (%s, %s, %s, %s) \
          """
    cursor.executemany(sql, companies_data)
    print(f"Successfully inserted {cursor.rowcount} companies.")


def populate_job_applications(cursor, num_records):
    """
    Inserts fake job application data into the JobApplications table.
    Requires existing user_ids and company_ids.
    """
    print(f"Populating {num_records} job applications...")

    # Fetch existing user_ids and company_ids
    cursor.execute("SELECT user_id FROM Users")
    user_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT company_id FROM Companies")
    company_ids = [row[0] for row in cursor.fetchall()]

    if not user_ids:
        print("No users found to create job applications for. Skipping job application population.")
        return
    if not company_ids:
        print("No companies found to create job applications for. Skipping job application population.")
        return

    job_applications_data = []
    for _ in range(num_records):
        user_id = random.choice(user_ids)
        company_id = random.choice(company_ids)
        # Note: In your current schema, JobApplications only has user_id and company_id.
        # If you add more fields like job_title, application_date, status etc., add them here.

        job_applications_data.append((user_id, company_id))

    sql = """
          INSERT INTO JobApplications (user_id, company_id)
          VALUES (%s, %s) \
          """
    cursor.executemany(sql, job_applications_data)
    print(f"Successfully inserted {cursor.rowcount} job applications.")


# --- Main Execution Block ---
if __name__ == "__main__":
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute population functions
        populate_users(cursor, NUM_USERS)
        populate_companies(cursor, NUM_COMPANIES)
        populate_job_applications(cursor, NUM_JOB_APPLICATIONS)

        conn.commit()  # Commit all changes to the database
        print("All data population complete and committed successfully!")

    except Exception as e:
        print(f"\nAn error occurred during data population: {e}")
        if conn:
            conn.rollback()  # Rollback changes if an error occurs
            print("Database transaction rolled back.")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")

print("Python script finished.")