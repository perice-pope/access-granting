# be sure to run pip install -r requirements.txt

import hashlib
import psycopg2 
import random
import os
from dotenv import load_dotenv

load_dotenv()

# Postgres connection setup  
db_host = os.environ['DB_HOST']
db_name = os.environ['DB_NAME'] 
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']

# Generate random 8-digit UMID
umid = str(random.randint(10000000,99999999))  
umid = []

def hash_umid(umid):
    return hashlib.sha256(umid.encode('utf-8')).hexdigest()

def write_hashed_umid_to_db(umid, hashed_umid):
    try:
        conn = psycopg2.connect(
            host=db_host,  
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO approved_mcl_users (umid, uuid) VALUES (%s, %s)", (umid, hashed_umid)) 
        conn.commit()
        conn.close()
    except:
        print("Error inserting into database")

hashed_umid = hash_umid(umid)
write_hashed_umid_to_db(umid, hashed_umid) 

print(f"Inserted UMID: {umid}")
print(f"Hashed UMID: {hashed_umid}")