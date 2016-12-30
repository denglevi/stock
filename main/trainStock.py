# coding:utf-8
import MySQLdb
import click


# @click.group()
# def getStock():
#     pass
#
# @getStock.command()
# @click.option("--code", prompt="your code", help="please input your code")
# def getStockCMD(code):
#     '''dddddd'''
#     print("your code is %s" % code)
#
# @click.group()
# def getStockMeanPriceByDay():
#     pass
#
# @getStockMeanPriceByDay.command()
# @click.option("--day", prompt="day num", help="please input your day num")
# def getStockMeanPriceByDayCMD(day):
#     '''day'''
#     click.echo("you day num is %s" % day)
#
#
# analyseStock = click.CommandCollection(sources=[getStock, getStockMeanPriceByDay])

class TrainStock(click.MultiCommand):
    def importStockInfo(self):
        '''importStockInfo'''
        # pass
    @click.command()
    @click.option("--code",prompt="your code",help="please input your code")
    def importStockPrice(self):
        '''importStockPrice'''
        # pass


@click.command(cls=TrainStock)
def trainStock(cls):
    cls.importStockPrice()
    pass


if __name__ == "__main__":
    trainStock()
