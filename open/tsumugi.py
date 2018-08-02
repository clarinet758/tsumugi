import discord # install[pip3 install discord.py]
import settings #
import asyncio
import datetime
import urllib.request, urllib.error
import json


client = discord.Client() # 接続に使用するオブジェクト

# 起動時に通知してくれる処理
@client.event
async def on_ready():
    print('ログインしました')

# 「/neko」と発言したら「にゃーん」が返る処理
@client.event
async def on_message(message):
    if message.content.startswith('/neko'):
        reply = 'にゃーん'
        await client.send_message(message.channel, reply)

    elif message.content.startswith('/1'):
        for i in range(5):
            w = Weather(0,i)
            reply = w.run()
            await client.send_message(message.channel, reply)

    elif message.content.startswith('/2'):
        for i in range(5):
            w = Weather(1,i)
            reply = w.run()
            await client.send_message(message.channel, reply)

    elif message.content.startswith('/8'):
        t = metro()
        if t[0] == 'error':
            reply = 'にゃーん'
        else:
            tmp = "{0:}線の{1:}の時点の運行情報は{2:}に更新されていて、{3:}"
            reply = tmp.format("東西",t[0],t[1],t[2])
        await client.send_message(message.channel, reply)
            

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
        elif t.hour%4==0 and t.minute<0:
            a="定期更新"
            await client.send_message(channel, a)
        #else:
        #    a="10分更新"
        #    await client.send_message(channel, a)
        await asyncio.sleep(900) # task runs every 60 seconds



# botの接続と起動
# （tokenにはbotアカウントのアクセストークンを入れてください）
client.loop.create_task(my_background_task())
client.run(settings.tkn)
