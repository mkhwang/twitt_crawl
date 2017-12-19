from googletrans import Translator
from datetime import datetime

import re
from pip._vendor.pyparsing import basestring


class Twitt:
    """
    tweet_id
    등록자Id
    원문
    번역
    등록시간
    """

    def __init__(self, json_data, coin_data=None):
        self.tweet_id = json_data['id_str']
        self.user_id = json_data['user']['screen_name']
        self.text_en = json_data['text']
        self.text_ko = ''
        self.name_ko = ''
        self.name_en = ''
        self.screen_name = ''

        if coin_data is not None:
            self.name_ko = coin_data.name_ko
            self.name_en = coin_data.name_en
            self.screen_name = coin_data.screen_name
            self.alias = coin_data.alias

        translator = Translator(service_urls=[
            'translate.google.com',
            'translate.google.co.kr',
        ])

        refine_text = self.remove_emoji(self.text_en)
        refine_text = self.remove_text_symbol(refine_text)
        temp_ko_text = ''
        try:
            temp_ko = translator.translate(refine_text, dest='ko')
            temp_ko_text = temp_ko.text
        except Exception as e:
            print('trans error : %s' % refine_text)
            temp_ko_text = '### 번역 에러 ###'


        self.text_ko = temp_ko_text

        temp_date = json_data['created_at']
        myDatetime = datetime.strptime(temp_date, '%a %b %d %H:%M:%S %z %Y')
        self.created_date = myDatetime.strftime('%Y-%m-%d %H:%M:%S')

    def remove_emoji(self, data):
        """
        去除表情
        :param data:
        :return:
        """
        if not data:
            return data
        if not isinstance(data, basestring):
            return data
        try:
            # UCS-4
            patt = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
        except re.error:
            # UCS-2
            patt = re.compile(
                u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
        return patt.sub('', data)

    def remove_text_symbol(self, data):
        return data.replace('\t', ' ').replace('amp;', '').replace('\r', '')
