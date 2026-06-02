from Utils import db_connector
from Utils import queries
from Utils import db_faker

def main():
    Connector = db_connector.DBConnector()
    Connector.connect()

    try:
        with open("Sql/drop_db.sql", "r") as file:
            sql_query = file.read()
            Connector.execute(sql_query)
            Connector.commit()
            "tables deleted"
    except Exception as e:
            print(f"Error: {e}") 
    finally:
        try:
            with open("Sql/init_db.sql", "r") as file:
                sql_query = file.read()
                Connector.execute(sql_query)
                Connector.commit()
                "table created"
        except Exception as e:
                print(f"Error: {e}") 
    
    fk = db_faker.Fake()
    try:
        fk.insert_sample_data(Connector._connection, 'products', 10)   
        fk.insert_sample_data(Connector._connection, 'customers', 10)   
        fk.insert_sample_data(Connector._connection, 'orders', 10)   
        fk.insert_sample_data(Connector._connection, 'order_lines', 10)   
        fk.insert_sample_data(Connector._connection, 'stock_moves', 10)  
    finally:
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
        Cur = Connector.execute(queries.CREATE_PRODUCT,(1, 'name_prod', "5", "10", "3", "General", True))
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
