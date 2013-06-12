'''Writes the necessary .glm files for a calibration round. Define recording interval and MySQL schema name here.'''

import datetime 
import re
import math
import feeder
import Milsoft_GridLAB_D_Feeder_Generation

interval = 300  # seconds
schema = 'CalibrationDB'

def makeGLM(clock, calib_file, baseGLM, case_flag, feeder_config, dir):
	'''Create populated dict and write it to .glm file
	
	- clock (dictionary) links the three seasonal dates with start and stop times (start simulation full 24 hour before day we're recording)
	- calib_file (string) -- filename of one of the calibration files generated during a calibration round 
	- baseGLM (dictionary) -- orignal base dictionary for use in Milsoft_GridLAB_D_Feeder_Generation.py
	- case_flag (int) -- flag technologies to test
	- feeder_config (string TODO: this is future work, leave as 'None')-- feeder configuration file (weather, sizing, etc)
	- dir(string)-- directory in which to store created .glm files
	'''
	# create populated dictionary
	glmDict, last_key = Milsoft_GridLAB_D_Feeder_Generation.GLD_Feeder(baseGLM,case_flag,calib_file,feeder_config) 
	
	fnames =  []
	for i in clock.keys():
		print ("Making .glm for "+i)
		# define start and end
		starttime = clock[i][0]
		rec_starttime = i
		stoptime = clock[i][1]
		
		# calculate limit
		j = datetime.datetime.strptime(rec_starttime,'%Y-%m-%d %H:%M:%S')
		k = datetime.datetime.strptime(stoptime,'%Y-%m-%d %H:%M:%S')
		diff = (k - j).total_seconds()
		limit = math.ceil(diff / interval)
		
		populated_dict = glmDict
		
		# get into clock object and change start and stop
		# glmCaseDict[last_key] = {'clock' : '',
							 # 'timezone' : '{:s}'.format(config_data['timezone']),
							 # 'starttime' : "'{:s}'".format(tech_data['start_date']),
							 # 'stoptime' : "'{:s}'".format(tech_data['end_date'])}
							 
		for i in populated_dict.keys():
			if 'clock' in populated_dict[i].keys():
				populated_dict[i]['starttime'] = "'{:s}'".format(starttime)
				populated_dict[i]['stoptime'] = "'{:s}'".format(stoptime)
		
		lkey = last_key
		populated_dict[lkey] = { 'module' : 'mysql' }
		lkey += 1
		populated_dict[lkey] = {'object' : 'database',
									'name' : '{:s}'.format(schema),
									'schema' : '{:s}'.format(schema) }
		lkey += 1
		populated_dict[lkey] = {'object' : 'mysql.recorder',
									'table' : 'network_node_recorder',
									'parent' : 'network_node',
									'property' : 'measured_real_power,measured_real_energy',
									'interval' : '{:d}'.format(interval),
									'limit' : '{:d}'.format(limit),
									'connection': schema,
									'mode': 'a'}
		
		# turn into a .glm and save it in the given directory
		if calib_file is None:
			id = 'DefaultCalibration'
		else:
			m = re.compile( '\.py$' )
			id = m.sub('',calib_file)
			
		date = re.sub('\s.*$','',rec_starttime)
		filename = id + '_' + date + '.glm'
		glmstring = feeder.sortedWrite(populated_dict)
		file = open(dir+'\\'+filename, 'w')
		file.write(glmstring)
		file.close()
		print ("File "+filename+ " written to "+dir+ ". Ready to be run in GLD.")
		fnames.append(filename)
	return fnames

def main():
	print (__doc__)
	print (makeGLM.__doc__)
if __name__ ==  '__main__':
	 main();