import mysql.connector

def create_connection(host='localhost',user='root',password='rootuser',database='job_market'):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

def close_connection(conn):
    conn.close()

def skill_demand_summary(conn):
    sql = """
    CREATE TABLE IF NOT EXISTS skill_demand_summary as
    select 'python' as skill, sum(has_python) as job_count from jobs_clean
    UNION ALL
    SELECT 'sql', SUM(has_sql) FROM jobs_clean
    UNION ALL
    SELECT 'power_bi', SUM(has_power_bi) FROM jobs_clean
    UNION ALL
    SELECT 'tableau', SUM(has_tableau) FROM jobs_clean
    UNION ALL
    SELECT 'excel', SUM(has_excel) FROM jobs_clean
    UNION ALL
    SELECT 'aws', SUM(has_aws) FROM jobs_clean
    UNION ALL
    SELECT 'machine_learning', SUM(has_machine_learning) FROM jobs_clean
    UNION ALL
    SELECT 'statistics', SUM(has_statistics) FROM jobs_clean
    UNION ALL
    SELECT 'r', SUM(has_r) FROM jobs_clean;
    """
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS skill_demand_summary")
    cursor.execute(sql)

    conn.commit()
    cursor.close()

    print("Skill Demand Summary table built successfully!")

def salary_by_country(conn):
    sql="""
    CREATE TABLE IF NOT EXISTS salary_by_country as
    select country, round(avg(avg_salary), 2) as avg_salary, count(*) as job_count from jobs_clean where avg_salary is not null group by country
    """
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS  salary_by_country")
    cursor.execute(sql)

    conn.commit()
    cursor.close()

    print('Skill Demand Summary table built successfully!')

def hiring_trends(conn):
    sql="""
    CREATE TABLE IF NOT EXISTS hiring_trends as
    select created_date, count(*) as job_count from jobs_clean group by created_date
    """

    cursor = conn.cursor()
    cursor.execute("drop table if exists hiring_trends")
    cursor.execute(sql)

    conn.commit()
    cursor.close()

    print('Hiring Trends table built successfully!')

def monthly_trends(conn):
    sql="""
    CREATE TABLE IF NOT EXISTS monthly_trends as
    select month(created_date) as month, count(*) as job_count from jobs_clean group by month(created_date) order by month(created_date)
    """
    cursor = conn.cursor()
    cursor.execute("drop table if exists monthly_trends")
    cursor.execute(sql)

    conn.commit()
    cursor.close()

    print('Monthly Trends table built successfully!')


if __name__=="__main__":
    conn = create_connection()
    skill_demand_summary(conn)
    salary_by_country(conn)
    hiring_trends(conn)
    monthly_trends(conn)
    close_connection(conn)