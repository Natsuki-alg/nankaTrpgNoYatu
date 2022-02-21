import random
import argparse

parser = argparse.ArgumentParser(description='指定されたリストからランダムチョイスを実行する。')
parser.add_argument('-l', required=True, nargs="*", type=str, default='Empty List',
                    help='必須項目。ランダムチョイスしたい文字列を半角スペース区切りで入力してください。') 
parser.add_argument('--r', action='store_true',
                    help='choiceの表現に揺らぎを導入したい時に入れるオプション。')
args = parser.parse_args()

# choiceするリスト
rdmList = args.l

# 処理用の変数を作成。
choiceResult = []
choiceResult_ratio = {}

if args.r:
    # 揺らぎの要求があったので、choiceを1000回実行する。
    for i in range(0,1000):
        choiceResult.append(random.choice(rdmList))
elif not args.r:
    # 揺らぎの要求が無かったのでchoiceを1回実行する。
    choiceResult.append(random.choice(rdmList))

if len(choiceResult) == 1:
    # 揺らぎ要求無しの結果だったので、フツーに知らせる。
    print('choice {} => {}'.format(rdmList,choiceResult))
elif len(choiceResult) > 1:
    # 揺らぎ要求有りの結果だったので、知らせる前の準備をする。
    for i in range(0,len(rdmList)):
        choiceResult_ratio.update({'{}'.format(rdmList[i]):choiceResult.count(rdmList[i])
        })
    print('{} => {}\nbreakdown : {}'.format(rdmList,max(choiceResult_ratio,key=choiceResult_ratio.get),choiceResult_ratio))



