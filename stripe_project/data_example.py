import psycopg2
import os


def get_db_connection():
    conn = psycopg2.connect(host=os.environ.get('POSTGRES_HOST'),
                            database=os.environ.get('POSTGRES_DB_NAME'),
                            user=os.environ.get('POSTGRES_USER'),
                            password=os.environ.get('POSTGRES_PASSWORD'),
							port=os.environ.get('POSTGRES_PORT'))
    return conn


conn = get_db_connection()
cur = conn.cursor()
data = (
    (1, 'Cup', 'A good glass cup', 300.67),
    (2, 'Bowl', 'A good white glass bowl', 330.43),
    (3, 'Water bottle', '500 ml of clean artezian water', 150),
)
[cur.execute(f"insert into public.payment_item values('{id}', '{name}', '{desc}', '{price}') on conflict(id) do nothing;") for id, name, desc, price in data]
conn.commit()
cur.close()
conn.close()