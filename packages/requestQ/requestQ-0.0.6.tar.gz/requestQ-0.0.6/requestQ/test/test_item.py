from requestQ import item,Case,fetch,raw
a=[]
# for i in range(13800960320,13800960321):
#     a.append(item(str(i),fetch("https://paytest.ciicsh.com/auth/authenticate/register", {
#     "headers": {
#         "accept": "application/json, text/plain, */*",
#         "accept-language": "zh-CN,zh;q=0.9",
#         "cache-control": "no-cache",
#         "content-type": "application/json;charset=UTF-8",
#         "pragma": "no-cache",
#         "sec-fetch-dest": "empty",
#         "sec-fetch-mode": "cors",
#         "sec-fetch-site": "same-origin"
#     },
#     "referrer": "https://paytest.ciicsh.com/register",
#     "referrerPolicy": "no-referrer-when-downgrade",
#     "body": "{\"companyName\":\""+str(i)+"\",\"corporationName\":\"123\",\"socialUnifiedCreditCode\":\"123\",\"businessRegistrationNumber\":\"\",\"taxIdentificationNumber\":\"\",\"orgCode\":\"\",\"scaleEnterprise\":3,\"classification\":7,\"authType\":\"2\",\"phone\":\""+str(i)+"\",\"password\":\"AAAaaa111\",\"code\":\"138009\"}",
#     "method": "POST",
#     "mode": "cors",
#     "credentials": "omit"
#     })))
# Case('1',*a).run()
for i in range(8,60):
#     a.append(item(str(i),raw('''
#     POST https://hkgentai-test.ciicsh.com/background/api/cm/CfgHospital/Add?_rnd=0.5949009795839972 HTTP/1.1
# Host: hkgentai-test.ciicsh.com
# Connection: keep-alive
# Content-Length: 131
# Pragma: no-cache
# Cache-Control: no-cache
# Accept: application/json, text/plain, */*
# Authorization: bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbklkIjoiYWRtaW4ifQ.oqj7tBXezWssOkGWJFYAtvYhVj5xs60q7HMsYHJ28L8
# User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36
# Content-Type: application/json
# Origin: https://hkgentai-test.ciicsh.com
# Sec-Fetch-Site: same-origin
# Sec-Fetch-Mode: cors
# Sec-Fetch-Dest: empty
# Referer: https://hkgentai-test.ciicsh.com/
# Accept-Encoding: gzip, deflate, br
# Accept-Language: zh-CN,zh;q=0.9

# {"updatedTime":null,"updatedBy":null,"id":null,"enabled":null,"hospitalName":"%s","createdTime":null,"initial":"%s","createdBy":null}
#     ''' % (str(i),str(i)))))
    a.append(item(str(i),fetch("https://hkgentai-test.ciicsh.com/background/api/cm/CfgType/Add?_rnd=0.34155027261529103", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "authorization": "bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpbklkIjoiYWRtaW4ifQ.oqj7tBXezWssOkGWJFYAtvYhVj5xs60q7HMsYHJ28L8",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "pragma": "no-cache",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://hkgentai-test.ciicsh.com/",
  "referrerPolicy": "no-referrer-when-downgrade",
  "body": "{\"children\":null,\"id\":null,\"productSeriesId\":\"85433ebc-cc56-4506-b583-4e597d117248\",\"ftypeNo\":\"001.001.001\",\"typeNo\":\"001.001.001.00"+str(i)+"\",\"productSeriesName\":\"2323233干要不果z中u然\",\"typeName\":\""+str(i)+"\"}",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
})))
Case('1',*a).run()

