import sys
import os

up_dir = os.path.dirname(os.path.abspath(__file__)) + '/../../utils'
sys.path.append(up_dir)

import utils.ubo_logger


def main(argv: object):
    """
    Main function
    - instantiate KEYPAD class
    """

    # ==================================
    # Establish the logging mechanism
    # local_log is true if we want 
    #  
    # ==================================
    local_log: bool = False
    utils.ubo_logger.establish_logging(local_log)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])

    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
