import logging
import sys
from flask import Flask

def setup_logger(app: Flask):
    handler = logging.StreamHandler(sys.stdout)
    
    log_level = logging.INFO
    if app.debug:
        log_level = logging.DEBUG
        
    app.logger.setLevel(log_level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    if app.logger.hasHandlers():
        app.logger.handlers.clear()
        
    app.logger.addHandler(handler)
    
    app.logger.info("Logger initialized.")
