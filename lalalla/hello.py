import requests
res = requests.get("http://baidu.com")
f = open("baidu.txt", "a")
f.write(res.content)
f.close()
print "I will write the source codes of baidu.com into the file named baidu.txt"
print "I will write the source codes of baidu.com into the file named baidu.txt"
print "I will write the source codes of baidu.com into the file named baidu.txt"
