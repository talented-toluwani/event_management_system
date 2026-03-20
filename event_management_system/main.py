import sys
import logging
from event_database import init_database, get_connection
import event_config
from event_repository import EventRepository
from user_repository import UserRepository
from registration_repository import RegistrationRepository
from event_service import EventService
from user_service import UserService
import menu_handler


def setup_logging():
    logging.basicConfig(
        level=getattr(logging, event_config.LOG_LEVEL),
        format= event_config.LOG_FORMAT
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Application logging initialized.")


def initialize_database():
    logger = logging.getLogger(__name__)
    logger.info("Initializing database.")
    init_database()
    logger.info("Database initialized successfully.")


def create_repositories(connection):
    logger = logging.getLogger(__name__)
    logger.info("Creating repository instances.")
    
    user_repository = UserRepository(connection)
    event_repository = EventRepository(connection)
    registration_repository = RegistrationRepository(connection)

    logger.info("Repository instances created successfully.")

    return(user_repository, event_repository, registration_repository)

def create_services(user_repository, event_repository, registration_repository):
    logger = logging.getLogger(__name__)
    logger.info("Creating services instance,")

    user_service = UserService(user_repository)
    event_service = EventService(event_repository, registration_repository)

    logger.info("Services instance successfully created.")
    return(user_service, event_service)
    

def main():