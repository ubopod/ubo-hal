import os
import sys
import logging.config
import platform
from datetime import datetime
import logging
import logging.config
import logging.handlers


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
                       + '/logging.cfg'
        print(log_cfg_path)

        # does the path exists ?
        if os.path.exists(log_cfg_path) is False:
            print('the specified logging configuration file %s does not exist' % log_cfg_path)
            sys.exit(1)

        logging.config.fileConfig(log_cfg_path, defaults=None,
                                  disable_existing_loggers=True)

        logger = logging.getLogger(__name__)
        logger.debug('UBO Keypad  log')
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
