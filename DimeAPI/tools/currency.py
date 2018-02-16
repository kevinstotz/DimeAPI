import pymysql.cursors
import pymysql
import json
import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler

import urllib.request



def insertData(connection, data, symbol, currency_id):
    # data = b'{"RAW":{"BTC":{"USD":{"TYPE":"5","MARKET":"CCCAGG","FROMSYMBOL":"BTC","TOSYMBOL":"USD","FLAGS":"4","PRICE":11292.73,"LASTUPDATE":1517262752,"LASTVOLUME":0.208906,"LASTVOLUMETO":2356.45968,"LASTTRADEID":"181011902","VOLUMEDAY":73520.9924655142,"VOLUMEDAYTO":839779570.6581985,"VOLUME24HOUR":77600.13656951858,"VOLUME24HOURTO":888301586.0589739,"OPENDAY":11769.8,"HIGHDAY":11860.29,"LOWDAY":11089.52,"OPEN24HOUR":11854.67,"HIGH24HOUR":11877.38,"LOW24HOUR":11073.69,"LASTMARKET":"Bitfinex","CHANGE24HOUR":-561.9400000000005,"CHANGEPCT24HOUR":-4.740241609424813,"CHANGEDAY":-477.0699999999997,"CHANGEPCTDAY":-4.053339903821643,"SUPPLY":16833850,"MKTCAP":190100122910.5,"TOTALVOLUME24H":248001.94736121633,"TOTALVOLUME24HTO":2812603226.840703}}},"DISPLAY":{"BTC":{"USD":{"FROMSYMBOL":"\xc9\x83","TOSYMBOL":"$","MARKET":"CryptoCompare Index","PRICE":"$ 11,292.7","LASTUPDATE":"Just now","LASTVOLUME":"\xc9\x83 0.2089","LASTVOLUMETO":"$ 2,356.46","LASTTRADEID":"181011902","VOLUMEDAY":"\xc9\x83 73,521.0","VOLUMEDAYTO":"$ 839,779,570.7","VOLUME24HOUR":"\xc9\x83 77,600.1","VOLUME24HOURTO":"$ 888,301,586.1","OPENDAY":"$ 11,769.8","HIGHDAY":"$ 11,860.3","LOWDAY":"$ 11,089.5","OPEN24HOUR":"$ 11,854.7","HIGH24HOUR":"$ 11,877.4","LOW24HOUR":"$ 11,073.7","LASTMARKET":"Bitfinex","CHANGE24HOUR":"$ -561.94","CHANGEPCT24HOUR":"-4.74","CHANGEDAY":"$ -477.07","CHANGEPCTDAY":"-4.05","SUPPLY":"\xc9\x83 16,833,850.0","MKTCAP":"$ 190.10 B","TOTALVOLUME24H":"\xc9\x83 248.00 K","TOTALVOLUME24HTO":"$ 2,812.60 M"}}}}'
    data = json.loads(data.decode('utf8'))
    s = json.dumps(data, indent=4, sort_keys=True)
    print("Price:" + str(data['RAW'][symbol]['USD']['PRICE']))
    price = data['RAW'][symbol]['USD']['PRICE']
    print(data['RAW'][symbol]['USD']['SUPPLY'])
    supply = data['RAW'][symbol]['USD']['SUPPLY']
    print(data['RAW'][symbol]['USD']['LASTUPDATE'])
    timestamp = data['RAW'][symbol]['USD']['LASTUPDATE']
    print("marketCap:" + str(float(data['RAW'][symbol]['USD']['SUPPLY'] * float(data['RAW'][symbol]['USD']['PRICE']))))
    marketCap = float(data['RAW'][symbol]['USD']['SUPPLY']) * float(data['RAW'][symbol]['USD']['PRICE'])
    print(currency_id)

    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `dimeapi_currencyhistory` (`price`, `marketCap`, `totalCoinSupply`,`currency_id`, `timestamp`) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (price, marketCap, supply,currency_id, timestamp ))
        connection.commit()

def some_job():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='dimeapi-dev',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    sql = "SELECT currency_id FROM `dimeapi_DimeMutualFund` WHERE rebalanceDate = '2017-12-23'"
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            for row in cursor.fetchall():
                with connection.cursor() as currency:
                    sql = "SELECT `symbol` FROM `dimeapi_currency` WHERE `id`=%s"
                    currency.execute(sql, row['currency_id'])
                    for curr in currency.fetchall():
                        with connection.cursor() as url2get:
                            sql = "SELECT `url`  FROM `dimeapi_xchange` WHERE `id` = 1"
                            url2get.execute(sql)
                            for row2 in url2get.fetchall():
                                # print(row2['url'].replace('XXX',curr['symbol']))
                                data = urllib.request.urlopen(row2['url'].replace('XXX',curr['symbol'])).read()
                                insertData(connection, data, curr['symbol'], row['currency_id'] )


    finally:
        connection.close()

scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', hours=1)
scheduler.start()
