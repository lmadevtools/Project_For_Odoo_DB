from Utils import db_connector
from Utils import queries
from Utils import db_faker

def main():
    Connector = db_connector.DBConnector()
    Connector.connect()

    fk = db_faker.Fake()

    fk.insert_sample_data(Connector._connection, 'products', 10)
    Connector.commit()
    fk.insert_sample_data(Connector._connection, 'customers', 10)  
    Connector.commit()
    fk.insert_sample_data(Connector._connection, 'orders', 10)
    Connector.commit()
    fk.insert_sample_data(Connector._connection, 'order_lines', 10)
    Connector.commit()
    fk.insert_sample_data(Connector._connection, 'stock_moves', 10)
    Connector.commit()

    Connector.disconnect()

'''   
    #print(Connector._connection)
    print(queries.LIST_CUSTOMERS)
    Cur = Connector.execute(queries.LIST_CUSTOMERS)
    print(Cur.fetchall())
    print()

    print('ADD PROD OK')
    print(queries.CREATE_PRODUCT)
    try:
        Cur = Connector.execute(queries.CREATE_PRODUCT,(3, 'name_prod', "5", "10", "3", "General", True))
    except Exception as e:
        print(f"Error: {e}")
    else:
        Connector.commit()
        Cur = Connector.execute(queries.LIST_PRODUCTS)
        print(Cur.fetchall())
    print()

    print('ADD PROD NOK')
    try:
        Cur = Connector.execute(queries.CREATE_PRODUCT,(1, 'name_prod', "5", "10", "3", "General", True))
    except Exception as e:
        print(f"Error: {e}")
    else:
        Connector.commit()
        Cur = Connector.execute(queries.LIST_PRODUCTS)
        print(Cur.fetchall())

    Connector.disconnect()
'''

if __name__ == "__main__":
    main()
