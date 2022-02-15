#!/bin/python3
"""
    Title:          Hex Dump
    Version:        v1.0
    Author:         Perry Bunn
    Discussions-To: perry@auburn.edu
    Status:         Development
    Created:        2022-02-13
    Last Modified:  2022-02-13
    Description:    This script will dump the contents of a DINAP save file and
                    try to display the contents in a human readable format.
"""
from argparse import ArgumentParser
from pathlib import Path

import datetime
import os
import yaml

from lib import namespace
from lib.logger import logging_function


def dump(file: Path):
    pass


def driver(config, logger, save: Path=None):
    if save:
        dump(save)
        return
    save_dir = Path(config["SAVE_DIR"])
    os.chdir(save_dir.as_posix())
    save_subdirs = [x for x in save_dir.iterdir() if x.is_dir()]
    if len(save_dir) > 1:
        logger.debug(f"Multiple save profiles found: {save_subdirs}")
        profile = input("Which profile do you want dump a save from? ")
        os.chdir(Path(profile.strip()))
    else:
        os.chdir(save_subdirs[0])


def main(arg: namespace, save: str):
    """
        Flow:
        1. Navigate to save location and read user profile
        2. Search for saves, prompt user which save to dump
        3. Read selected save file
            a. For each row of the file display: Address, raw, dump; versions of
               the data.
            b. Display the resources in a table for easy viewing.
    """
    config_file = arg.config
    with open(config_file, 'r', encoding="utf-8") as file:
        config = yaml.safe_load(file)
    logger = logging_function(Path(__file__).name, config["LOG_DIR"], "DEBUG",
                              datetime.datetime.now())
    logger.info("Logger created!")

    if save:
        logger.debug(f"Save file passed: {save}")
        driver(logger, save)
    logger.debug("No save file passed.")
    driver(config, logger)


if __name__ == '__main__':
    desc = "This script will dump the contents of a DINAP save file and try to"\
           "display the contents in a human readable format."
    parser = ArgumentParser(description=desc)
    config_help = "Path to app.yaml"
    config_path = "config/app.yaml"
    parser.add_argument("-c", "--config", type=str, nargs=1,
                        default=config_path, help=config_help)
    save_help = "Path to a user save file"
    parser.add_argument("-s", "--save", type=str, nargs=1, required=False,
                        help=save_help)
    out_help = ""
    parser.add_argument("-O", "--output", type=str, nargs=1, required=False,
                        help=out_help)
    color_help = ""
    parser.add_argument("-C", "--color", type=str, required=False,
                        help=color_help)
    args = parser.parse_args(namespace=namespace)
    main(args, args.save)
