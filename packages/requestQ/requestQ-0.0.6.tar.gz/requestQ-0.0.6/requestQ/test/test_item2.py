from requestQ import item,DoRequest,fetch

item('1',fetch("https://paytest.ciicsh.com/auth/authenticate/login", {
  "headers": {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=UTF-8",
    "pragma": "no-cache",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "signstr": "02c8a08f5b914599451300ef10177575",
    "timestamp": "1598508409373",
    "token": ""
  },
  "referrer": "https://paytest.ciicsh.com/login?redirect=%2Femployee%2FempAdd",
  "referrerPolicy": "no-referrer-when-downgrade",
  "body": "{\"userId\":\"13800950094\",\"password\":\"AAAaaa111\"}",
  "method": "POST",
  "mode": "cors",
  "credentials": "omit"
})).expect('data.code').toBe(0).debug(DoRequest())