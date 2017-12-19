from datetime import datetime

import tweepy

from dao.mongo_dao import MongoDao
from domain.Coin import Coin
from domain.Key import Key
from domain.PushData import PushData
from domain.Twitt import Twitt


class TwittCrawlService:
    def __init__(self):
        self.key = Key()
        self.dao = MongoDao()

    def parseTwittAll(self):
        coin_list = self.getCoinList()
        api = self.getTwittApi()

        for coin in coin_list:
            print('parse coin %s start' % coin.name_ko)
            last_twitt_time = self.getLastTwittTime(coin.screen_name)

            #print('1 : %s' % last_twitt_time)


            timeline_list = api.user_timeline(coin.screen_name)
            for timeline in timeline_list:
                twitt = Twitt(timeline._json, coin)
                #print('2 : %s' % twitt.created_date)
                if self.filterLastTwittDate(last_twitt_time, twitt.created_date):
                    break

                if self.filterDate(twitt.created_date):
                    break

                self.dao.openSession()
                self.dao.insertTwitt(twitt)
                self.dao.closeSession()
                print(twitt.text_ko)



    def getTwittApi(self):
        auth = tweepy.OAuthHandler(self.key.twitt_consumer_key, self.key.twitt_consumer_secret)
        auth.set_access_token(self.key.twitt_access_token, self.key.twitt_access_token_secret)
        api = tweepy.API(auth)
        return api

    def getCoinList(self):
        self.dao.openSession()
        db_coin_list = self.dao.getCoinList()
        coin_list = list()
        for item in db_coin_list:
            coin_list.append(Coin(item))
        self.dao.closeSession()
        return coin_list

    def filterLastTwittDate(self, last_twitt_date_str, date_str):
        if last_twitt_date_str is None:
            return False

        twitt_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        last_twitt_date = datetime.strptime(last_twitt_date_str, '%Y-%m-%d %H:%M:%S')
        gabDate = twitt_date - last_twitt_date
        #print('3 : %d' % gabDate.total_seconds())

        if gabDate.total_seconds() > 0:
            return False
        else:
            return True

    def filterDate(self, date_str):
        twitt_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        nowDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        nowDate = datetime.strptime(nowDate, '%Y-%m-%d %H:%M:%S')
        gabDate = nowDate - twitt_date
        if gabDate.days < 7:
            return False
        else:
            return True

    def getLastTwittTime(self, screen_name):
        self.dao.openSession()
        data_last_twitt = self.dao.getLastTwitt(screen_name)
        self.dao.closeSession()
        try:
            last_twitt = PushData(data_last_twitt)
        except Exception as e:
            return None

        return last_twitt.created_date
