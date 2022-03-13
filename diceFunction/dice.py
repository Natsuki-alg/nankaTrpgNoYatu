import argparse
import re
# 自作の関数をインポート
from create_dPara import create_dPara
from diceroll import diceroll
from dbc2sbc import dbc2sbc

parser = argparse.ArgumentParser(description='要求されたダイスの結果を返します。')
parser.add_argument('d', type=str, default='',
                    help='ダイスの種類および個数を入力してください')
parser.add_argument('-v7', action='store_true', default=bool(0),
                    help='CoC第7版仕様のd100ロールを行います。')
parser.add_argument('-bp', default='Default',
                    help='ボーナスダイスおよびペナルティダイスの数を整数で入力してください。プラス側がボーナス、マイナス側がペナルティとなります。「-bp」オプション使用時、何も値を指定しないとエラーで動きません。') 
args = parser.parse_args()

selectDice = args.d

# -v7オプション無しで-bpオプションが入っていたらアナウンスしつつ処理を中断する。
try:
    if not args.v7 and not args.bp == 'Default':
        # 条件合致したときはゼロ割エラー処理させてexceptで拾って止める。
        error = 1 / 0
except ZeroDivisionError:
    print('「-bp」オプション使用時は「-v7」オプションも同時に選択してください。\n処理を中断します。')
    exit()

# bpオプションにstr型の数字が入っている？
if bool(re.search('^[-|+|＋|ー|－]?[0-9|０-９][0-9|０-９]?$',args.bp)):
    # 全角文字が入っている？
    if bool(re.search('^[＋|ー|－]?[０-９][０-９]?$',args.bp)):
        # 処理はするけど半角文字に変換した旨をアナウンス。
        print('-bpオプションの内容に全角文字「{}」が含まれていました。\n相応な半角文字に変換してdice.pyの処理を続けます。'
              .format(re.search('^[-|+|＋|ー|－]?[0-9|０-９][0-9|０-９]?$',args.bp).group()))

    # str型の整数が入っていたので、int型に変換してbpとする。
    bp = int(dbc2sbc(args.bp))
# 整数ではなく、'Default'が入っている？    
elif args.bp == 'Default':
    # bpにはそのままの引数を入れる。
    bp = args.bp
# 'Default'でない文字列が入れられている。
else:
    print('オプション「-bp」は整数の入力のみを受け付けます。\n値を確認し、再度dice.pyを実行してください。')

# d100のバージョン選択。
selectV7 = args.v7
# ダイスの状態を取得する。
dPara = create_dPara(selectDice,selectV7,bp)
# ダイス結果リスト
diceRollList=[]

# 要求された回数分、ダイスを振る。
for i in range(1,dPara['diceCount']+1):

    diceResult = diceroll(dPara)
    diceRollList.append(diceResult['value'])
    # 毎回の詳細なロール結果を見たければこのprintを生かす。
    print(diceResult['comment'])

# 折角なので合計値をつくって表示しておく。
diceRollListSum = sum(diceRollList)
print('Result {} Total「{}」'.format(diceRollList,diceRollListSum))
