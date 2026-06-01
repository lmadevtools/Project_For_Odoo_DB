from Utils import db_connector
from Utils import queries

def main():
    Connector = db_connector.DBConnector()
    Connector.connect()
    #print(Connector._connection)
    print(queries.LIST_CUSTOMERS)
    Cur = Connector.execute(queries.LIST_CUSTOMERS)
    print(Cur.fetchall())

    Connector.disconnect()

if __name__ == "__main__":
    main()
