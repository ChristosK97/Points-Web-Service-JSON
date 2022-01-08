import json
import requests

def addTransaction(usersDict):
    r = requests.post('http://127.0.0.1:8080/addPoints', json=json.dumps(usersDict))
    print(r.text)


def multipleAdds():

    listOfAddCalls = [{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" },
                      { "payer": "UNILEVER", "points": 200, "timestamp": "2020-10-31T11:00:00Z" },
                      { "payer": "DANNON", "points": -200, "timestamp": "2020-10-31T15:00:00Z" },
                      { "payer": "MILLER COORS", "points": 10000, "timestamp": "2020-11-01T14:00:00Z" },
                      { "payer": "DANNON", "points": 300, "timestamp": "2020-10-31T10:00:00Z" }


    ]
    for item in listOfAddCalls:
        r = requests.post('http://127.0.0.1:8080/addPoints', json=json.dumps(item))
        print(r.text)


def spendPoints():
    spendCall = {"points": 5000}
    r = requests.post('http://127.0.0.1:8080/spendPoints', json=json.dumps(spendCall))
    newJson = json.loads(r.json())
    prettyResponse = json.dumps(newJson, indent=4)
    print(prettyResponse)

def retrieveBalances():
    r = requests.get('http://127.0.0.1:8080/retrieveBalances')
    responseJson = json.loads(r.json())
    prettyResponse = json.dumps(responseJson, indent=4)
    print(prettyResponse)


multipleAdds()  #add all transactions from the example

# addTransaction()  #pass parameter in the exact form from the example. ex. { "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }

# spendPoints()  #uto spend the 5000 points from example.

# retrieveBalances()  #to retrieve balances
