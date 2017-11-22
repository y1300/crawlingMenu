import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '745de58055b542358617fe95ec945bc4',
}

params = urllib.parse.urlencode({
	'lang': 'en',
	'city': 'London',
	'limit': '0'
})

try:
    conn = http.client.HTTPSConnection('api.vivacityapp.com')
    conn.request("GET", "/test/internal/restaurant/list?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))