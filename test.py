from datetime import datetime

import tweepy
from googletrans import Translator
from slacker import Slacker

import re
import json

from pip._vendor.pyparsing import basestring

class Twitt:
    """
    tweet_id
    등록자Id
    내용
    원문
    번역
    링크
    등록시간
    """
    def __init__(self, json_data):
        self.tweet_id = json_data['id_str']
        self.user_id = json_data['user']['screen_name']
        self.en_text = json_data['text']
        self.ko_text = ''

        translator = Translator(service_urls=[
            'translate.google.com',
            'translate.google.co.kr',
        ])

        refine_text = self.remove_emoji(self.en_text)
        refine_text = self.remove_text_symbol(refine_text)
        temp_ko_text = ''
        try:
            temp_ko_text = translator.translate(refine_text, dest='ko')
        except Exception as e:
            print(refine_text)

        self.ko_text = temp_ko_text.text

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
        return data.replace('\t', ' ').replace('\n', '').replace('amp;', '').replace('\r', '')


def remove_emoji(data):
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
        patt = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
    return patt.sub('', data)

def remove_text_symbol(data):
    return data.replace('\t', ' ').replace('\n', '').replace('amp;', '').replace('\r', '')

if __name__ == '__main__':
    consumer_key = '7F4N1XguAMQ3POMA7o3rl1jQc'
    consumer_secret = '8tt0HtVfOGLEJxgIwLQzLjiTuUsPTGEPEJKDwOjrsSZa9A1Y1P'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    access_token = "942576960584089605-bzkkjQyeFlYAHMTK9GoxLKVj3CB32ez"
    access_token_secret = "HWUTrSeRH6mPlUDHNTtFFev0SkSWn3w6DLJVWXhycX4VX"
    auth.set_access_token(access_token, access_token_secret)

    slack_token = 'xoxp-288923356646-287398388752-288665799876-14e85e2d44b439fe857229738cf4622a'
    slack = Slacker(slack_token)


    # twitter API 생성
    api = tweepy.API(auth)

    id_list = list()
    id_list.append('Dashpay')
    id_list.append('Ripple')
    id_list.append('ethereumproject')
    id_list.append('einsteiniumcoin')
    id_list.append('NxtCommunity')

    translator = Translator(service_urls=[
        'translate.google.com',
        'translate.google.co.kr',
    ])


    for id in id_list:
        timelines = api.user_timeline(id)
        print(id)
        seq = 1
        for tweet in timelines:
            temp2 = tweet._json
            twitt_obj = Twitt(temp2)
            print(twitt_obj.tweet_id)
            print(twitt_obj.user_id)
            print('%s > %s' % (twitt_obj.en_text, twitt_obj.ko_text))
            print(twitt_obj.created_date)
            msg = '[ %s ]\n %s\n 원문 : %s\n 등록일시 : %s' % (twitt_obj.user_id, twitt_obj.ko_text, twitt_obj.en_text, twitt_obj.created_date)
            attachment_dic = dict()
            attachment_dic['text'] = msg
            attachments = [attachment_dic]
            slack.chat.post_message('#general', text=None, attachments=attachments, as_user=True)
            print('#####################################################')
            seq += 1
            if seq > 5:
                break



