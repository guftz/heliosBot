import sqlite3

class Database:
    def __init__(self):
        pass
       
        
    def connect(db_path: str):
        try:
            connection = sqlite3.connect(db_path)
            print("Connected to database")
            return connection
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None
        
    @staticmethod
    def insert_data(connection, table_name: str, data: dict):
        try:
            cursor = connection.cursor()

            columns = ', '.join(data.keys())
            values = ', '.join(['?'] * len(data))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

            cursor.execute(sql, tuple(data.values()))
            connection.commit()

        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    @staticmethod
    def delete_data(connection, table_name: str, condition: dict):
        try:
            cursor = connection.cursor()

            where_clause = ' AND '.join([f"{col} = ?" for col in condition.keys()])
            sql = f"DELETE FROM {table_name} WHERE {where_clause}"

            cursor.execute(sql, tuple(condition.values()))
            connection.commit()

        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")

    @staticmethod
    def select_data(connection, table_name: str, columns: list = None, condition: dict = None):
        try:
            cursor = connection.cursor()
            
            if columns and len(columns) > 0:
                columns_clause = ', '.join(columns)
            else:
                columns_clause = '*' 
            sql = f"SELECT {columns_clause} FROM {table_name}"


            if condition:
                where_clause = ' AND '.join([f"{col} = ?" for col in condition.keys()])
                sql += f" WHERE {where_clause}"
                cursor.execute(sql, tuple(condition.values()))
            else:
                cursor.execute(sql)

            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            result = [dict(zip(column_names, row)) for row in rows]
            return result

        except sqlite3.Error as e:
            print(f"Error selecting data: {e}")
            return None

    @staticmethod
    def update_data(connection, table_name: str, data: dict, condition: dict):
        if connection is None:
            print("Database connection not established.")
            return

        try:
            cursor = connection.cursor()

            # Constructing the SET clause
            set_clause = ', '.join([f"{col} = ?" for col in data.keys()])

            # Constructing the WHERE clause
            where_clause = ' AND '.join([f"{col} = ?" for col in condition.keys()])

            # Complete SQL query
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

            # Execute the UPDATE statement
            cursor.execute(sql, tuple(data.values()) + tuple(condition.values()))
            connection.commit()

        except sqlite3.Error as e:
            print(f"Error updating data: {e}")

    @staticmethod
    def insert_user_on_database(connection, user_id: int, username: str):

        
        user_check = Database.select_data(connection, "profiles", ["user_id"], {"user_id": user_id})
        
        if user_check and len(user_check) > 0:
            print(f"User is already in the database (ID: {user_check[0]['user_id']})")
        else:
            try:
                Database.insert_data(connection, "profiles", {"user_id": user_id, "username": username})
                print(f"User inserted into the database ({username})")
            except sqlite3.Error as e:
                print(f"Error inserting user into database: {e}")
                return None


            



