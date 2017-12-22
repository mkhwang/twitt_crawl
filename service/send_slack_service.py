from slacker import Slacker

from dao.mongo_dao import MongoDao
from domain.Key import Key
from domain.PushData import PushData
from service.push_msg_maker import MessageMaker


class SlackPushService:
    def __init__(self):
        self.key = Key()
        self.dao = MongoDao()

    def pushSlack(self):
        push_list = self.getPushData()
        slack = Slacker(self.key.slack_token)
        channel = '#' + self.key.slack_channel

        for push in push_list:
            maker = MessageMaker(push)
            slack.chat.post_message(channel, text=None, attachments=maker.makeSlackMsg(), as_user=True)
            self.updatePushComplete(push)

    def getPushData(self):
        self.dao.openSession()
        db_push_list = self.dao.getPushTargetTwitt()
        self.dao.closeSession()
        push_list = list()

        for db_push in db_push_list:
            push_list.append(PushData(db_push))

        return push_list

    def updatePushComplete(self, push):
        self.dao.openSession()
        self.dao.updateTwiitPush(push.twitt_id)
        self.dao.closeSession()
