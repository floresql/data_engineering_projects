from dotenv import load_dotenv
load_dotenv()

from databricks import sql
import os

with sql.connect(
    server_hostname=os.environ["DATABRICKS_HOST"],
    http_path=os.environ["DATABRICKS_HTTP_PATH"],
    access_token=os.environ["DATABRICKS_TOKEN"],
) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT current_catalog(), current_schema()")
        print(cur.fetchall())