import requests
import json
import datetime
# from pprint import pprint
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4395.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest'
}

root_url = 'https://yqtb.sut.edu.cn'
login_url = 'https://yqtb.sut.edu.cn/login'

def login(username, password):
    login_data = json.dumps( {'user_account': username, 'user_password': password})
    s = requests.Session()

    login_reply = s.post(login_url, data=login_data, headers=headers, verify=False)

    login_result = json.loads(login_reply.content)

    if(login_result['code'] != 200):
        print('Login Failed')
        exit()

    s.cookies = login_reply.cookies
    return s
    
def getForm(day, session):
    url = root_url + '/getPunchForm'
    datas = json.dumps({'date': day})
    
    res = session.post(url, data=datas, headers=headers)
    res_json = json.loads(res.content)

    if(res_json['code'] == 200):
        return res_json['datas']
    else:
        return None


def punchForm(form, session):
    url = root_url + '/punchForm'
    date = datetime.datetime.now() + datetime.timedelta(days=1)
    datestr = date.strftime("%Y-%m-%d")
    
    print(datestr)
    
    datas_dict = {
        'punch_form': json.dumps(form),
        'date': datestr
    }
    datas = json.dumps(datas_dict)
    # print(datas)

    res = session.post(url, data=datas, headers=headers)
    res_json = json.loads(res.content)
    print(res_json)
    headers9={'Content-Type':'application/x-www-form-urlencoded'}
    url9='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=SL5CvrTkoZWOP_7Hlingq1ci8xAyKfzIwy2d1cWeqJQ' #填你自己的key，想发到群里的把send改成group。
    message9='夫祸患常积于忽微，而智勇多困于所溺！【每日健康提醒】'+str(res_json)+' 加油奥利给！！[嘿哈][嘿哈] ' #想发送啥消息自己改
    text={ "content":message9}
    data9={
           "touser" : "@all",
           "toparty" : "PartyID1|PartyID2",
           "totag" : "TagID1 | TagID2",
           "msgtype" : "text",
           "agentid" : 1000002,
           "text" : {
               "content" : '程序已运行，'+message9+'\n可查看<a href=\"https://yqtb.sut.edu.cn\">沈阳工业大学健康打卡系统</a>，避免漏签。'
           },
           "safe":0,
           "enable_id_trans": 0,
           "enable_duplicate_check": 0,
           "duplicate_check_interval": 1800
         }
    re=requests.post(url=url9,headers=headers9,data=json.dumps(data9))
    print(re.json())

def submit(username, password, address, params=None):
    s = login(username, password)
    # result = s.post(root_url + '/getHomeDate', headers=headers)

    today = datetime.date.today().strftime('%Y-%m-%d')
    form_dict = getForm(today, s)

    fields = form_dict['fields']
    form = { dict['field_code']: dict['user_set_value'] for dict in fields }
    
    for key, value in params.items():
        if not value:
            value = 'null'
        form[key] = value
    
    if address != "":
        form['zddw'] = address

    punchForm(form, s)
