import psycopg
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

BERLIN = ZoneInfo("Europe/Berlin")
GYM_URL = os.getenv("GYM_URL")
DB_CONFIG = dict(
    host=os.getenv("HOST"),
    port=os.getenv("PORT"),
    dbname=os.getenv("DBNAME"),
    user=os.getenv("DBUSER"),
    password=os.getenv("DBPASSWORD"),
)
gym_ids = [1, 7, 11, 12, 13, 20, 21, 23, 24, 33, 34, 37, 38]


def get_data(gym_id: int) -> dict:
    url = f"{GYM_URL}&stud_nr={gym_id}&jsonResponse=1"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.json()


SQL_INSERT_IF_CHANGED = """
INSERT INTO data (gym_id, workload, recorded_at)
SELECT %s, %s, %s
WHERE %s IS DISTINCT FROM (
  SELECT workload
  FROM data
  WHERE gym_id = %s
  ORDER BY recorded_at DESC
  LIMIT 1
);
"""


def main():
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:

            cur.execute("SET TIME ZONE 'Europe/Berlin';")
            recorded_at = datetime.now(BERLIN)
            for gym_id in gym_ids:
                data = get_data(gym_id)

                workload_new = Decimal(str(data["numval"]))

                # insert nur wenn geändert (oder noch kein Eintrag)
                cur.execute(
                    SQL_INSERT_IF_CHANGED,
                    (gym_id, workload_new, recorded_at, workload_new, gym_id),
                )


if __name__ == "__main__":
    main()
