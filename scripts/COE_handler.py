import sys, os, subprocess, platform, time, json
from libs.Common import *


absoluteSimulationPath = sys.argv[1]
start_time = sys.argv[2]
end_time = sys.argv[3]

pt = platform.system()


def aResultsFileAlreadyExists(absoluteSimulationPath):
	resultsFilePath = os.path.join(absoluteSimulationPath,RESULTS_FILE)
	if os.path.exists(resultsFilePath):
		if os.path.getsize(resultsFilePath) > 200:
			return True
		else:
			os.remove(resultsFilePath)
	return False


def getSessionKeyFromInitialisationResponse(rawInitResponse):
	parsedInitResponse = json.loads(rawInitResponse)[0]
	#print json.dumps(parsedInitResponse, sort_keys=True, indent=4, separators=(',',': '))
	sessionKey = parsedInitResponse['sessionId']	
	return sessionKey

def getSessionKeyFromSessionResponse(rawSessionResponse):
	parsedSessionResponse = json.loads(rawSessionResponse)
	#print json.dumps(parsedInitResponse, sort_keys=True, indent=4, separators=(',',': '))
	sessionKey = parsedSessionResponse['sessionId']	
	return sessionKey


def runSimulationAndGetResults():
	print("        get session id")

	sessionCmd = 'curl -s http://localhost:8082/createSession'
	rawSessionResponse = subprocess.check_output(sessionCmd, shell=True)
	#print ""
	#print "raw response"
	#print(rawSessionResponse)

	sessionKey = getSessionKeyFromSessionResponse(rawSessionResponse)
	print "            session id: " + str(sessionKey)


	time.sleep(1)


	print("        initiliasing simulation")

	#initilise the coe and get session id
	configPath = absoluteSimulationPath + os.path.sep + DEFAULT_SIM_CONFIG
	initialiseCmd = 'curl -s -H "Content-Type: application/json" --data @' + configPath + ' http://localhost:8082/initialize/' + str(sessionKey)
	#print ""
	#print "intialisation cmd"
	#print(initialiseCmd)

	initialisationResponse = subprocess.check_output(initialiseCmd, shell=True)
	#print ""
	#print "intialisation response"
	#print(initialisationResponse)
	#sessionKey = getSessionKeyFromInitialisationResponse(initialisationResponse)
	time.sleep(1)


	print("        launching simulation")
	if pt == 'Darwin':
		#print("Darwin detected")
		runSimulationCmd = 'curl -s -H "Content-Type: application/json" --data \'{"startTime":' + start_time + ', "endTime":' + end_time +'}\' http://localhost:8082/simulate/' + str(sessionKey)
	
	if pt == 'Linux':
		print("Linux detected - but not yet supported")
	
	if pt == 'Windows':
		#print("Windows detected")
		runSimulationCmd = 'curl -s -H "Content-Type: application/json" --data "{\\"startTime\\":' + start_time + ', \\"endTime\\":' + end_time +'}" http://localhost:8082/simulate/' + str(sessionKey)
	#print ""
	#print "simulation cmd"
	#print runSimulationCmd
	
	runSimulationResponse = subprocess.check_output(runSimulationCmd, shell=True)
	#print ""
	#print "simulation response"
	#print runSimulationResponse

	time.sleep(1)

	print("        fetching results")
	getResultsCmd = 'curl -s http://localhost:8082/result/' + str(sessionKey)
	#print ""
	#print "get results cmd"
	#print getResultsCmd

	getResultsResponse = subprocess.check_output(getResultsCmd, shell=True)
	#print ""
	#print "get results response"
	#print getResultsResponse



	resultsFile = open(absoluteSimulationPath + os.path.sep + RESULTS_FILE,'w')
	resultsFile.write(getResultsResponse)
	#print 'Results Printed'

	print("        destroying session")
	destroySessionCmd = 'curl -s http://localhost:8082/destroy/' + str(sessionKey)
	getDestroyResponse = subprocess.check_output(getResultsCmd, shell=True)
	
if aResultsFileAlreadyExists(absoluteSimulationPath):
	print "        Results file already exists, skipping this simulation"
else:
	runSimulationAndGetResults()
	