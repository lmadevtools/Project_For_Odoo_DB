from faker import Faker
from datetime import datetime
import random

class Fake:
    def __init__(self):
        self.fake = Faker()
        self.generated_ids = set()


    def generate_data(self,data_type):
        if data_type == 'uuid':
            return self.fake.uuid4()
        elif data_type == 'character varying':
            return self.fake.name() if 'name' in data_type else self.fake.email()
        elif data_type == 'timestamp without time zone':
            return datetime.now()
        elif data_type == 'integer':
            while True:
                id = random.randint(1, 10000)
                if id not in self.generated_ids:
                    self.generated_ids.add(id)
                    return id
        else:
            return None

    def insert_sample_data(self,conn, table_name, num_samples):
        cursor = conn.cursor()
        cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s", (table_name,))
        schema = cursor.fetchall()
        for _ in range(num_samples):
            data = []
            columns = []
            for column in schema:
                if column[1] != 'serial':
                    data.append(self.generate_data(column[1]))
                    columns.append(column[0])
                placeholders = ', '.join(['%s'] * len(data))
                columns = ', '.join(columns)
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                cursor.execute(query, tuple(data))
            conn.commit()
            cursor.close()
            print(f"Inserted {num_samples} records into {table_name}.")


