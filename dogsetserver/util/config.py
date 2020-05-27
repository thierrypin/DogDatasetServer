# -*- coding: utf-8 -*-

from configparser import ConfigParser


def config(filename='database.ini', section=''):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section
    conf = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            conf[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return conf