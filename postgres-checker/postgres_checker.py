"""
Helpscript to verify if postgres us alive
"""
import psycopg2, time
POSTGRES_HOST="postgres"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"

def _is_db_ready():
    try:
        conn = psycopg2.connect("host={} user={} password={}".format(POSTGRES_HOST, POSTGRES_USER, POSTGRES_PASSWORD))
        conn.close()
        return True

    except psycopg2.OperationalError as ex:
        print("Connection failed: {0}".format(ex))
        return False

if __name__ == '__main__':
    max_attempts = 40
    attempts = 0
    while not _is_db_ready() or attempts > max_attempts:
        print("db not ready, waiting..")
        attempts += 1
        time.sleep(10)

    if attempts > max_attempts:
        raise Exception("db not ready giving up")