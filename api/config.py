import os

def database(**kwargs):
    return {
        'host' : "iteam-s.mg",
        'user' : os.environ['ITEAMS_DB_USER'],
        'password': os.environ['ITEAMS_DB_PASS'],
        'database': 'LOGAS',
        'charset': 'utf8mb4'
    }