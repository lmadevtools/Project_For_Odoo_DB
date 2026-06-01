from Utils import db_connector
from Utils import queries

def main():
    Connector = db_connector.DBConnector()
    Connector.connect()
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

if __name__ == "__main__":
    main()
