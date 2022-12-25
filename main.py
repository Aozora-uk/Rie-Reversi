"""
The MIT License (MIT)

Copyright (c) 2015 bpyamasinn.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import subprocess
import asyncio
import json
import datetime
import os
import websockets
import re
import uuid
from subprocess import PIPE
from misskey import Misskey

TOKEN = "INPUT YOUR TOKEN HERE"    # トークンを入力
instance = "misskey.example.com"    #ドメインを入力


msk = Misskey(instance, i=TOKEN)
cwd = os.getcwd()
MY_ID = msk.i()["id"]
WS_URL = "wss://" + instance + "/streaming?i=" + TOKEN
myuuid = str(uuid.uuid4())
_level = "21"    #難易度0〜60 あまり上げすぎると止まる
mfmheader = "\n\n$[x3 $[x3 :_BOARD:]]\n\\(\\\\[-16.88em]\\kern{3.85em}\)<small>"
mfmfooter = "}\\\\[-20em]\\kern{-2em}\\)$[x3 $[x3 :blank:]]\\(\\\\[0em]\\kern{13em}\\)$[font.fantasy AiReversi alpha 1]"


async def runner():
 async with websockets.connect(WS_URL) as ws:
  await ws.send(json.dumps({
   "type": "connect",
   "body": {
     "channel": "main",
     "id": myuuid
   }
  }))
  while True:
    data = json.loads(await ws.recv())
    if (data['type'] == 'channel' and data['body']['type'] == 'mention'):
      try:
        a = data["body"]["body"]["reply"]["text"]
        if (data["body"]["body"]["user"]["id"] in a and not ("finished" in a)):
          await play(data)
        elif ("AiReversi" in a) :
          msk.notes_create(text="ここには返信できませんよ！", reply_id=data["body"]["body"]['id'])
      except KeyError:
        if (data['body']['type'] == 'mention'):
          if (re.search(r'リバーシ|オセロ|Reversi|Othello|reversi|othello', data["body"]["body"]["text"])):
            await newgame(data)


async def talk(replyid,status):
  #print("stdtalk!")
  if (status == "owari"):
    msk.notes_create(text="わかりました。", reply_id=replyid)


async def newgame(data):
  note = data['body']['body']
  if note.get('mentions'):
    if MY_ID in note['mentions']:
      text = note['text']
      lev = re.search(r"(level) (\d+)", text)
      try:
        lev = str(lev).split("match='level ")[1].split("'>")[0]
      except :
        lev = _level
      if (re.search(r'先|first|First', text)):
        ai_first = "no"
        aianswer = subprocess.run(['bash', cwd+'/ai.sh', lev, "", "", ""], stdout=PIPE, text=True)
      else :
        ai_first = "yes"
        aianswer=subprocess.run(['bash', cwd+'/ai.sh', lev, "new", "go", ""], stdout=PIPE, text=True)

      reply = aiprocessor(aianswer)
    

      reply = "良いですよ～"+mfmheader+reply+"\\phantom{level="+lev+",user="+note["user"]["id"]+",ai_first="+ai_first+",start="+(datetime.datetime.now().strftime("%Y:%m:%d:%T"))+mfmfooter
      msk.notes_create(text=reply, reply_id=note['id'])



def aiprocessor(aianswer):
  disks=""
  reply=""
  disknum=0
  aianswer = aianswer.stdout.replace('.','#')
  for i in aianswer:
    if (i == "O" or i == "X" or i == "#"):
        disks += i

  disks = disks[-64:]
  for i in range(64):
    disknum+=1
    reply += disks[i]
    if (disknum % 8 == 0 and disknum != 64):
      reply += "</small>\\(\\\\[0.05em]\\kern{3.85em}\\)<small>"
  reply += "</small>\("
  reply = reply.replace('O',":_Wh:")
  reply = reply.replace('X',":_Bl:")
  reply = reply.replace('#',":blank:")

  return(reply)


  
async def play(data):
  note = data["body"]["body"]
  text = data["body"]["body"]["text"]
  replytext = note["reply"]["text"]
  bordstext = replytext.split("_BOARD")[1].split("\\(\\phantom")[0]
  bords = ""
  bordstext = bordstext.replace(":blank:", "#")
  bordstext = bordstext.replace(":_Bl:","X")
  bordstext = bordstext.replace(":_Wh:","O")
  for l in bordstext:
    if (l == "X"):
      bords += "X"
    elif (l == "O"):
      bords += "O"
    elif (l == "#"):
      bords += "-"
  print(len(bords))
  print(bords)
  lev = replytext.split("level=")[1]
  lev = lev.split(",user=")[0]
  ai_first = replytext.split(",ai_first=")[1]
  ai_first = ai_first.split(",start=")[0]
  startdate = replytext.split(",start=")[1]
  startdate = startdate.split(mfmfooter)[0]
  if (re.search(r'やめる|投了|リタイ|終|おわり|止|あきらめ|諦|Stop|STOP|stop', text)):
    await talk(data["body"]["body"]["id"],"owari")
    return(0)
  elif (re.search(r'パス|ﾊﾟｽ|Pass|pass|PASS|飛', text)):
    if (ai_first == "yes"):
      bords += "X"
    else :
      bords += "O"
    aianswer = subprocess.run(['bash', cwd+'/ai.sh', lev, "setboard "+bords, "go", ""], stdout=PIPE, stderr=PIPE, text=True)
    phrase = "パスですか?わかりました。"
  else :
    if (ai_first == "yes"):
      bords += "O"
    else :
      bords += "X"
    text = text.replace("@ai@"+instance,"")
    text = text.replace("@ai","")
    playtext = ""
    for i in text:
      if (i in ["A","B","C","D","E","F","G","H","a","b","c","d","e","f","g","h"]):
        playtext = i
        break
    for j in text:
      if (j in ["1","2","3","4","5","6","7","8"]):
        playtext += j
        break
    if (len(playtext)!=2):
      aianswer = subprocess.run(['bash', cwd+'/ai.sh', lev, "setboard "+bords, "", ""], stdout=PIPE, stderr=PIPE, text=True)
      phrase = "`A2` みたいなかんじで場所を教えてください\nパスといえばパスできますよ♪"
    else :
      aianswer = subprocess.run(['bash', cwd+'/ai.sh', lev, "setboard "+bords, "play "+playtext, "go"], stdout=PIPE, stderr=PIPE, text=True)
      phrase = "どうぞ!"
  aianswer_out = aiprocessor(aianswer)
  if (not "ERROR" in aianswer.stderr):
    reply = phrase+mfmheader+aianswer_out+"\\phantom{level="+lev+",user="+note["user"]["id"]+",ai_first="+ai_first+",start="+startdate+mfmfooter
  elif ("game over" in aianswer.stderr):
    blackdisc = aianswer_out.count("\\):_Bl:\\( ")
    whitedisc = aianswer_out.count("\\):_Wh:\\( ")
    if (blackdisc == whitedisc):
      phrase = "引き分けでした"
    elif ((blackdisc < whitedisc and ai_first == True) or (blackdisc > whitedisc and ai_first == False)):
      phrase = "負けちゃいました..."
    else :
      phrase = "藍の勝ちです！"
    reply = str(blackdisc)+"対"+str(whitedisc)+"で"+phrase+mfmheader+aianswer_out+"\\phantom{finished,level="+lev+",user="+note["user"]["id"]+",ai_first="+ai_first+",start="+startdate+mfmfooter
  elif ("invalid move" in aianswer.stderr):
    reply = "そこには置けないみたいです:woozy_ai:\n\n"+data["body"]["body"]["reply"]["text"].split("\n\n")[1]
  else :
      reply = "エラーです！コード:"+aianswer.stderr
  msk.notes_create(text=reply, reply_id=note['id'])

asyncio.get_event_loop().run_until_complete(runner())

