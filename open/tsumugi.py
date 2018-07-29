import discord # install[pip3 install discord.py]
import settings #
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
        target = [['東京都内', '13'], ['千葉北西部','12'], ['熊本地方','43'], ['京都南部','26'],['宮城西部','04']]
        for a,i in enumerate(target):
            w = Weather(0,a,i[1],i[0])
            reply = w.run()
            await client.send_message(message.channel, reply)

    elif message.content.startswith('/2'):
        target = [['東京都内', '13'], ['千葉北西部','12'], ['熊本地方','43'], ['京都南部','26'],['宮城西部','04']]
        for a,i in enumerate(target):
            w = Weather(1,a,i[1],i[0])
            reply = w.run()
            await client.send_message(message.channel, reply)

class Weather:
    def __init__(self, flag, todo, code, area):
        self.flag = flag
        self.todo = todo
        self.code = code
        self.area = area

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




# botの接続と起動
# （tokenにはbotアカウントのアクセストークンを入れてください）
client.run(settings.tkn)
