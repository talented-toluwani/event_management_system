from event_models import User 
import logging 
import event_exceptions as event_exceptions

class UserRepository:
    def __init__(self,connection):
        self.connection = connection #initializes a connection , later used by other methods in this class

    def create(self, user:User):
        cursor = None
        try:
           database = ( """INSERT into users_table (name, email, role) VALUES (?,?,?)""")

           data = (user.name,
                user.email,
                user.role
        )#this is are labels or cagtegory, they don't store values, so uppercase
           
           cursor = self.connection.cursor()
           cursor.execute(database, data)

           new_id = cursor.lastrowid
           self.connection.commit()
           user.user_id = new_id #gets the user id

        except Exception:
           self.connection.rollback()
           logging.error("Unexpected database error", exc_info= True)
           raise

        finally:
            if cursor is not None:
                cursor.close()

    def _row_to_user(self, row): #converts databse row to user object
        return User(
        user_id = row[0],
        name= row[1],
        email = row[2],
        role = row[3]
        )
        
    def get_by_id(self, user_id):
        cursor = None
        try:
            cursor = self.connection.cursor()
            sql_query = "SELECT * from users_table WHERE user_id = ?"
            cursor.execute(sql_query, (user_id,))
            row = cursor.fetchone()

            if row is not None:
                return self._row_to_user(row)
                
            else:
                raise event_exceptions.UserNotFound(user_id)

        except Exception:
           logging.error("Unexpected database error", exc_info=True)
           raise

        finally:
            if cursor is not None:
                cursor.close()

    def get_by_email(self, email):
        cursor = None

        if "@" not in email or "." not in email:
            raise event_exceptions.InvalidEmail(email)
        
        try:
            cursor = self.connection.cursor() 
            sql_query = "SELECT * from users_table WHERE email = ?"
            cursor.execute(sql_query, (email,))
            row = cursor.fetchone()

            if row is not None:
               return self._row_to_user(row)
                
            else:
                raise event_exceptions.UserNotFound(email)
        
        except Exception: 
            logging.error("Unexpected database error", exc_info=True)
            raise

        finally:
            if cursor is not None:
                cursor.close()

    def get_all(self):
        cursor = None
        try:
            cursor =  self.connection.cursor() 
            sql_query = "SELECT * from users_table ORDER by user_id"
            cursor.execute(sql_query)

            rows = cursor.fetchall()
            user_list = []
            for row in rows:
                user_object = self._row_to_user(row)
                user_list.append(user_object)
            return user_list
            
        except Exception:
            logging.error("Unexpected database error", exc_info= True)
            raise

        finally:
            if cursor is not None:
                cursor.close()
                 
