#!/usr/bin/env python3
'''
parser.py

A fleshed out implementation of argparger with checks for input error.

All parameters get passed to pos_calc.run()

'''


import argparse
import datetime
import os
import math
import sys
import pos_calc

verbose = False

def my_abort():
	''' Abort helper, added 'my' for namespace disambiguation '''
	global verbose
	if verbose:
		print("Aborting, exit 1")
	
		return

def verify_config(config_filename):
	''' Verify given parameter: config_file exists '''
	if not os.path.isfile(config_filename):
		print (config_filename,": no such file found")
		my_abort()
def verify_ra_dec(ra, dec):
	''' Verify given parameters: ra and dec are within their respective ranges '''
	if ra > 2*math.pi or ra < 0:
		print ("Bad right ascension value. ra (in radians) must be between 0 and 2pi")
		my_abort()
	if dec > math.pi or dec < 0:
		print ("Bad declination value. dec (in radians) must be between 0 and pi")
		my_abort()

def abreviated_str_to_ms(s):
	''' Convert time string like '12m' to ms. Also format checking'''
	unit  = ''.join([i for i in s if not i.isdigit()])
	count = float(''.join([i for i in s if i.isdigit()]))
	if len(unit) != 1:
		print(s, ": bad time string. Should only contain one char (h,m or s)")
		my_abort()
		return

	if unit == 'h':
		count *= 3600000
	elif unit == 'm':
		count *= 60000
	elif unit == 's':
		count *= 1000
	else:
		print(s, ": bad time string. Should only contain one char (h,m or s)")
		my_abort()
		return
	return count




if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(add_help=True)
	parser.add_argument("-ra", "--right_ascension", type=float, required=True,
	                    help="Right ascension of observation's target (radians)")
	parser.add_argument("-dec", "--declination", type=float, required=True,
	                    help="Declination of observation's target (radians)")
	parser.add_argument("-s", "--start", type=int, action="store", dest='start_utc', default=datetime.datetime.utcnow(),
	                    help="UTC timestamp for the start of the observation of target")

	parser.add_argument("-d", "--duration", type=str, action="store", dest='duration',required=True,
	                    help="How long will target be observed. Use abbreviated string i.e. 12m, 0.5h, 90s etc.")
	# TODO, add freq for beam-haflwidth calc

	parser.add_argument("-v", "--verbose", action="store_true", default=False,
	                    help="increase output verbosity")

	# parser.add_argument("-o", "--output", type=str, action="store", dest='output_filename',
	#                     help="Outout filename for writing the results.")
	# TODO, use this ^^ when you have a better idea how it might be used
	# TODO, quiet mode
	parser.add_argument("-f", "--config_file", type=str, action="store", dest='config_filename', required=True,
	                    help="Outout filename for writing the results.")

	args = parser.parse_args().__dict__

	verbose = args["verbose"]

	target_ra = args["right_ascension"]
	target_dec = args["declination"]
	verify_ra_dec(target_dec, target_ra)

	start_time_utc = args['start_utc']
	# TODO, catch case where start is too far from now and tles are screwed up
	duration_str = args['duration']
	duration_ms = abreviated_str_to_ms(duration_str)

	config_filename = args['config_filename']
	verify_config(config_filename)
	pos_calc.run(config_filename=config_filename, target_ra=target_ra, target_dec=target_dec, verbose=verbose, start_time_utc=start_time_utc, duration_ms=duration_ms)