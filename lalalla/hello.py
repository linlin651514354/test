import requests
res = requests.get("http://baidu.com")
f = open("baidu.txt", "a")
f.write(res.content)
f.close()
