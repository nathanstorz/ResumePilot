import os
import psycopg
from dotenv import load_dotenv
from psycopg.types.json import Jsonb

load_dotenv()


def get_connection():
    return psycopg.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )


def initialize_database():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analyses (
                    id SERIAL PRIMARY KEY,
                    match_score INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    resume_hash TEXT,
                    job_url TEXT,
                    CONSTRAINT unique_resume_job UNIQUE (resume_hash, job_url)
                )
            """)

    print("Analyses table ready!", flush=True)


def find_analysis(resume_hash, job_url):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM analyses
                WHERE resume_hash = %s
                AND job_url = %s
            """, (resume_hash, job_url))

            return cursor.fetchone()

def save_analysis(analysis, resume_hash, job_url):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO analyses (
                    match_score,
                    strengths,
                    skill_gaps,
                    relevant_experience,
                    recommendations,
                    resume_hash,
                    job_url
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                analysis.match_score,
                Jsonb(analysis.strengths),
                Jsonb(analysis.skill_gaps),
                Jsonb(analysis.relevant_experience),
                Jsonb(analysis.recommendations),
                resume_hash,
                job_url
            ))

            return cursor.fetchone()[0]

initialize_database()