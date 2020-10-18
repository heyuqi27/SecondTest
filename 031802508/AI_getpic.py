import requests
import 提交
url = "http://47.102.118.1:8089/api/challenge/start/faffa1cf-b298-452b-b469-d48f8ddf57a0"
payload ="   {\r\n        \"teamid\": 7,\r\n        \"token\": \"b91bda89-5d50-468b-beb5-2e58b9ff57c0\"\r\n   }"
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))

r_dic = 提交.loads(response.text)
dd = r_dic["data"]
print(dd['img'])
print(r_dic["uuid"])
