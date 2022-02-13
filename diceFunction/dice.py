# ダイスロール要求dictを受け取り、その結果を返すプログラムを作るぞ！

# 正規表現を使用する
import re
# ランダム処理を使用する
import random
# 自作の関数をインポート
from create_dPara import create_dPara
from diceroll import diceroll
# まだ使いこなせていないlogger機能…。
from logging import getLogger, FileHandler, DEBUG, StreamHandler, INFO, Formatter 
logger = getLogger(__name__)





# 文字列データとして'〇d☆'もしくは'choice'を入力する。
# selectDice = 'choice'
selectDice = '1d100'
# d100を10面ダイス×2(calc)で行うか、100面ダイス×1(simple)で行うか。
d100Pattern = 'calc'
# ボーナスダイスもしくはペナルティダイスの数。
# プラスがボーナス扱いでマイナスがペナルティ扱い。
bp = 0
# choiceするリスト
rdmList = ['hoge','fuga','piyo','foo','bar']






# ダイスの状態を取得する。
dPara = create_dPara(selectDice,d100Pattern,bp,rdmList)

# ダイス結果リスト
diceRollList=[]

# 要求された回数分、ダイスを振る。
for i in range(1,dPara['diceCount']+1):

    diceResult = diceroll(dPara)
    diceRollList.append(diceResult['value'])
    # 毎回の詳細なロール結果を見たければこのprintを生かす。
    print(diceResult)

# 折角なので合計値をつくる。
diceRollListSum = sum(diceRollList)

# choiceか否かで最後の表示を変える。
if dPara['diceType'] == 'choice':
    print('choice {} => {}'.format(dPara['rdmList'],diceRollList))
elif not dPara['diceType'] == 'choice':
    print('{} d {} => {} Total「{}」'.format(dPara['diceCount'],dPara['diceType'],diceRollList,diceRollListSum))
