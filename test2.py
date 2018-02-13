import pymongo
import json



if __name__ == '__main__':
    client = pymongo.MongoClient('14.0.92.40', 27017)

    coin_list = client.etc['coin'].find({},{'_id':0})
    client.close()

    json_list = list()
    for coin in coin_list:
        json_list.append(json.dumps(coin))

    for temp in json_list:
        temp = str(temp).encode('utf-8')
        print(temp)
        temp = temp.decode('utf-8')
        print(temp)

