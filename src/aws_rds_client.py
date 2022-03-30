import json
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
#  Client


class Client:
    # Create a global psql connection object
    def __init__(self, user, password, database, host):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        global connection
        connection = psycopg2.connect(user=self.user,
                                      password=self.password,
                                      database=self.database,
                                      host=self.host)

    def __repr__(self):
        return "User {0} connected to {1}.".format(self.user, self.database)

    @classmethod
    # Easy login with json
    def from_json(cls, file_path):
        with open(file_path, mode="r") as json_file:
            # Store credentials to the global namespace
            global credentials
            credentials = json.load(json_file)
        # Use credentials to log in
        return cls(credentials["user"],
                   credentials["password"],
                   credentials["database"],
                   credentials["host"])


class Load:
    @classmethod
    # One-step create table from csv to pandas df
    def create_and_load(cls, data, tablename):
        try:
            # Create sqlalchemy engine for pandas df.to_sql function
            engine = create_engine('postgresql+psycopg2://{0}:{1}@{2}/{3}'
                                   .format(credentials["user"],
                                           credentials["password"],
                                           credentials["host"],
                                           credentials["database"]
                                           )
                                   )
        except Exception as ex:
            print('Exception:')
            print(ex)
        try:
            # Read csv and do not include index column
            df = pd.read_csv(data, index_col=False)
            # Do not store into postgres with an index column
            df.to_sql("{0}".format(tablename), con=engine, index=False)
            print("Created table: {0}".format(tablename))
        except Exception as ex:
            print('Exception:')
            print(ex)
        connection.commit()

    @classmethod
    # One-step create table from pandas df
    def create_and_load_pd(cls, data, tablename):
        try:
            # Create sqlalchemy engine for pandas df.to_sql function
            engine = create_engine('postgresql+psycopg2://{0}:{1}@{2}/{3}'
                                   .format(credentials["user"],
                                           credentials["password"],
                                           credentials["host"],
                                           credentials["database"]
                                           )
                                   )
        except Exception as ex:
            print('Exception:')
            print(ex)
        try:
            # Do not store into postgres with an index column
            data.to_sql("{0}".format(tablename), con=engine, index=False, if_exists='replace')
            print("Created table: {0}".format(tablename))
        except Exception as ex:
            print('Exception:')
            print(ex)
        connection.commit()

    @classmethod
    # One-step drop table
    def drop(cls, table):
        cursor = connection.cursor()
        cursor.execute("""
        DROP TABLE IF EXISTS {0}  
        """.format(table)
        )
        connection.commit()
        cursor.close()
        print("Dropped table: {0}".format(table))


class Query:
    @classmethod
    # Retrieve column names in given table
    def get_columns(cls, table):
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM {0} LIMIT 0    
        """.format(table)
        )
        colnames = [desc[0] for desc in cursor.description]
        cursor.close()
        return(colnames)

    @classmethod
    # Return subset of table
    def get_sample(cls, table, num_records):
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM {0} LIMIT {1}    
        """.format(table, num_records)
        )
        result = cursor.fetchall()
        cursor.close()
        columns = Query.get_columns(table)
        df = pd.DataFrame(result, columns=columns)
        return(df)

    @classmethod
    # Get all records
    def fetchall(cls, table):
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM {0}
        """.format(table))
        result = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        cursor.close()
        df = pd.DataFrame(result, columns=colnames)
        return(df)

    @classmethod
    # Basic query
    def query(cls, query):
        cursor = connection.cursor()
        cursor.execute("""{0}""".format(query))
        result = cursor.fetchall()
        colnames = [desc[0] for desc in cursor.description]
        cursor.close()
        df = pd.DataFrame(result, columns=colnames)
        return(df)


class Meta:
    @classmethod
    # See all tables in DB instance
    def get_tables(cls):
        cursor = connection.cursor()
        cursor.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public'
        """)
        result = cursor.fetchall()
        cursor.close()
        if len(result) < 1:
            result = "There are no tables in this database"
        return(result)
