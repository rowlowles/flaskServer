from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime
from pytz import timezone
import decimal
import json

secrets = json.load(open('secrets.json', encoding="utf8"))
teamMarfDB = mysql.connector.connect(
    host=secrets['host'],
    port=secrets['port'],
    user=secrets['user'],
    password=secrets['password'],
    db=secrets['db']
)
curse = teamMarfDB.cursor()

app = Flask(__name__)

# Constants and other useful variables
est = timezone('EST')
columns = ['setName', 'cardName', 'foil', 'blue', 'green', 'red', 'white', 'black', 'cardPriceUSD', 'foilPrice']
colours = ['blue', 'green', 'red', 'white', 'black']
skipColumns = ['setName', 'cardName'] + colours
colString = ', '.join(columns)
placeHolders = ', '.join(['%s']*len(columns))


def parseCardReturnValues(results, cardName):
    """
    Take a list of results for each edition of a card we receive and compile it into a nice simple format to parse
    Return format is
    {"cardInfo": {"cardName":..., "sets":[...], "red":0/1, "green":1/0, "blue":1/0, "white":1/0, "black":1/0},
    "sets": {"setName1":{"cardPriceUSD": #, "foil":1/0, "foilPrice":#} ... "setNameN:{}},
    "type":1
    }
    :param results: The list of tuples we get from MySQL
    :param cardName: The card name searched for
    :return: JSON string in above format
    """
    cardList = {"type": 1, "cardInfo": {"cardName": cardName, "colour": {}, "sets": []}, "sets": {}}
    for index, result in enumerate(results):
        setNameIndex = columns.index('setName')
        setName = result[setNameIndex]
        cardList["cardInfo"]["sets"].append(setName)
        cardObj = {}

        if index == 0:
            # Get index for the colours
            # Append colours to parent dictionary
            for colour in colours:
                colourVal = result[columns.index(colour)]
                cardList["cardInfo"]['colour'][colour] = colourVal

        for item, key in zip(result, columns):
            if key in skipColumns:
                continue
            if type(item) == decimal.Decimal:
                item = float(item)
            cardObj[key] = item
        cardList["sets"][setName] = cardObj

    return jsonify(cardList)


def parseCommandReturnValues(results):
    """
    Take the list of command objects and parse them into an easy to use format. Return format is:
    [{
    "data":{"categories":{"cat0": ..., ..., "catM": ...}, "numCat": #, "sortType": ...},
    "type": 0
    }]
    :param results:
    :return:
    """
    returnObject = []
    for command in results:
        # print(command)
        commandObject = {'type': 0, 'data': {'sortType': None, 'numCat': None, 'categories': None}}
        commandObject['data']['sortType'] = command[1]
        commandObject['data']['numCat'] = command[2]
        commandObject['data']['categories'] = json.loads(command[3])['categories']
        returnObject.append(commandObject)

    return jsonify(returnObject)


@app.route('/')
def BaseRoute():
    return jsonify({'Message': 'Welcome to the cardobot API!'})


@app.route('/cardInfo', methods=['GET'])
def cardInfoRoute():
    """
    Take a card name from a user's post and return a list of cards which match it. Set "limit" in request body if 
    you are sorting by colour so you don't need as huge of a response object. 
    :return:
    """
    message = request.get_json()
    cardName = message['cardName']
    query = 'SELECT %s FROM magicCards WHERE cardName = \"%s\"' % (colString, cardName)
    if 'limit' in message:
        query += ' LIMIT 1'
    curse.execute(query)
    results = curse.fetchall()
    return parseCardReturnValues(results, cardName)


@app.route('/sortCommands', methods=['GET'])
def sortCommandsRoute():
    """
    Get the sort commands to be used for the sorting system. Set "debug" inb request body if you want
    :return: 
    """
    debugStat = request.get_json()
    if 'debug' in debugStat:
        query = 'SELECT * FROM sortCommands'
    else:
        query = 'SELECT * FROM sortCommands WHERE received = 0 ORDER BY timestamp ASC LIMIT 1'
    curse.execute(query)
    results = parseCommandReturnValues(curse.fetchall())

    if 'debug' not in debugStat:
        updateQuery = 'UPDATE team_marf_db.sortCommands SET received = 1 WHERE received = 0 ' \
                      'ORDER BY timestamp ASC LIMIT 1'
        curse.execute(updateQuery)

    teamMarfDB.commit()
    return results


@app.route('/postCommand', methods=['POST'])
def postCommand():
    """
    Insert a sorting command into the database
    :return:
    """
    message = request.get_json()
    sortType = message['sortType']
    categories = json.dumps({"categories": message['categories']})
    numCats = len(categories['categories'])
    timestamp = datetime.now(est)
    sortObj = (timestamp, sortType, numCats, categories)
    query = "INSERT INTO sortCommands (timestamp, sortType, numCat, categories) VALUES (%s, %s, %s, %s)"
    curse.execute(query, sortObj)
    teamMarfDB.commit()
    return jsonify({"message": 'Post successful'})


@app.route('/postCollection', methods=['POST'])
def postCollection():
    """
    Post a user's collection to the database
    :return:
    """
    message = request.get_json()
    name = message['userName']
    value = message['collectionValue']
    collection = json.dumps(message['collection'])
    query = 'INSERT INTO userCards (userName, userCollectionValue, userCardCollection) VALUES (\'%s\', %s, \'%s\') ON DUPLICATE' \
            ' KEY UPDATE userCollectionValue=%s, userCardCollection = \'%s\'' % (name, value, collection, value, collection)
    print(query)
    curse.execute(query)
    teamMarfDB.commit()
    return jsonify({"message": 'Post successful'})


if __name__ == "__main__":
    app.run(debug=True)
