import logging
import functools

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename='info.log'
)
logger = logging.getLogger("hotelassistant")



def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log start of function
        func_name = func.__name__
        logger.info(f"Starting function: {func_name}")
        
        # Execute the function
        result = func(*args, **kwargs)
        
        # Log end of function
        logger.info(f"Ending function: {func_name}")
        
        return result
    return wrapper

