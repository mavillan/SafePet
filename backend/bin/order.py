#!/bin/python2
import sys
import os
import subprocess

"""
WARNING: Don't execute this shit
"""


if __name__ == '__main__':
	if len(sys.argv)!=2:
		sys.exit('Wrong input!')

	path=sys.argv[1]
	os.chdir(path)

	cmd='convert {0} {1}'
	ind=1 #starting index

	for file_name in os.listdir("."):
		new_id=str(ind)
		new_id=(5-len(new_id))*'0'+new_id
		target_name='dog_'+new_id+'.jpg'
		if file_name.strip().split('.')[-1]!='jpg':
			bashCommand=cmd.format(file_name,target_name)
			process=subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
			process.communicate()[0]
			os.remove(file_name)
		else:
			if file_name==target_name:
				ind+=1
				continue
			os.rename(file_name,target_name)
		ind+=1