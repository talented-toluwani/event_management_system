#import logging
import event_exceptions
import re
from event_enums import UserRole
from event_models import User
class UserService:
    def __init__(self, user_repository, registration_repository, event_repository):
        self.user_repository = user_repository
        self.registration_repository = registration_repository
        self.event_repository = event_repository

    
    def register_user(self, name:str, email:str, role:str):

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name cannot be empty.")
        
        if len(name) < 2 or len(name) > 50:
            raise ValueError("The length of the name must be between 2 and 50 characters.")
        
        if role is not UserRole.PARTICIPANT:
            raise PermissionError("Note, you must have the role of a participant, before you can register")
        
        email_regex = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
    
        if not re.fullmatch(email_regex, email.strip().lower()):
            raise ValueError(f"'{email}' is not a valid email format.")
        
        existing_user = self.user_repository.get_by_email(email)

        if existing_user is not None:
            raise event_exceptions.DuplicateRegistration()
        
        new_user = User(
            user_id = None,
            name = name.strip(),
            email = email.strip().lower(),
            role = role
        )

        created_user = self.user_repository.create(new_user)
        return created_user
        
    
    def login(self, email:str):

        existing_user = self.user_repository.get_by_email(email)
        if existing_user is not None:
            return existing_user
        
        return None
    

    def get_user(self, user_id:int):

        existing_user = self.user_repository.get_by_id(user_id)
        if existing_user is not None:
            return existing_user
        
        raise event_exceptions.UserNotFound(user_id)
    
    def get_user_events(self, user_id:int):

        self.get_user(user_id) #fetches the user
        
        event_ids = self.registration_repository.get_user_events(user_id)#fetches users events
        event_object_list = []
        
        for event_id in event_ids:
            event_object = self.event_repository.get_by_id(event_id)
            event_object_list.append(event_object)
        return event_object_list


        

         
        

        
        
