import logging 
from event_enums import UserRole
import event_exceptions

class MenuHandler:

    def __init__(self, event_service, user_service):

        self.event_service = event_service
        self.user_service = user_service
        self.current_user = None 
        self.logger = logging.getLogger(__name__)
    

    def run(self):
        print("------ Welcome to Vantag Event Management System ------")
        
        while True:
            if self.current_user is None:
                should_continue = self.handle_main_menu()
                if not should_continue :
                    break 
        

            elif self.current_user.is_admin:
                should_continue = self.handle_admin_menu()
                if not should_continue:
                    break

            else:
                should_continue = self.handle_participant_menu()
                if not should_continue:
                    break

        print("------ Thanks for making use of the event management system. Enjoy your booked event(s)! ------")
    

    def handle_main_menu(self):
        print ("\n--- Welcome to the main menu of the Vantag Event Management System! ---")

        print("You can perform these following actions: \n")

        print("1. Register as a new user.")
        print("2. Login.")
        print("3. Exist.")

        user_choice = self._get_menu_choice(1,3)
        
        if user_choice == 1:
            self._register_new_user()
            return True

        elif user_choice == 2:
            self._login()
            return True
        
        else:
            return False
        
    
    def handle_participant_menu(self):
        print(f"\n === Welcome {self.current_user.name} to the participant menu of the Vantag Event Management System === ")
        print("You can perform the following actions:\n")
        
        print("1. View all events")
        print("2. View upcoming events")
        print("3. Search events")
        print("4. Join event")
        print("5. Cancel registration")
        print("6. View my registered events ")
        print("7. Logout")
        
        user_choice = self._get_menu_choice(1,7)
        
        if user_choice == 1:
            self._view_all_events()
            return True
        
        elif user_choice == 2:
            self._view_upcoming_events()
            return True
        
        elif user_choice == 3:
            self._search_events()
            return True
        
        elif user_choice == 4:
            self._join_event()
            return True
        
        elif user_choice == 5:
            self._cancel_registration()
            return True
        
        elif user_choice == 6:
            self._view_my_events()
            return True
        
        else:
            self._logout()
            return True
        
    
    def handle_admin_menu(self):
        print(f"\n === Welcome {self._current_user.name} to the Admin Menu of the Vantag Event Management System")
        print("You can perform the following actions.\n")

        print("1. Create event")
        print("2. View all events")
        print("3. Edit event")
        print("4. Cancel event")
        print("5. Delete event")
        print("6. View event participants")
        print("7. View upcoming events")
        print("8. Search events")
        print("9. Logout")

        user_choice = self._get_menu_choice(1,9)
              
        if user_choice == 1:
            self._create_event()
            return True
        
        elif user_choice == 2:
            self._view_all_events()
            return True
        
        elif user_choice == 3:
            self._edit_event()
            return True
        
        elif user_choice == 4:
            self._cancel_event_admin()
            return True

        elif user_choice == 5:
            self._delete_event()
            return True
        
        elif user_choice == 6:
            self._view_event_participants()
            return True
        
        elif user_choice == 7:
            self._view_upcoming_events()
            return True
        
        elif user_choice == 8:
            self._search_events()
            return True
        
        elif user_choice == 9:
            self._logout()
            return True
        

    def _register_new_user(self):
        print("\n === Register New User === ")

        user_name = self._get_string_input("Enter in your name: ")
        user_email = self._get_string_input("Enter in your valid email: ")
        
        print("Select your role")
        print("1. Participant")
        print("2. Admin")

        user_choice = self._get_menu_choice(1,2)
        
        user_role = None

        if user_choice == 1:
            user_role = UserRole.PARTICIPANT
        elif user_choice == 2:
            user_role = UserRole.ADMIN

        try:
            new_user = self.user_service.register_user(user_name, user_email, user_role)
            print(f"Registration successful! Welcome {new_user.name}.")
            self.current_user = new_user

        except event_exceptions.InvalidEmail as e:
            print(f"Error message: {e}")
            self.logger.error("The user entered in an invalid email format", exc_info=True)
                
        except event_exceptions.DuplicateRegistration as e:
            print(f"Error message: {e}")
            self.logger.error("The user has regsitered before.", exc_info=True)
                
        except ValueError as e:
            print(f"Invalid input: {e}")
            self.logger.error("The users entered in a wrong input", exc_info=True)
            
        except Exception as e:
            print("An unecpected error ccurred. Please try again.")
            self.logger.error(f"Unexpected error occurred {e}")


    def _login(self):
        print("\n === Login === ")
        email = self._get_string_input("Enter in your email: ") #gets the user's email

        try:
            user = self.user_service.login(email) #logs in the user

            if user is None:
                print(f"No user found with this {email} email.")
                print("Tip: Register as a new user from the main menu.")

            else:
                self.current_user = user
                print("Welcome back. Login successful!")

        except Exception as e:
            self.logger.error(f"Login error {e}")
            print("An error occurred while trying to log in. Please, try again.")

    def _logout(self):
        if self.current_user is not None:
            print(f"Goodbye {self.current_user.name}!")

            self.current_user = None
            print("You have succesfull logged out.")

    def _view_all_events(self):
        print("\n === All events === ")

        try:
            events = self.even
            
           
