import requests, urllib.parse, json
from pprint import pprint

class restaurantDetail:

    # paras = {
    #       'city': name of the city,
    #       'limit': limit number of returns (0 = no limit)
    # }
    def __init__(self, id):

        self.headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': '745de58055b542358617fe95ec945bc4'
        }

        # self.params = urllib.parse.urlencode({
        # 	'id' : id
        # })

        self.id = id


    def extract(self):
        try:
            url = 'https://api.vivacityapp.com/test/internal/restaurant/detailed/%s' % self.id
            # print(url)
            response = requests.get(url, headers=self.headers)
            data = [response.json()]
            # pprint(data)

            output = []
            # for each restaurant in lists returned
            for d in data:
                try:
                    output.append((d['id'], d['name'], d['socialMedia']['url']))
                except:
                    output.append((d['id'], d['name'], None))
            return output

        except Exception as e:
            # print("[Errno {0}] {1}".format(e.errno, e.strerror))
            print(e)
            return None