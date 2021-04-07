"""Wrap configuration options as an object"""
import argparse
import logging

import yaml


class Config:
    """Class to represent flathunter configuration"""

    __log__ = logging.getLogger('flathunt')

    def __init__(self, filename=None, string=None):
        if string is not None:
            self.config = yaml.safe_load(string)
        elif filename is not None:
            self.__log__.info("Using config %s", filename)
            with open(filename) as file:
                self.config = yaml.safe_load(file)
        else:
            raise ValueError("Either filename or string must be given")

    def __iter__(self):
        """Emulate dictionary"""
        return self.config.__iter__()

    def __getitem__(self, value):
        """Emulate dictionary"""
        return self.config[value]

    def get(self, key, value=None):
        """Emulate dictionary"""
        return self.config.get(key, value)

    def redis_host(self):
        return command_line_arg("redis_host") or self.config["redis"]["host"]

    def redis_port(self):
        return command_line_arg("redis_port") or self.config["redis"]["port"]


def command_line_arg(argument):
    parser = argparse.ArgumentParser()
    parser.add_argument("--" + argument)
    print(parser.parse_known_args()[0])
    return getattr(parser.parse_known_args()[0], argument)
