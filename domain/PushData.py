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