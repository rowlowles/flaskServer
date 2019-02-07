from flask import Flask, request, jsonify
import mysql.connector
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

columns = ['setName', 'cardName', 'foil', 'blue', 'green', 'red', 'white', 'black', 'cardPriceUSD', 'foilPrice']
colours = ['blue', 'green', 'red', 'white', 'black']
skipColumns = ['setName', 'cardName'] + colours
colString = ', '.join(columns)
placeHolders = ', '.join(['%s']*len(columns))

def parseCardReturnValues(results, cardName):
    cardList = {"type": 1, "cardInfo": {"cardName": cardName, "sets": []}, "sets": {}}

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
                cardList["cardInfo"][colour] = colourVal

        for item, key in zip(result, columns):
            if key in skipColumns:
                continue
            if type(item) == decimal.Decimal:
                item = float(item)
            cardObj[key] = item
        cardList["sets"][setName] = cardObj

    return jsonify(cardList)


def parseCommandReturnValues(results):
    returnObject = []
    for command in results:
        commandObject = {'type': 0, 'data': {'sortType': None, 'numCat': None, 'categories': None}}
        commandObject['data']['sortType'] = command[1]
        commandObject['data']['numCat'] = command[2]
        commandObject['data']['categories'] = json.loads(command[3])['categories']
        returnObject.append(commandObject)

    return jsonify(returnObject)

@app.route('/')
def hello():
    return 'Welcome to the cardobot server!'


@app.route('/welcome')
def BaseRoute():
    return jsonify({'Message': 'Welcome to the cardobot API!'})


@app.route('/cardInfo', methods=['GET', 'POST'])
def cardInfoRoute():
    cardName = request.get_json()['cardName']
    query = 'SELECT %s FROM magicCards WHERE cardName = \"%s\";' % (colString, cardName)
    curse.execute(query, cardName)
    results = curse.fetchall()
    return parseCardReturnValues(results, cardName)


@app.route('/sortCommands', methods=['GET', 'POST'])
def sortCommandsRoute():
    debugStat = request.get_json()
    if 'debug' in debugStat:
        query = 'SELECT * FROM sortCommands'
    else:
        query = 'SELECT * FROM sortCommands WHERE timestamp = (SELECT MAX(timestamp) from sortCommands)'
    curse.execute(query)
    results = curse.fetchall()
    return parseCommandReturnValues(results)


if __name__ == "__main__":
    app.run(debug=True)
