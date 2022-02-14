"""
Program Name:        logger.py
Date:                06/09/2020
History:             Original Copy
                     ---
                     v2.0 - Modernized and adapted from NOAA logger creation lib
Author:              Perry Bunn
Email:               perry@auburn.edu
Created:             06/09/2020
Last Modified:       2022-02-13
Description:         This file contains Python functions for setting up logging
"""
import datetime
import logging
import sys

from logging import Logger
from pathlib import Path
from typing import Union


def logging_function(program_name: str, log_directory: Union[str, Path],
                     logging_level: str, run_time: datetime) -> Logger:
    """
    Parameters
    ----------
    program_name: str
    log_directory: str, Path
    logging_level: str
        either "INFO", "DEBUG", "WARNING", "ERROR" or the equivalent Python
        logging.log_level object
    run_time: datetime

    Returns
    -------
    Logger - Root level logging object
    """
    log_directory = Path(log_directory)
    if not log_directory.exists():
        print(f"ERROR: Log directory {log_directory.name} not found")
        print("       check that LOGS_DIR is set correctly in config file")
        sys.exit(1)

    current_datestring = datetime.datetime.strftime(run_time, "%Y%m%d")
    current_timestring = datetime.datetime.strftime(run_time, "%H%M%S")

    log_date_dir = log_directory / f"{current_datestring}"
    log_date_dir.mkdir(exist_ok=True)
    log_file = f"{log_date_dir.as_posix()}/{program_name}_{current_timestring}.log"
    return _get_logger(log_file, logging_level)


def _get_logger(log_file: Union[str, Path], log_level: str="INFO") -> Logger:
    """
    Sets up and returns a root logger with standard
    formatting and handlers

    Parameters
    ----------
    log_file: str, Path
    log_level: str
        either "INFO", "DEBUG", "WARNING", "ERROR" or the equivalent Python
        logging.log_level object

    Returns
    -------
    Logger - Root level logging object
    """
    # set the name of the logger being used
    logger = logging.getLogger()
    # logger = logging.getLogger(name)
    logger.setLevel(log_level)
    # defines how the header information of a log event will appear
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # define handler used to output text to log file
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # add the file handler to the logging object
    logger.addHandler(file_handler)
    # add the stream handler to the logging object
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)
    logger.addHandler(stream_handler)
    return logger
