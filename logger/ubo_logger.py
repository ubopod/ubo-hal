# ===============================================================
# This python module to handle a simple logging mechanism
# it relies  on the following modules:
# logging: https://docs.python.org/3/library/logging.html
# logging.config: https://docs.python.org/3/library/logging.config.html
# loging.handlers: https://docs.python.org/3/library/logging.handlers.html
#
# ===============================================================
import os
import sys
import platform
from datetime import datetime
import logging
import logging.config
import logging.handlers
import argparse


def configure_logging(logfile_path):
    """
    Configure the logging mechanism
    This function is used to specify where the log files will reside.
    @param logfile_path: The file path where the logging files will be stored
    This function does:
    - Assign INFO and DEBUG level to logger file handler and console handler
    """

    # specify what we want to see on log lines
    # for debug and info
    debug_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] "
        "[%(name)s] [%(funcName)s():%(lineno)s] [PID:%(process)d \
TID:%(thread)d] %(message)s",
        "%d/%m/%Y %H:%M:%S")

    info_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s]"
        " [%(name)s] [%(funcName)s():%(lineno)s] [PID:%(process)d \
TID:%(thread)d] %(message)s",
        "%d/%m/%Y %H:%M:%S")

    file_handler = logging.handlers. \
        RotatingFileHandler(logfile_path, maxBytes=500 * 1024, backupCount=300,
                            encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    file_handler.setFormatter(debug_formatter)
    console_handler.setFormatter(info_formatter)

    logging.root.setLevel(logging.DEBUG)
    logging.root.addHandler(file_handler)
    logging.root.addHandler(console_handler)
    return


def establish_logging(local_log=True):
    """
    This function establishes the overall
    logging mechanism
    """
    if local_log is False:
        # Log on a specific filepath
        log_cfg_path = os.path.abspath(os.path.dirname(sys.argv[0])) \
                       + '/config.ini'
        print(log_cfg_path)

        # does the path exists ?
        if os.path.exists(log_cfg_path) is False:
            print('the specified logging configuration file %s does not exist' % log_cfg_path)
            sys.exit(1)

        logging.config.fileConfig(log_cfg_path, defaults=None,
                                  disable_existing_loggers=True)

        logger = logging.getLogger(__name__)
        logger.debug('UBO Keypad log')
    else:
        now = datetime.now().isoformat()
        now = str(now).split('.')[0].replace(':', '-')

        # Create directory for logs
        h = platform.uname()[1]
        this_directory = os.path.realpath(os.path.dirname(__file__))
        logs_path = this_directory + '/Logs/' + h + '/'
        if not os.path.exists(logs_path):
            os.makedirs(logs_path)
        # create a cycle number file
        # this file has a single number incremented each
        # time this program is run
        cycle_path = logs_path + 'cycle'
        if os.path.exists(cycle_path) is False:
            with open(cycle_path, 'w') as f:
                cycle = '1'
                f.write(cycle)
                f.close()
        else:
            with open(cycle_path, 'r') as f:
                cycle = f.read()
                f.close()
            cycle = int(cycle)
            cycle += 1
            cycle = str(cycle)

            with open(cycle_path, 'w') as f:
                f.write(cycle)
                f.close()
        logs_path += cycle
        if not os.path.exists(logs_path):
            os.makedirs(logs_path)
        configure_logging(logs_path + '/' + now + '_UBO_Keypad.log')
        logger = logging.getLogger(__name__)
        logger.debug('UBO Keypad log')
    return

def command_line_params(argv: object) -> object:
    """
    This function processes the arguments found on the command line
    We chose to use the argparse module in preference of getopt module
    :return:
    """
    # =======================================================
    # Establish the CLI commands parser
    # we use argparse module
    # ========================================================
    logger = None

    print(argv)
    # Create the parser and add arguments
    parser = argparse.ArgumentParser(prog='UBO',
                                     description='UBO Keypad command line arguments',
                                     epilog='UBO Keypad')

    # Add the Verbose option
    parser.add_argument('--verbose', '-v',
                        dest='verbose_level', nargs='?', type=str,
                        help='Select a verbosity level to use')

    # Add the Config option
    parser.add_argument('--config', '-c',
                        dest='config_file', nargs='?', type=str,
                        help='Specify a Configuration file')

    # Parse and process the results
    args = parser.parse_args()

    # Process verbose flag
    if args.verbose_level:
        logger = logging.getLogger(__name__)
        logger.debug('Verbosity Level: ' + args.verbose_level)
        verbose_level = args.verbose_level

        valid_levels = [
            'NOTSET',
            'DEBUG',
            'INFO',
            'WARNING',
            'ERROR',
            'CRITICAL'
        ]

        logger_level = [
            logging.NOTSET,
            logging.DEBUG,
            logging.INFO,
            logging.WARNING,
            logging.ERROR,
            logging.CRITICAL
        ]

        if verbose_level in valid_levels:
            i = valid_levels.index(verbose_level)
            logger.setLevel(logger_level[i])
        else:
            logger.error('An invalid verbose level was specified %s:' % verbose_level)

    # Process config file flag
    if args.config_file:
        logger.debug('Config file: ' + args.config_file)
        config_file = args.config_file
        # check for existence of this file
        if os.path.exists(config_file) is False:
            logger.error('The specified config file %s does not exist' % config_file)
        else:
            logger.info('The UBO config file is %s: ' % config_file)
    return