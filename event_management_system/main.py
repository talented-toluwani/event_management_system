import sys
import logging
from event_database import get_connection, init_database
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
    logger.info("Application logging initialized")
    