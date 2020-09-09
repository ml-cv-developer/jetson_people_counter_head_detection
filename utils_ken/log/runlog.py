from getlog import get_logger
from getlog import get_logger_console
from getlog import get_logger_file
import time
import logging

def run() :
	logname = 'runlog'
	logfile = 'run.log'
	runloger = get_logger_console(logname=logname)
	# runloger = get_logger_file(logname=logname, logfile=logfile)
	runloger.debug('start')
	runloger.debug('This is debug')


def test() :
	# Create a custom logger
	logger = logging.getLogger('hello')

	# Create handlers
	c_handler = logging.StreamHandler()
	f_handler = logging.FileHandler('file.log')
	c_handler.setLevel(logging.ERROR)
	f_handler.setLevel(logging.ERROR)

	# Create formatters and add it to handlers
	c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
	f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	c_handler.setFormatter(c_format)
	f_handler.setFormatter(f_format)

	# Add handlers to the logger
	logger.addHandler(c_handler)
	logger.addHandler(f_handler)

	logger.warning('This is a warning')
	logger.error('This is an error')	


if __name__ == '__main__' :
	while(True) :
		time.sleep(1)
		print("start")
		# test()
		run()