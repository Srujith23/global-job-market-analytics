from scraper import adzuna
import mysql.connector
from datetime import datetime



def create_database():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='rootuser'
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS job_market")
    cursor.close()
    conn.close()



def execute_schema():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='rootuser',
        database='job_market'
    )
    cursor = conn.cursor()

    with open("database/schema.sql", "r") as f:
        sql_commands = f.read()

    for command in sql_commands.split(";"):
        if command.strip():
            cursor.execute(command)

    conn.commit()
    cursor.close()
    conn.close()




def insert_sql(jobs, cursor, country):
    sql = """
    INSERT IGNORE INTO jobs_raw
    (job_id, job_title, job_description, company, job_location, country, city,
    min_salary, max_salary, created, job_url, source)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    for job in jobs:
        created = datetime.fromisoformat(
            job['created'].replace("Z", "")
        ).strftime("%Y-%m-%d %H:%M:%S")
        values = (
            job['id'],
            job['title'],
            job['description'],
            job.get('company', {}).get('display_name'),
            job.get('location', {}).get('display_name'),
            country,
            job['location']['area'][-1],
            job.get('salary_min'),
            job.get('salary_max'),
            created,
            job['redirect_url'],
            "adzuna"
        )
        cursor.execute(sql,values)

def run_pipelines(countries,maxpages):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password = 'rootuser',
        database='job_market'

    )
    cursor = conn.cursor()
    
    for country in countries:
        for page in range(1, maxpages+1):
            print(f"Fetching page {page}")
            data = adzuna.fetch_jobs(country,page)
            jobs = data['results']
            insert_sql(jobs, cursor, country)
    conn.commit()
    cursor.close()
    conn.close()
    
if __name__=='__main__':
    create_database()
    execute_schema()
    countries = ['gb','us','de','ca','au','in']
    run_pipelines(countries, maxpages=10)