'''
Created on Apr 25, 2015

@author: jordan
'''
import logging
import os

# set up logging to file - see previous section for more details
log_fname = 'res/logger.log'
if not os.path.exists(log_fname):
    with open(log_fname, 'w') as f:
        pass
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=log_fname,
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)


if __name__ == '__main__':
    logging.info('hello')