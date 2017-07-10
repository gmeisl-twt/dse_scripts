# change to dse directory for calling other scripts
import os,sys, time
try:
  os.chdir(os.path.dirname(os.path.realpath(__file__)))
except WindowsError, OSError:
  print 'Error changing to scripts directory'
  sys.exit(1)
  
import json, platform, subprocess, time, io, math
from subprocess import CalledProcessError 
from libs.Common import *

from Tkinter import *
import time
root = Tk()

S = Scrollbar(root)
T = Text(root, height=4, width=50)
S.pack(side=RIGHT, fill=Y)
T.pack(side=LEFT, fill=Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)

#li = 'Carl Patrick Lindsay Helmut Chris Gwen'.split()
#listb = Listbox(root)           # Create a listbox widget
#for item in li:                 # Insert each item within li into the listbox
#    listb.insert(0,item)

#listb.pack()                    # Pack listbox widget



argumentsCountNormal = 4
argumentsCountRepairMode = 5

timingScriptStart = time.time()




def iterateOverScenarios(scenarioList, keyList, paramValues, simParamVals, dseConfig, absoluteResultsPath ):
	if len(scenarioList) > 0:
		for scenario in scenarioList:
			iterateOverParams(scenario, dseConfig['parameters'].keys(), dseConfig['parameters'], {}, dseConfig, absoluteResultsPath)
	else:
		iterateOverParams('', dseConfig['parameters'].keys(), dseConfig['parameters'], {}, dseConfig, absoluteResultsPath)
	

def iterateOverParams(scenarioID, keyList, paramValues, simParamVals, dseConfig, absoluteResultsPath ):
	keyListLocal = list(keyList)
	thisKey = keyListLocal.pop()
	
	for val in paramValues[thisKey]:
		simParamValsLocal = dict(simParamVals)
		simParamValsLocal[thisKey] = val
	
		if len(keyListLocal) >0:
			iterateOverParams(scenarioID, keyListLocal, paramValues, simParamValsLocal, dseConfig, absoluteResultsPath)
		else:
			if checkParameterContraints(simParamValsLocal, dseConfig['parameterConstraints']):
				message = "Running a sim"
				T.insert(END,message)
				root.update()
				defineRunAndEvluatieSimulation(parsed_multimodel_json, scenarioID, simParamValsLocal, dseConfig, absoluteResultsPath, absoluteProjectPath)
			else:
				print simParamValsLocal, " does not meet parameter constraints"
	return

def call(args):
  p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out,err = p.communicate()
  for line in out.split(os.linesep):
    if not line == '':
      print line
  for line in err.split(os.linesep):
    if not line == '':
      print line  
 

 
 
def dseMain(): 
 
	print ("DSE Exhaustive starting")

	print ("Processing command arguments")
	global absoluteProjectPath
	absoluteProjectPath  = sys.argv[1]
	relativeExperimentConfigPath = sys.argv[2]
	#experimentConfigFile = experimentConfigName + DSE_CONFIG_EXTENSION
	
	
	#multiModelConfigName = sys.argv[3]
	#multiModelConfigFile = multiModelConfigName + MULTI_MODEL_EXTENSION
	
	relativeCoeConfigFile = sys.argv[3]
	absoluteCoeConfigFile = absoluteProjectPath + os.path.sep + relativeCoeConfigFile
	
	#absoluteExperimentPath = absoluteProjectPath + os.path.sep + DSE_FOLDER + os.path.sep + experimentConfigName + os.path.sep
	
	absoluteExperimentConfigPath = os.path.join(absoluteProjectPath, relativeExperimentConfigPath)
	trimLocation = absoluteExperimentConfigPath.rfind(os.path.sep)
	absoluteExperimentPath = absoluteExperimentConfigPath[:trimLocation] + os.path.sep
	
		#absoluteBaseMultiModelPath = absoluteProjectPath + os.path.sep + MULTI_MODEL_FOLDER + os.path.sep + multiModelConfigName + os.path.sep + multiModelConfigFile
	
	absoluteUserScriptPath = absoluteProjectPath + os.path.sep + USER_METRICS_FOLDER + os.path.sep
	
	
	
	if len(sys.argv) == argumentsCountRepairMode:
		dateTimeFolder = sys.argv[argumentsCountRepairMode - 1]
	else:
		dateTimeFolder = dateTimeFolderName()
	
	absoluteResultsPath = absoluteExperimentPath + dateTimeFolder
	
	print ("Opening DSE config: " + absoluteExperimentConfigPath)
	dseConfig_data = open(absoluteExperimentConfigPath)
	dseConfig = json.load(dseConfig_data)
		
	print ("Combining model configs: ")
	
	global parsed_multimodel_json
	parsed_multimodel_json = combineModelFiles(absoluteCoeConfigFile, dseConfig, absoluteProjectPath)
	
	#multimodel_json_data = open(absoluteBaseMultiModelPath)
	#json.load(multimodel_json_data)
	
	print ("Creating Date Time folder")
	makeDateTimeFolder(absoluteExperimentPath, dateTimeFolder)
	
	print("Starting the Simulations...")
	T.insert(END,"Starting the Simulations...")
	root.update()                   # Pack listbox widget
	timingSimulationsStart = time.time()
	iterateOverScenarios(dseConfig['scenarios'], dseConfig['parameters'].keys(), dseConfig['parameters'], {}, dseConfig, absoluteResultsPath)
	timingSimulationsEnd = time.time()
	print("Simulations complete.")
	T.insert(END,"Simulations complete.")
	root.update()                    # Pack listbox widget
	
	print("Starting the ranking...")
	call(["python", "Ranking_pareto.py" ,absoluteExperimentPath, absoluteExperimentConfigPath,  absoluteResultsPath])
	print("Ranking complete.")
	print("Generating results page...")
	call(["python", "Output_HTML.py", absoluteExperimentPath, absoluteResultsPath])
	print("Page complete.")
	
	timingScriptEnd = time.time()
	
	print
	print "Timings" 
	print "Total script time:", timingScriptEnd - timingScriptStart, " seconds" 
	print "Total simulation time:", timingSimulationsEnd - timingSimulationsStart, " seconds" 
	
	root.destroy()
	
root.after(1000,dseMain)	
root.mainloop()                 # Execute the main event handler
