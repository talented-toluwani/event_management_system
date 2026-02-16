from dataclasses import dataclass
from datetime import datetime
from event_enums import UserRole

@dataclass
class Event:
    event_id:str # an integer, string or a combination of both of them is expected
    title: str # a sting is expected
    description: str #a string is expected
    date_time: datetime # both the date, and time are expected
    max_capacity: int # an integer is ecpected
    category: str # a sting is expected
    current_participants: int # an integer is ecpected
    status: str # a sting is expected

    @property
    def is_full(self) -> bool: #checks if the number of participant is more than the maxium capacity required, and returns the complementary boolean answer
            return self.current_participants >= self.max_capacity
    
    @property
    def available_spots(self) -> int: #checks the number of available spots left
        return self.max_capacity - self.current_participants
    
    @property
    def is_upcoming(self):
         return self.date_time > datetime.now()
    
@dataclass
class User:
     user_id = "user_id"
     name = "name"
     email = "email"
     role = "role"

     @property
     def is_admin(self) -> bool:
          return self.role == UserRole.ADMIN
