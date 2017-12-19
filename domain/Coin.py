class Coin:
    """
    screen_name
    name_ko
    name_en
    alias
    twitt_url
    rank
    """
    def __init__(self, data):
        print(data)
        self.screen_name = data['screenName']
        self.name_ko = data['name_ko']
        self.name_en = data['name_en']
        self.alias = data['alias']
        self.twitt_url = data['twittUrl']
        self.rank = data['rank']
