import discord # install[pip3 install discord.py]
import settings #
import asyncio
import datetime
import urllib.request, urllib.error
import json
from faker import Faker
from pymongo import MongoClient

q   = '0000'
que = 0
client = discord.Client() # 接続に使用するオブジェクト
fake = Faker("ja_jp")

# 起動時に通知してくれる処理
@client.event
async def on_ready():
    print('ログインしました')

# 「/neko」と発言したら「にゃーん」が返る処理
@client.event
async def on_message(message):
    own = str(message.author)
    global que
    global q
    if client.user.id in message.content and settings.ori==own: # 話しかけられたかの判定
        #reply = message.content.replace(settings.bot,"")
        reply = 'このあといいことあるよ！！いぇい！！'
        await client.send_message(message.channel, reply)
    elif message.content.startswith('/neko'):
        reply = 'にゃーん'
        await client.send_message(message.channel, reply)

    elif message.content.startswith('/1'):
        l = chk(1)
        if len(l) == 0:
            await client.send_message(message.channel, "月曜日のチェックする放送はありません。")
        else:
            for i in l:
                l[i]["h"]=str(int(l[i]["h"]))
                l[i]["m"]=str(int(l[i]["m"]))
                m="月曜日の{0:}時{1:}分に{2:}です。".format(l[i]["h"],l[i]["m"],l[i]["title"])
                await client.send_message(message.channel, m)

    elif message.content.startswith('/2'):
        l = chk(2)
        if len(l) == 0:
            await client.send_message(message.channel, "火曜日のチェックする放送はありません。")
        else:
            for i in l:
                l[i]["h"]=str(int(l[i]["h"]))
                l[i]["m"]=str(int(l[i]["m"]))
                m="火曜日の{0:}時{1:}分に{2:}です。".format(l[i]["h"],l[i]["m"],l[i]["title"])
                await client.send_message(message.channel, m)

    elif message.content.startswith('/3'):
        l = chk(3)
        if len(l) == 0:
            await client.send_message(message.channel, "水曜日のチェックする放送はありません。")
        else:
            for i in l:
                l[i]["h"]=str(int(l[i]["h"]))
                l[i]["m"]=str(int(l[i]["m"]))
                m="水曜日の{0:}時{1:}分に{2:}です。".format(l[i]["h"],l[i]["m"],l[i]["title"])
                await client.send_message(message.channel, m)

    elif message.content.startswith('/4'):
        l = chk(4)
        if len(l) == 0:
            await client.send_message(message.channel, "木曜日のチェックする放送はありません。")
        else:
            for i in l:
                l[i]["h"]=str(int(l[i]["h"]))
                l[i]["m"]=str(int(l[i]["m"]))
                m="木曜日の{0:}時{1:}分に{2:}です。".format(l[i]["h"],l[i]["m"],l[i]["title"])
                await client.send_message(message.channel, m)

    elif message.content.startswith('/5'):
        l = chk(5)
        if len(l) == 0:
            await client.send_message(message.channel, "金曜日のチェックする放送はありません。")
        else:
            for i in l:
                l[i]["h"]=str(int(l[i]["h"]))
                l[i]["m"]=str(int(l[i]["m"]))
                m="金曜日の{0:}時{1:}分に{2:}です。".format(l[i]["h"],l[i]["m"],l[i]["title"])
                await client.send_message(message.channel, m)

    elif message.content.startswith('/6'):
        l = chk(6)
        if len(l) == 0:
            await client.send_message(message.channel, "土曜日のチェックする放送はありません。")
        else:
            for i in l:
                l[i]["h"]=str(int(l[i]["h"]))
                l[i]["m"]=str(int(l[i]["m"]))
                m="土曜日の{0:}時{1:}分に{2:}です。".format(l[i]["h"],l[i]["m"],l[i]["title"])
                await client.send_message(message.channel, m)

    elif message.content.startswith('/7'):
        l = chk(7)
        if len(l) == 0:
            await client.send_message(message.channel, "日曜日のチェックする放送はありません。")
        else:
            for i in l:
                l[i]["h"]=str(int(l[i]["h"]))
                l[i]["m"]=str(int(l[i]["m"]))
                m="日曜日の{0:}時{1:}分に{2:}です。".format(l[i]["h"],l[i]["m"],l[i]["title"])
                await client.send_message(message.channel, m)

    elif message.content.startswith('/8'):
        t = metro()
        if t[0] == 'error':
            reply = 'にゃーん'
        else:
            tmp = "{0:}線の{1:}の時点の運行情報は{2:}に更新されていて、{3:}"
            reply = tmp.format("東西",t[0],t[1],t[2])
        await client.send_message(message.channel, reply)
            
    elif message.content.startswith('/9'):
        for i in range(5):
            w = Weather(0,i)
            reply = w.run()
            await client.send_message(message.channel, reply)

    elif message.content.startswith('/0'):
        for i in range(5):
            w = Weather(1,i)
            reply = w.run()
            await client.send_message(message.channel, reply)

    elif message.content.startswith('/d'):
        await client.send_message(message.channel, q)

    elif message.content.startswith('/r'):
        q=gen()
        #global que
        que=0
        await client.send_message(message.channel, q)

    elif message.content.startswith('/q'):
        #global que
        que+=1
        c=message.content.replace('/q ','')
        bulls=cows=0
        bc=[]
        if c==q:
            mess = str(que) + " done"
            q=gen()
            await client.send_message(message.channel, mess)
        else:
            for i in range(4):
                if c[i]==q[i]:
                    bulls+=1
                    bc.append(i)
            for i in range(4):
                for j in range(4):
                    if i!=j and j not in bc and i not in bc and c[i]==q[j]:
                        cows += 1
                        bc.append(j)
            mess=str(bulls)+" "+str(cows)
            await client.send_message(message.channel, mess)
            
      
        #await client.send_message(message.channel, c)
    #if client.user.id in message.content and settings.ori==own: # 話しかけられたかの判定
        #reply = message.content.replace(settings.bot,"")

def metro():
    ans=[]
    u = "https://api.tokyometroapp.jp/api/v2/datapoints?rdf:type=odpt:TrainInformation&acl:consumerKey="
    t = settings.met
    a = urllib.request.urlopen(u+t)
    b = a.read()
    c = b.decode('utf_8')
    d = json.loads(c)
    for i in d:
        if i["odpt:railway"] == "odpt.Railway:TokyoMetro.Tozai":
        #if i["odpt:railway"] == "odpt.Railway:TokyoMetro.Chiyoda":
            ans.append(i["dc:date"].replace("+09:00",""))
            ans.append(i["odpt:timeOfOrigin"].replace("+09:00",""))
            ans.append(i["odpt:trainInformationText"])
            return ans
    return ("error",)

def jg(j):
    moc=settings.moc
    mot=settings.mot
    try:
        e=[]
        i=j.read()
        x = json.loads(i)
        if len(x)!=5: e[5]=5
        if len(x['title'])==0: e[5]=5
        if 0<=int(x['w'])<7: e[5]=5
        if 0<=int(x['h'])<24: e[5]=5
        if 0<=int(x['m'])<60: e[5]=5
        if 0<=int(x['p'])<2: e[5]=5
        client = MongoClient(moc,mot)
        db = client["anime"]
        db.authenticate(settings.mou,settings.mop)
        k = db.anime.find({'title':x['title']})
        for i in k:
            if i['title']==x['title'] and i['w']==x['w'] and i['h']==x['h'] and i['m']==x['m'] and i['p']==x['p']:
                return "登録しました。"
        return "登録に失敗したかもしれません。" 
    except:
        return "不正なフォーマットの可能性があるため登録を実行しません。。。"

def gen():
    seed = '0123456789'
    ret  = ''
    for i in range(4):
        o = datetime.datetime.now()
        ret += str(seed[o.microsecond%10])
    return ret

def chk(i):
    moc=settings.moc
    mot=settings.mot
    d={}
    client = MongoClient(moc,mot)
    db = client["anime"]
    db.authenticate(settings.mou,settings.mop)
    k = db.anime.find({"w":i-1})
    for a,i in enumerate(k):
        d[a]=i
    return d        

    

class Weather:
    def __init__(self, flag, todo):
        self.flag = flag
        self.todo = todo
        self.target = [['東京都内', '13'], ['千葉北西部','12'], ['熊本地方','43'], ['京都南部','26'],['宮城西部','04']]
        self.code = self.target[self.todo][1]
        self.area= self.target[self.todo][0]

    def get_json(self):
        url = 'http://www.drk7.jp/weather/json/' + self.code + '.js'
        res = urllib.request.urlopen(url)
        nama = res.read()
        nama8 = nama.decode('utf_8')
        nama8=nama8.replace("drk7jpweather.callback(","").replace(");","")
        j = json.loads(nama8)
        return j


    def get_info(self):
        l = []
        data = self.get_json()
        area  = ['東京地方', '北西部', '熊本地方', '南部', '西部']
        l.append(data['pref']['area'][area[self.todo]]['info'][self.flag]['weather'])
        l.append(data['pref']['area'][area[self.todo]]['info'][self.flag]['temperature']['range'][0]['content'])
        l.append(data['pref']['area'][area[self.todo]]['info'][self.flag]['temperature']['range'][1]['content'])
        for p in range(4):
            l.append(data['pref']['area'][area[self.todo]]['info'][self.flag]['rainfallchance']['period'][p]['content'])
        return l


    def make_text(self):
        d = self.get_info()
        temp = "{0:}の{1:}ら辺の天候は{2:}です。最高気温は{3:}度くらいで、最低気温は{4:}度くらい。降水確率は6時間区切りで{5:}, {6:}, {7:}, {8:}です。"
        text = temp.format(['今日','明日'][self.flag], self.area, d[0], d[1], d[2], d[3], d[4], d[5], d[6])
        return text

    def run(self):
        m = self.make_text()
        return m

async def my_background_task():
    await client.wait_until_ready()
    counter = 0
    channel = discord.Object(id=settings.ani)
    while not client.is_closed:
        t = datetime.datetime.now()
        u = "http://www.nowshika.com/joso/dummy.json"
        a = urllib.request.urlopen(u)
        b = a.read()
        c = b.decode('utf_8')
        d = json.loads(c)
        if t.hour == 0 and t.minute<15:
            res = []
            l   = d["anime"]
            for i in l:
                if i["w"] == t.weekday():
                    res.append(i["title"])
            if len(res) == 0:
                m = "今日のチェックする放送はありません"
            else:
                x = ", ".join(res)
                m = "今日のチェックする放送は" + x
            await client.send_message(channel, m)
        elif t.hour%8==0 and t.minute<15:
            #a="定期更新"
            a=fake.sentence()
            await client.send_message(channel, a)
        #else:
        #    a="10分更新"
        #    await client.send_message(channel, a)
        await asyncio.sleep(900) # task runs every 60 seconds



# botの接続と起動
# （tokenにはbotアカウントのアクセストークンを入れてください）
client.loop.create_task(my_background_task())
client.run(settings.tkn)
