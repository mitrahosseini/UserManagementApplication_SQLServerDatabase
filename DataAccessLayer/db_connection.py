from msilib.schema import ODBCDriver

import pyodbc
class DatabaseConnection:
    @staticmethod
    def get_connection():
        connection_string=(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=Localhost;"
            "DATABASE=UserManagement;"
            "Trusted_Connection=yes;"
            #"UID=sa;"
           # "PWD=Sadat/13196987;"
        )
        print("connection string:")
        print(connection_string)
        print("ODBC Driver:")
        print(pyodbc.drivers())
        connection=pyodbc.connect(connection_string)
        return connection
