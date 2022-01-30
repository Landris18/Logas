import os
from dotenv import load_dotenv

load_dotenv() 


def database(**kwargs):
    return {
        'host' : 'iteam-s.mg',
        'user' : os.environ['ITEAMS_DB_USER'],
        'password': os.environ['ITEAMS_DB_PASS'],
        'database': 'LOGAS'
    }
