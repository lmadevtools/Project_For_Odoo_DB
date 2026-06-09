from faker import Faker
from datetime import datetime
import random


class Fake:
    def __init__(self):
        self.fake = Faker()
        self.countC = 0
        self.countP = 0
        self.countO = 0
        self.generated_ids = set()

    def generate_data(self, table_name, column_name, data_type, max_length):
        if data_type == 'uuid':
            return self.fake.uuid4()

        elif data_type == 'character varying':
            if 'email' in column_name.lower():
                value = self.fake.email()
            elif column_name == 'customer_name':
                value = self.fake.name()
            elif column_name == 'product_name':
                value = self.fake.word().capitalize() + " " + self.fake.word().capitalize()
            elif 'phone' in column_name.lower():
                value = self.fake.phone_number()
            elif column_name == 'order_status':
                value = 'draft'
            elif column_name == 'direction':
                value = random.choice(['in', 'out'])

            elif column_name == 'customer_id':
                if table_name == 'customers':
                    self.countC += 1
                    return "C" + str(self.countC)
                else:
                    return "C" + str(random.randint(1, self.countC))

            elif column_name == 'product_id':
                if table_name == 'products':
                    self.countP += 1
                    return "P" + str(self.countP)
                else:
                    return "P" + str(random.randint(1, self.countP))

            elif column_name == 'order_id':
                if table_name == 'orders':
                    self.countO += 1
                    id = self.countO
                else:
                    id = random.randint(1, self.countO)
                return f"CMD/2026/{str(id).zfill(4)}"

            else:
                value = self.fake.word()
            return value[:max_length] if max_length else value

        elif data_type == 'timestamp without time zone':
            return datetime.now()

        elif data_type in ('integer', 'numeric'):
            if column_name in ('price', 'unit_price', 'subtotal', 'total'):
                return round(random.uniform(1.0, 500.0), 2)
            elif column_name == 'quantity':
                return random.randint(1, 100)
            elif column_name == 'minimum_stock':
                return random.randint(1, 20)
            else:
                return random.randint(1, 1000)

        elif data_type == 'boolean':
            return True

        else:
            return None

    def insert_sample_data(self, conn, table_name, num_samples):
        # Columns that are auto-managed by the DB and must be excluded from INSERT
        EXCLUDED_COLUMNS = {'id'}

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT column_name, data_type, character_maximum_length FROM information_schema.columns WHERE table_name = %s ORDER BY ordinal_position",(table_name,))
            schema = cursor.fetchall()

            for _ in range(num_samples):
                data = []
                columns = []

                for column_name, data_type, max_length in schema:
                    # Skip auto-increment columns (exposed as 'integer' by pg for serial)
                    if column_name in EXCLUDED_COLUMNS:
                        continue

                    result = self.generate_data(table_name, column_name, data_type, max_length)
                    columns.append(column_name)
                    data.append(result)

                placeholders = ', '.join(['%s'] * len(data))
                query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                #print(query)

                try:
                    cursor.execute(query, tuple(data))
                    #print(tuple(data))
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(f"[WARN] Skipped row in '{table_name}': {e}")

        finally:
            self.generated_ids = set()
            cursor.close()
            print(f"Done — records inserted into '{table_name}'.")
