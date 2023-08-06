from requestQ import item as it,fetch,Case,Cases

a=it('test1',fetch("https://paytest.ciicsh.com/auth/authenticate/login", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=UTF-8",
    "pragma": "no-cache",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "signstr": "ea35510c9ec9a98ded6f681732875df5",
    "timestamp": "1597801739559",
    "token": ""
  },
  "referrer": "https://paytest.ciicsh.com/login?redirect=%2FsalaryMgr%2FcomputeSearch",
  "referrerPolicy": "no-referrer-when-downgrade",
  "body": "{\"userId\":\"13800920000\",\"password\":\"AAAaaa111\"}",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
}))
b=it('test2',fetch("https://paytest.ciicsh.com/auth/authenticate/login1", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=UTF-8",
    "pragma": "no-cache",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "signstr": "ea35510c9ec9a98ded6f681732875df5",
    "timestamp": "1597801739559",
    "token": ""
  },
  "referrer": "https://paytest.ciicsh.com/login?redirect=%2FsalaryMgr%2FcomputeSearch",
  "referrerPolicy": "no-referrer-when-downgrade",
  "body": "{\"userId\":\"13800920000\",\"password\":\"AAAaaa111\"}",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
}))
c=it('test3',fetch("https://paytest.ciicsh.com/auth/authenticate/login", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=UTF-8",
    "pragma": "no-cache",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "signstr": "ea35510c9ec9a98ded6f681732875df5",
    "timestamp": "1597801739559",
    "token": ""
  },
  "referrer": "https://paytest.ciicsh.com/login?redirect=%2FsalaryMgr%2FcomputeSearch",
  "referrerPolicy": "no-referrer-when-downgrade",
  "body": "{\"userId\":\"13800920000\",\"password\":\"AAAaaa111\"}",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
}))
# Case('ceshi2',a).run()
c=Cases(Case('ceshi2',a,b,c))
# print(c.step)
# print(c.res)
# print(c.detail)
# print(c.run_info)
# print(c.id_dict)

