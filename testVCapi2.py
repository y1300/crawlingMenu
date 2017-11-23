import requests, urllib.parse, json
from pprint import pprint

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '745de58055b542358617fe95ec945bc4'
}

params = urllib.parse.urlencode({
	'lang': 'en',
	'city': 'London',
	'limit': '0'
})

try:
    url = 'https://api.vivacityapp.com/test/internal/restaurant/list?%s' % params
    # print(url)
    response = requests.get(url, headers=headers)
    data = response.json()
    # pprint(data)

    # for each restaurant in lists returned
    for d in data:
        print(d['id'], d['name'])
        try:
            print(d['socialMedia']['url'])
        except:
            print('no Website')

except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))