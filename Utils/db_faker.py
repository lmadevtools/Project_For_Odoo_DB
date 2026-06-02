from faker import Faker
from datetime import datetime
import random
from Classes import inventory

class Fake:
    def __init__(self):
        self.fake = Faker()
        self.countC = 0
        self.countP = 0
        self.countO = 0
        self.generated_ids = set()

    def generate_data(self,table_name, column_name,data_type,max_length):
        if data_type == 'uuid':
            return self.fake.uuid4()
        elif data_type == 'character varying':
            if 'email' in column_name.lower():
                value = self.fake.email()
            elif 'name' in column_name.lower():
                value = self.fake.name()
            elif 'phone' in column_name.lower():
                value = self.fake.phone_number()
            elif column_name == 'order_status':
                value = 'draft'
            elif column_name == 'direction':
                rdm = random.randint(1, 2)
                if rdm == 1:
                    value = 'in'
                else:
                    value = 'out' 
            elif column_name == 'customer_id':
                if table_name == 'customers':
                    self.countC += 1
                    return (self.countC)
                else:
                     return random.randint(1, self.countC)    
            elif column_name == 'product_id':
                if table_name == 'products':
                    self.countP += 1
                    return (self.countP)
                else:
                     return random.randint(1, self.countP)    
            elif column_name == 'order_id':
                if table_name == 'orders':
                    self.countO += 1
                    id = self.countO
                else:
                    id = random.randint(1, self.countO) 

                if len(str(id)) == 1:
                    return"CMD/2026/000" + str(id)
                else:
                    return "CMD/2026/00" + str(id)
            else:
                value = self.fake.word()
            return value[:max_length] 
        elif data_type == 'timestamp without time zone':
            return datetime.now()
        elif data_type == 'integer' or data_type == 'numeric' :
            if column_name == 'id':
                while True:
                    id = random.randint(0, 1000)
                    if id not in self.generated_ids:
                        self.generated_ids.add(id)
                        return id
            else:
                val = random.randint(0, 1000)
                return val 
        elif data_type == 'boolean':
            return True
        else:
            return None

    def insert_sample_data(self,conn, table_name, num_samples):
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT column_name, data_type, character_maximum_length FROM information_schema.columns WHERE table_name = %s", (table_name,))
            schema = cursor.fetchall()
            for _ in range(num_samples):
                data = []
                columns = []
                for column in schema:
                    column_name = column[0]
                    data_type = column[1]
                    max_length = column [2]
                    if column[1] != 'serial':
                        result = self.generate_data(table_name,column_name,data_type,max_length)
                        data.append(result)
                    placeholders = ', '.join(['%s'] * len(data))
                    columns.append(column_name)
                    
                query = f"INSERT INTO {table_name} ("
                query += ','.join(columns)
                query += f") VALUES ({placeholders})"
                try:
                    cursor.execute(query, tuple(data))
                    conn.commit()
                except Exception as e:
                    pass
                    #print(f"Error: {e}")
        finally:
            self.generated_ids = set()  #put back to 0 for next table.
            cursor.close()
            print(f"records inserted into {table_name}.")


