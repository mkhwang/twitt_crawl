import pymongo


class MongoDao:
    def openSession(self):
        self.client = pymongo.MongoClient('14.0.92.40', 27017)

    def closeSession(self):
        self.client.close()

    def insertTwitt(self, twitt):
        self.client.etc['twitt'].insert(
            {
                'twittId': twitt.tweet_id,
                'screenName': twitt.screen_name,
                'nameKo': twitt.name_ko,
                'nameEn': twitt.name_en,
                'textEn': twitt.text_en,
                'textKo': twitt.text_ko,
                'createdDate': twitt.created_date,
                'alias': twitt.alias,
                'pushed': 0
            }
        )

    def updateTwiitPush(self, tweet_id):
        self.client.etc['twitt'].update(
            {
                'twittId': str(tweet_id)
            }, {
                '$set': {'pushed': 1}
            }
            , multi=True
        )

    def getPushTargetTwitt(self):
        return self.client.etc['twitt'].find({'pushed': 0})

    def getCoinList(self):
        return self.client.etc['coin'].find()

    def getLastTwitt(self, screen_name):
        return self.client.etc['twitt'].find_one({'screenName': screen_name}, sort=[("createdDate", pymongo.DESCENDING)])