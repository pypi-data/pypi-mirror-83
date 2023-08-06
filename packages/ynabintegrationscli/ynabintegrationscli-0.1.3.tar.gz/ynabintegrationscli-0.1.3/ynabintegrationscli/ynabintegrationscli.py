#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: ynabintegrationscli.py
#
# Copyright 2019 Costas Tyfoxylos
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for ynabintegrationscli.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import argparse
import json
import logging
import logging.config

import coloredlogs
from ynabintegrationslib.ynabintegrationslib import Service

__author__ = '''Costas Tyfoxylos <costas.tyf@gmail.com>'''
__docformat__ = '''google'''
__date__ = '''10-10-2019'''
__copyright__ = '''Copyright 2019, Costas Tyfoxylos'''
__credits__ = ["Costas Tyfoxylos"]
__license__ = '''MIT'''
__maintainer__ = '''Costas Tyfoxylos'''
__email__ = '''<costas.tyf@gmail.com>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


# This is the main prefix used for logging
LOGGER_BASENAME = '''ynabintegrationscli'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


def get_arguments():
    """
    Gets us the cli arguments.

    Returns the args as parsed from the argsparser.
    """
    # https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(description='''A tool to  upload transactions from an abn amro account and
    credit card to ynab provided a configuration file and valid session cookies for an abn amro connection''')
    parser.add_argument('--config',
                        '-c',
                        action='store',
                        dest='config',
                        help='The location of the config json file',
                        default='')
    parser.add_argument('--log-level',
                        '-l',
                        help='Provide the log level. Defaults to info.',
                        dest='log_level',
                        action='store',
                        default='info',
                        choices=['debug',
                                 'info',
                                 'warning',
                                 'error',
                                 'critical'])
    args = parser.parse_args()
    return args


def setup_logging(level, config_file=None):
    """
    Sets up the logging.

    Needs the args to get the log level supplied

    Args:
        level: At which level do we log
        config_file: Configuration to use

    """
    # This will configure the logging, if the user has set a config file.
    # If there's no config file, logging will default to stdout.
    if config_file:
        # Get the config for the logger. Of course this needs exception
        # catching in case the file is not there and everything. Proper IO
        # handling is not shown here.
        try:
            with open(config_file) as conf_file:
                configuration = json.loads(conf_file.read())
                # Configure the logger
                logging.config.dictConfig(configuration)
        except ValueError:
            print(f'File "{config_file}" is not valid json, cannot continue.')
            raise SystemExit(1)
    else:
        coloredlogs.install(level=level.upper())


def main():
    """
    Main method.

    This method holds what you want to execute when
    the script is run on command line.
    """
    args = get_arguments()
    setup_logging(args.log_level)
    configuration = json.loads(open(args.config).read())
    service = Service(configuration.get('ynab_token'))
    for contract in configuration.get('contracts'):
        LOGGER.info('Registering contract "%s" for bank "%s"', contract.get('name'), contract.get('bank'))
        service.register_contract(contract.get('name'),
                                  contract.get('bank'),
                                  contract.get('type'),
                                  contract.get('authentication'))
    for account in configuration.get('accounts'):
        LOGGER.info('Registering account "%s"', account.get('ynab_name'))
        service.register_account(account.get('name'),
                                 account.get('budget_name'),
                                 account.get('ynab_name'),
                                 account.get('iban'))
    service.upload_latest_transactions()


if __name__ == '__main__':
    main()
