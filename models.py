from sqlalchemy import Table, Column, Integer, Text
from sqlalchemy.orm import mapper
from database import metadata, db_session

class cardInfo(object):
    query = db_session.query_property()

    def __init__(self,
                 cardIDNumber = None, cardName = None, setName = None, typeLine = None, blue = None, green = None,
                 white = None, black = None, red = None, cardPriceUSD = None, lastUpdated = None, foilPrice = None,
                 tcgIdNumber = None):

        self.id = cardIDNumber
        self.name = cardName
        self.setName = setName
        self.typeLine = typeLine
        self.blue = blue
        self.green = green
        self.white = white
        self.black = black
        self.red = red
        self.price = cardPriceUSD
        self.lastUpdated = lastUpdated
        self.foilPrice = foilPrice
        self.tcgIdNumber = tcgIdNumber

card_info = Table('magicCards', metadata,
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
                  Column('lastUpdated', Text),
                  Column('foilPrice', Integer),
                  Column('tcgIdNumber', Integer)
                  )

mapper(cardInfo, card_info)
