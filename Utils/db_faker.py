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
			if 'email' in column_name.lower():
				value = self.fake.email()
			elif 'name' in column_name.lower():
				value = self.fake.name()
			elif 'phone' in column_name.lower():
				value = self.fake.phone_number()
			else
				value = self.fake.word()
			return value[:max_length] 
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
        cursor.execute("SELECT column_name, data_type, char_max_length FROM information_schema.columns WHERE table_name = %s", (table_name,))
        schema = cursor.fetchall()
        for _ in range(num_samples):
            data = []
            columns = []
            for column in schema:
				column_name = column[0]
				data_type = column[1]
				max_length = column [2]
                if column[1] != 'serial':
                    data.append(self.generate_data(column_name,data_type,max_length))
                placeholders = ', '.join(['%s'] * len(data))
                columns = ', '.join(columns)
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
                cursor.execute(query, tuple(data))
            conn.commit()
            cursor.close()
            print(f"Inserted {num_samples} records into {table_name}.")


