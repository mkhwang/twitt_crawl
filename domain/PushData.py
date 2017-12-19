class PushData:
    def __init__(self, json_data):
        self.pushed = json_data['pushed']
        self.text_en = json_data['textEn']
        self.text_ko = json_data['textKo']
        self.alias = json_data['alias']
        self.name_ko = json_data['nameKo']
        self.name_en = json_data['nameEn']
        self.screen_name = json_data['screenName']
        self.created_date = json_data['createdDate']
        self.twitt_id = json_data['twittId']

    def getPushMessage(self):
        msg = '[ %s(%s) ]\n%s\n\n원문 : %s\n등록일시 : %s' % (
            self.name_ko, self.alias, self.text_ko, self.text_en, self.created_date)
        attachment_dic = dict()
        attachment_dic['text'] = msg
        attachments = [attachment_dic]
        return attachments