"""
Create dashboard with information for all the applications, each subsection will have the following tiles:
 Application overview, hosts health, service health, database health

Preconditions: 
	All Apps, Hosts, PG, Services and DB need to have an Application Tag
	API Token: read and write configuration


Limitations:
Entity must not be larger than 100000 bytes - 48 Applications / dashboards subsecction

"""
import requests, ssl, os, sys, json, copy

ENV = 'https://YOUR-DYNATRACE-CLUSTER-URL'
TOKEN = 'YOUR-DYNATRACE-API-TOKEN'
HEADERS = {'Authorization': 'Api-Token ' + TOKEN}
HEADERS_POST = {'Authorization': 'Api-Token ' + TOKEN, 'Content-Type' : 'application/json'}
PATH = os.getcwd()


# GetAppsTags: Retrieve all the Applications and returns all the Tags from each application 
#
def getAppsTags():
	appsTags=[]
	try:
		# Retrieve all Application-IDs
		r = requests.get(ENV + '/api/v1/entity/applications', headers=HEADERS)
		res = r.json()
		for entry in res:
			# for each Application-ID retrieve informations for each Application
			app = requests.get(ENV + '/api/v1/entity/applications/' + entry['entityId'], headers=HEADERS)
			tags = app.json()['tags']
			# store in appTags list, all the application tags
			if tags:
				for tag in tags:
				 	appsTags.append(tag['key'])
		return appsTags
	except ssl.SSLError:
		print("SSL Error")


# ReadTemplate: read information from the file template.json, in the same locations as the dahsboard.py script
#				Rerunts the data in json format
def readTemplate():
	with open('template.json', encoding="utf8") as json_file:  
		data = json.load(json_file)
	return data


# createNewDashboard: Retrieve all App tags and the data from template.json ( the dahsboard teamplate )
#					for each AppTag, creates a new tile group based on the template.json and filter by tag.
#					Finally create a new dashboard with all the new tiles.
#
def createNewDashboard():
	# Retrieve list of all the tags from monitored Applications
	appTags = getAppsTags()
	# Retrieve tiles from Template.json
	template = readTemplate()
	tilesTemplate = template['tiles']
	# position of tiles:
	# top : starts at 0 and increments 228 to create a new row
	# left : tiles next to left side of the screen start at 0
	# right : tiles from the half right of the screen start in 722
	top = 0
	right = 722
	left = 0

	newTilesList = []
	
	# For each tag, create tiles replacing the tag and position. The new tiles are added to the newTilesList 
	for tag in appTags:
		if left == 0 :
			newTilesList += replaceTag(tilesTemplate, tag, top, left)
			left = right # so next iteration the tiles will start on the right half of the screen
		else:
			newTilesList += replaceTag(tilesTemplate, tag, top, left)
			left = 0
			top += 228 # increments top, so on next interation top == next new row

	# replace the tiles from the template, with the new created tiles
	template['tiles'] = newTilesList;
	# Transform the dashboard data to JSON format
	newjson = json.JSONEncoder().encode(template)
	# post and create a new dahsboard with the json data
	postNewDashboard(newjson)


# PostNewDashboard: Create a new dashboard with the newDashboardJon data
#
def postNewDashboard(newDashboardJson):
	try:
		r = requests.post(ENV + '/api/config/v1/dashboards', headers=HEADERS_POST, data=newDashboardJson)
		res = r.json()
		if r.status_code == 201:
			dashboard_url = ENV + "/#dashboard;id=" + res['id']
			print()
			print("Response code: %s, Id new dashboards: %s, URL new dashboard: %s" % (r.status_code, res['id'], dashboard_url))
			print()
		else:
			print("Error - Response code: %s , Response: %s"% (r.status_code, res))	
	except ssl.SSLError:
		print("SSL Error")

# ReplaceTag: for each tile from the tilesTemplate, replace the tag to filter the tile
#			  The top and left values also are modified to modify the position of the tile
#
def replaceTag(tilesTemplate, tag, top, left):
	newTiles = copy.deepcopy(tilesTemplate)
	for tile in newTiles:
		# Edit tile possition:
		# Edit top possition to adapt the new tile to the right possition
		tile['bounds']['top'] += top
		# Edit left possition to adapt the new tile to the right possition
		tile['bounds']['left'] += left

		# Edit Tile tag
		# Markdown tile does not have a tag filter so it is used as title of tiles subsection
		if tile['tileType'] == "MARKDOWN":
			tile['markdown'] = "## " + tag 
		else:
		# for the other tiles (Application, hosts, services and database) apply the correct tag
			filterType = tile['filterConfig']['type']
			tile['filterConfig']['filtersPerEntityType'][filterType]['AUTO_TAGS'] = [tag + "⁈‼⁉%7C%7C%7CAll%7C%7C%7C"]
	return newTiles


def main():
	createNewDashboard()

if __name__ == '__main__':
	main()