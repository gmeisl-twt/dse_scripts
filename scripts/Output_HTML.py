import os, sys, json, io, webbrowser
from libs.Common import *

absoluteExperimentDir = sys.argv[1]
absoluteResultsPath = sys.argv[2]

def addGraphsForRanking(rank_id):
	htmlFile.write('<img src=graphs/' + rank_id + '.png>\n')

def putRankingsIntoTable(rank_id):
	htmlFile.write('<table>\n')
	addHeadings()
	addRows(rank_id)
	htmlFile.write('</table>\n')
	
def addRows(rank_id):
	this_ranking_root = ranking_json[rank_id]
	sorted_ranks = sorted(this_ranking_root)
	for rank in sorted_ranks:
		for design in this_ranking_root[rank]:
			addRow(rank,design)
			
def addRow(rank, design):
	htmlFile.write('<tr>')
	htmlFile.write('<td>' + rank + '</td>')
	addObjectiveValues(design)
	addDesignParameters(design)
	htmlFile.write('<tr>\n')
	
def addDesignParameters(design):
	configData = open(absoluteResultsPath + os.path.sep + design + os.path.sep + DEFAULT_SIM_CONFIG)
	config_json = json.load(configData)
	params_json = config_json['parameters']
	for param in params_json:
		htmlFile.write('<td>' + str(params_json[param]) + '</td>')

def addObjectiveValues(design):
	objectivesData = open(absoluteResultsPath + os.path.sep + design + os.path.sep + OBJECTIVES_FILE)
	objectives_json = json.load(objectivesData)
	for objective in objectives_json:
		htmlFile.write('<td>' + str(objectives_json[objective]) + '</td>')
	
def addHeadings():
	htmlFile.write('<tr>')
	htmlFile.write('<th>Rank</th>')
	firstSim = ranking_json['simulations'][0]
	getObjectiveHeadings(firstSim)
	getParameterHeadings(firstSim)
	htmlFile.write('</tr>\n')
	
def getObjectiveHeadings(design):
	objectivesData = open(absoluteResultsPath + os.path.sep + design + os.path.sep + OBJECTIVES_FILE)
	objectives_json = json.load(objectivesData)
	for objective in objectives_json:
		htmlFile.write('<th>' + objective + '</th>')
	
	
def getParameterHeadings(design):
	configData = open(absoluteResultsPath  + os.path.sep + design + os.path.sep + DEFAULT_SIM_CONFIG)
	config_json = json.load(configData)
	params_json = config_json['parameters']
	for param in params_json:
		htmlFile.write('<th>' + trimmedParamName(param) + '</th>')
		
def includeStyleSheet(fileName):
	returnString = ""
	if os.path.exists(fileName):
		cssFile = open(fileName)
		return cssFile.read()
	return ""
		
def trimmedParamName(param):
	tokens = param.split("}")
	return tokens[1][1:]
		
		
def listUnrankbleResultsInTable():
	htmlFile.write('<table>\n')
	addUnrankableRows()	
	htmlFile.write('</table>\n')
	
def addUnrankableRows():
	this_ranking_root = ranking_json['unrankable']
	#sorted_ranks = sorted(this_ranking_root)
	for folder in this_ranking_root:
		htmlFile.write('<tr>')
		htmlFile.write('<td>' + folder + '</td>')
		htmlFile.write('<tr>\n')


htmlFileName = absoluteResultsPath + os.path.sep +  HTML_RESULTS
htmlFile = open(htmlFileName,'w')

# create html header
htmlFile.write ('<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">')
htmlFile.write ('<html xmlns="http://www.w3.org/1999/xhtml">')
htmlFile.write ('<head>\n')
htmlFile.write ('<title>DSE Results Page</title>\n')
htmlFile.write ('<style>')
execdir = os.path.dirname(os.path.realpath(__file__))
htmlFile.write (includeStyleSheet(os.path.join(execdir, 'results.css')))
htmlFile.write ('\n</style>')
htmlFile.write ('</head>\n')
htmlFile.write ('<body>\n')


# open ranking.json
json_data = open(absoluteResultsPath + os.path.sep + RANKING_FILE)
ranking_json = json.load(json_data)

# read in rank ids (just pareto for now)
rank_id = 'pareto'

# create section
htmlFile.write('<h1>' + rank_id + '</h1>\n')

# add graph
addGraphsForRanking(rank_id)

# create section
htmlFile.write('<h2> Ranked results</h2>\n')

# add table of data with id, objective values and parameters
putRankingsIntoTable(rank_id)

# create section
htmlFile.write('<h2> Unrankable results</h2>\n')

# add table of unrankable results
listUnrankbleResultsInTable()

# close html
htmlFile.write ('</body>')
htmlFile.write ('</html>')

# close file
htmlFile.close()
