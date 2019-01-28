from sqlalchemy import Table, Column, Integer, Text, DateTime
from sqlalchemy.orm import mapper
from database import metadata, db_session

class cardInfo(object):
    query = db_session.query_property()

    def __init__(self,
                 cardIDNumber = None, cardName = None, setName = None, typeLine = None, blue = None, green = None,
                 white = None, black = None, red = None, cardPriceUSD = None, lastUpdated = None, foilPrice = None,
                 tcgIdNumber = None):
        self.cardIDNumber = cardIDNumber
        self.cardName = cardName
        self.setName = setName
        self.typeLine = typeLine
        self.blue = blue
        self.green = green
        self.white = white
        self.black = black
        self.red = red
        self.cardPriceUSD = cardPriceUSD
        self.lastUpdated = lastUpdated
        self.foilPrice = foilPrice
        self.tcgIdNumber = tcgIdNumber

magicCards = Table('magicCards', metadata,
                  Column('cardIDNumber', Text, primary_key=True),
                  Column('cardName',Text),
                  Column('setName',Text),
                  Column('typeLine',Text),
                  Column('blue', Integer),
                  Column('green', Integer),
                  Column('white', Integer),
                  Column('black', Integer),
                  Column('red', Integer),
                  Column('cardPriceUSD', Integer),
                  Column('lastUpdated', DateTime),
                  Column('foilPrice', Integer),
                  Column('tcgIdNumber', Integer)
                  )

mapper(cardInfo, magicCards)
