create table IF NOT EXISTS jobs_raw(
    id int auto_increment primary key,
    job_id varchar(64) unique,
    job_title TEXT,
    job_description LONGTEXT,
    company TEXT,
    job_location text,
    country varchar(50),
    city varchar(50),
    min_salary float,
    max_salary float,
    created DATETIME,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    job_url TEXT,
    source VARCHAR(50) 
)