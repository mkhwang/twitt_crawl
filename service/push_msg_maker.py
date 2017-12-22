from dao.mongo_dao import MongoDao


class MessageMaker:
    def __init__(self, push_data):
        self.push_data = push_data

    def makeSlackMsg(self):
        msg = '%s\n\n번역 : %s\n등록일시 : %s' % (self.push_data.text_en, self.push_data.text_ko, self.push_data.created_date)
        attachment_dic = dict()
        attachment_dic['text'] = msg
        attachment_dic['title'] = '[ %s(%s) ]' % (self.push_data.name_ko, self.push_data.alias)
        attachment_dic['title_link'] = self.getTwittUrl()
        attachments = [attachment_dic]
        return attachments

    def getTwittUrl(self):
        dao = MongoDao()
        dao.openSession()
        result = dao.getCoinData(self.push_data.screen_name)
        dao.closeSession()
        return result[0]['twittUrl']