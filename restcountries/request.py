import http.client
import json

conn = http.client.HTTPSConnection('restcountries.com')

conn.request('GET', '/v3.1/all')

res = conn.getresponse()
json_bytes = res.read()

json_string = json_bytes.decode('utf-8')

try:
    data = json.loads(json_string)
except json.JSONDecodeError:
    print("The JSON is not valid.")
    data = None

if data is not None:
    with open(r'C:\Users\scott\OneDrive\Documents\CMP419\Part_2\Assessment\restcountries\rest-countries.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
else:
    print("Failed to save JSON data due to decoding issues.")
