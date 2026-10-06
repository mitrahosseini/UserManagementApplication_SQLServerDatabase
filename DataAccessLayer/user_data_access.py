from DataAccessLayer.db_connection import DatabaseConnection
from Common.Entities.user import User
from Common.Model.response import Response
from  Common.Entities.role import Role
class UserDataAccess:
    def get_user(self, username, hash_password):
            connection = DatabaseConnection.get_connection()
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT id,
                   first_name,
                   last_name,
                   username,
                   status,
                   role
            FROM [User]
            Where username='{username}'
            AND password ='{hash_password}'""")
            data = cursor.fetchone()
            if data:
                return User(data[0], data[1], data[2], data[3], None,data[4],data[5])
    # def search_user(self, username):
    #     with sqlite3.connect(sqlite_database_name) as connection:
    #         cursor = connection.cursor()
    #         cursor.execute(f"""
    #         SELECT id,
    #                first_name,
    #                last_name,
    #                username,
    #                status,
    #                role
    #         FROM User
    #         Where username='{username}'""")
    #         data = cursor.fetchone()
    #         if data:
    #             return User(data[0], data[1], data[2], data[3], None,data[4],data[5])


    def insert_user(self, first_name,last_name,username,hash_password,status,role):
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()
        try:
                cursor.execute(f"""
                    INSERT INTO [User] (
                              first_name,
                              last_name,
                              username,
                              password,
                              status,
                              role
                              )
                    VALUES (
                             '{first_name}',
                             '{last_name}',
                             '{username}',
                             '{hash_password}',
                              {status},
                              {role}
                            );""")
                connection.commit()
        except Exception as ex:
            connection.rollback()
            raise ex
        finally:
            connection.close()

    # def get_user_list(self):
    #     user_list=[]
    #     with sqlite3.connect(sqlite_database_name) as connection:
    #         cursor=connection.cursor()
    #         cursor.execute(f"""
    #         SELECT id,
    #                first_name,
    #                last_name,
    #                username,
    #                status,
    #                role
    #           FROM User
    #           Where role != 1 """)
    #         data_list=cursor.fetchall()
    #         for data in data_list:
    #             user=User(data[0],data[1],data[2],data[3],None,data[4],data[5])
    #             user_list.append(user)
    #         return user_list

    def update_status(self,user_id,new_status):
            connection = DatabaseConnection.get_connection()
            cursor=connection.cursor()
            cursor.execute(f"""
            UPDATE [User]
               SET status = {new_status}
             WHERE id ={user_id};""")
            connection.commit()

    def update_role(self,user_id,new_role_id):
            connection = DatabaseConnection.get_connection()
            cursor=connection.cursor()
            cursor.execute(f"""
              UPDATE [User]
               SET 
                   role = {new_role_id}
             WHERE id ={user_id};""")
            connection.commit()

    def get_role_list(self):
            role_list = []
            connection = DatabaseConnection.get_connection()
            cursor = connection.cursor()
            cursor.execute(f"""
            SELECT id,
                   title
            FROM   [Role]""")
            data_list = cursor.fetchall()

            for data in data_list:
                role = Role(data[0], data[1])
                role_list.append(role)

            return role_list


    def search_list(self,term):
            user_list=[]
            connection = DatabaseConnection.get_connection()
            cursor=connection.cursor()
            cursor.execute(f"""
            SELECT id,
                   first_name,
                   last_name,
                   username,
                   status,
                   role
              FROM [User]
              Where first_name LIKE '%{term}%'
                OR  last_name  LIKE  '%{term}%'
                OR  username   LIKE  '%{term}%'""")
            data_list=cursor.fetchall()
            for data in data_list:
                user=User(data[0],data[1],data[2],data[3],None,data[4],data[5])
                user_list.append(user)
            return user_list

    def get_total_user_count(self):
        try:
                connection = DatabaseConnection.get_connection()
                cursor = connection.cursor()
                cursor.execute(f"""
                   SELECT COUNT(*)
                     FROM [User]""")
                total_users = cursor.fetchone()[0]
                return  total_users
        except Exception as ex:
            return 0

    def   get_paginated_users(self,current_user_id,limit,offset):
            user_list=[]
            connection = DatabaseConnection.get_connection()
            cursor = connection.cursor()
            try:
                    cursor.execute(f"""
                        SELECT id,
                               first_name,
                               last_name,
                               username,
                               status,
                               role
                          FROM [User]
                          WHERE id != ?
                          ORDER BY id
                          OFFSET ? ROWS
                          FETCH NEXT ? ROWS ONLY
                    """,(current_user_id,offset,limit))
                    data_list = cursor.fetchall()
                    for data in data_list:
                        user = User(data[0], data[1], data[2], data[3], None, data[4], data[5])
                        user_list.append(user)
                    return user_list
            finally:
                connection.close()

