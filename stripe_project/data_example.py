import psycopg2
import os


# Данный файл необходим для заполнения БД данными для демострации работы


def get_db_connection():
    conn = psycopg2.connect(host=os.environ.get('POSTGRES_HOST'),
                            database=os.environ.get('POSTGRES_DB_NAME'),
                            user=os.environ.get('POSTGRES_USER'),
                            password=os.environ.get('POSTGRES_PASSWORD'),
                            port=os.environ.get('POSTGRES_PORT'))
    return conn


conn = get_db_connection()
cur = conn.cursor()
data_item = (
    (1, 'Cup', 'A good glass cup', 300.67),
    (2, 'Bowl', 'A good white glass bowl', 330.43),
    (3, 'Water bottle', '500 ml of clean artezian water', 150),
)
data_coupon = (
    # Валидный купон
    (1, '5poff', '2022-11-26 15:00:00', '2023-11-26 15:00:00', 5, True),
    # Неактивный купон
    (2, '100percentoff', '2022-11-26 15:00:00', '2023-11-26 15:00:00', 100, False),
    # Просроченный купон
    (3, '10off', '2022-11-26 15:00:00', '2022-11-26 19:00:00', 5, True),
)
[cur.execute(f"insert into public.payment_item values('{id}', '{name}', '{desc}', '{price}') on conflict(id) do nothing;") for id, name, desc, price in data_item]
[cur.execute(f"insert into public.coupon_coupon values('{id}', '{code}', '{vfrom}', '{vto}', '{discount}', '{active}') on conflict(id) do nothing;") for id, code, vfrom, vto, discount, active in data_coupon]
conn.commit()
cur.close()
conn.close()
