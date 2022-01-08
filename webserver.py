import json
import cherrypy
from operator import itemgetter

def write_to_json(data, filename='points.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)




class pointsRecords(object):

    @cherrypy.expose
    def index(self):
        return "Use a specific endpoint, not just the base url"

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def addPoints(self):

        if cherrypy.request.method == "POST":

            output_json = json.loads(cherrypy.request.json)

            with open('points.json') as json_file:      #add the transactions to json file
                data = json.load(json_file)
                data["addedTransactions"].append(output_json)
            write_to_json(data)


            return output_json

        else:

            return 'Must be a POST request'


    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def spendPoints(self):
        if cherrypy.request.method == 'POST':
            spentPointsList = []
            balances = {}

            output = json.loads(cherrypy.request.json)
            pointsCost = output['points']

            with open('points.json') as json_file:
                data = json.load(json_file)

            for payerInfo in data["addedTransactions"]:  # loop to create initial balances

                if balances:
                    if payerInfo["payer"] in balances:   #check for duplicate payer to combine values
                        balances[payerInfo["payer"]] = balances[payerInfo["payer"]] + payerInfo["points"]
                    else:
                        balances[payerInfo["payer"]] = payerInfo["points"]
                else:
                    balances[payerInfo["payer"]] = payerInfo["points"]


            listByTimestamp = sorted(data["addedTransactions"], key=itemgetter('timestamp'))
            for payerInfoSorted in listByTimestamp:  # Loop to spend points in order of timestamp
                spentDict = {}
                points = payerInfoSorted['points']
                payer = payerInfoSorted['payer']

                if pointsCost == 0:
                    break
                else:
                    if pointsCost > points:
                        pointsCost = pointsCost - points
                        spentDict['payer'] = payer
                        spentDict['points'] = points

                        if len(spentPointsList) > 0:
                            for dictsInfo in spentPointsList:

                                if dictsInfo['payer'] == spentDict['payer']:    #check for duplicate payer to combine values
                                    dictsInfo['points'] = 0 - (dictsInfo['points'] + points)
                                    break
                                else:
                                    spentDict['points'] = 0 - points
                                    spentPointsList.append(spentDict)
                                    break
                        else:

                            spentPointsList.append(spentDict)
                    else:
                        points = 0 - pointsCost
                        pointsCost = 0
                        spentDict["payer"] = payer
                        spentDict["points"] = points
                        spentPointsList.append(spentDict)


            for payers in spentPointsList:  # Loop to update the payers balances
                if payers["payer"] in balances:
                    balances[payers["payer"]] = balances[payers["payer"]] + payers["points"]
                else:
                    continue

            data["payerBalances"].append(balances)
            write_to_json(data)

            return json.dumps(spentPointsList)

        else:
            return "Must be a POST request"


    @cherrypy.tools.json_out()
    @cherrypy.expose
    def retrieveBalances(self):
        with open('points.json') as json_file:
            data = json.load(json_file)
        return json.dumps(data["payerBalances"])


cherrypy.quickstart(pointsRecords())

