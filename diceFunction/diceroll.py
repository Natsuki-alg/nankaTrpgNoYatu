# 正規表現を使用する
import re
# ランダム処理を使用する
import random

# まだ使いこなせていないlogger機能…。
from logging import getLogger, FileHandler, DEBUG, StreamHandler, INFO, Formatter
logger = getLogger(__name__)


def diceroll(dPara):
    
    '''
    引数:dPara[1×4 dict]
        selectDice  : "1d100"や"2d6"など、ダイス個数とダイス種類を表す文字列。
                      "choice"の文字列が入っていた場合rdmListの中からランダムチョイスする。
        d100Pattern : d100のロールパターン。処理パターンは下表の通り。
                            |   value   |    process     |
                            | :------:  |  :----------:  |
                            | 'simple'  |  100面ダイス×1  |
                            |  'calc'   |  10面ダイス×2   |
        bp          : CoC7版だった場合のボーナスダイスorペナルティダイス。
                      selectDiceでd100処理が選択され、かつd100Pattern='calc'の場合のみ使用する。
        rdmList     : ランダムチョイスする名前のリスト。その場に居る生物名のリストになるかな？
    
    戻り値:diceResult[1×2 dict]
        | key     :    value                                       |
        | ------- : ---------------------------------------------- |
        | result  : 最終的なダイスの結果。int型。                    |
        | comment : ダイス結果算出までの途中経過などを入れる。char型。 |
    '''
    
    # logger.setLevel(DEBUG)
    # logger.setLevel(INFO)

    diceResult ={}    

    if dPara['diceType'] == 'choice':
        # diceTypeをベースにダイスを作成する
        dice = dPara['rdmList']
    else:
        # diceTypeをベースにダイスを作成する
        dice = list(range(1,dPara['diceType']+1))
    
    # 10面ダイス×2個のd100処理を要求された？
    if dPara['diceType'] == 100 and dPara['d100Pattern'] == 'calc':
        # 一の桁ダイスと十の桁ダイスを表現するリストを作成
        dice_at1 = list(range(0, 10))
        # logger.DEBUG('dice_at1 :{}'.format(dice_at1))
        dice_at10 = list(range(0, 100 ,10))
        # logger.DEBUG('dice_at10 :{}'.format(dice_at10))
        # 10面ダイス×2個でd100ロールすることをアナウンス
        print(('「10」面ダイスを「2」個使用して「100」面ダイスロールを実行します。'))
        # 1の桁を示す10面ダイスはボーナスダイス有無に関係なく振られるので、ここで処理。
        diceResult_at1=random.choice(dice_at1)
        # logger.DEBUG('diceResult_at1 :{}'.format(diceResult_at1))
        # ボーナスorペナルティダイスの有無による処理分岐。
        if dPara['bp'] == 0:
            # ボーナスダイスが0個なので、そのまま10面ダイスを振る。
            diceResult_at10=random.choice(dice_at10)
            # logger.DEBUG('diceResult_at10 :{}'.format(diceResult_at10))
            # 両方ともゼロだった場合、ファンブルで0が出力される仕様になるので、100が入るようにする。
            if diceResult_at1 == 0 and diceResult_at10 == 0:
                diceResult.update({'value' : 100,
                                   'comment' : '1 d 100 => 0 + 00 = 100'}
                )
            else:
                diceResultVal = diceResult_at1 + diceResult_at10
                # logger.DEBUG('diceResultVal :{}'.format(diceResultVal))
                diceResult.update({'value' : diceResultVal,
                                   'comment' : '1 d {} => {} + {} = {}'
                                   .format(dPara['diceType'],diceResult_at1,diceResult_at10,diceResultVal)}
                )
            # logger.DEBUG('diceResult :{}'.format(diceResult))
        elif not dPara['bp'] == 0:
            # ボーナスorペナルティダイスがあるので、それ専用のリストを用意
            bpResult = []
    
            # 10の位のダイスを1+abs(dPara[bp])個振る
            for iat10 in range(1,1+abs(dPara['bp']),1):
                bpResultDice=random.choice(dice_at10)
                # logger.DEBUG('bpResultDice :{}'.format(bpResultDice))
                bpResult.append(bpResultDice)

            # logger.DEBUG('bpResult :{}'.format(bpResult))
    
            # ボーナスダイス(プラス)側だった？
            if dPara['bp'] > 0:
                # ボーナスダイスの個数をアナウンス
                print('ボーナスダイスは 「{}」 個です。'.format(dPara['bp']))
                # logger.DEBUG('ボーナスダイスは 「{}」 個です。\n'.format(dPara['bp']))
    
                # 一の桁ロール結果がゼロで、十の桁ロール結果が全て0？
                if diceResult_at1 == 0:
                    # 十の桁群の状態によって処理を分岐
                    # logger.DEBUG('bpResult_reject0 :{}'.format([i for i in bpResult if not i == 0]))
                    if [i for i in bpResult if not i == 0]:
                        # 十の桁のゼロ以外で最も小さい値を採用
                        diceResultVal = diceResult_at1 + min([i for i in bpResult if not i == 0])
                        diceResult.update({'value' : diceResultVal,
                                           'comment' : '1 d {} => {} + {} = {}'
                                           .format(dPara['diceType'],diceResult_at1,bpResult,diceResultVal)}
                        )
                        # logger.DEBUG('diceResult :{}'.format(diceResult))
                    else:
                        # 一の桁がゼロで十の桁も全てゼロなので救いはない。
                        diceResult.update({'value' : 100,
                                           'comment' : '1 d 100 => 0 + 00 = 100'}
                        )
                        # logger.DEBUG('diceResult :{}'.format(diceResult))
                else:
                    # 一の桁がゼロではないので、十の桁は小さい値を採用
                    diceResultVal = diceResult_at1 + min(bpResult)
                    diceResult.update({'value' : diceResultVal,
                                      'comment' : '1 d {} => {} + {} = {}'
                                      .format(dPara['diceType'],diceResult_at1,bpResult,diceResultVal)}
                    )
                    # logger.DEBUG('diceResult :{}'.format(diceResult))
    
            # ペナルティダイス(マイナス)側だった？
            elif dPara['bp'] < 0:
                # ペナルティダイスの個数をアナウンス
                print('ペナルティダイスは 「{}」 個です。'.format(abs(dPara['bp'])))
                # logger.DEBUG('ペナルティダイスは 「{}」 個です。\n'.format(dPara['bp']))
                # 一の桁ロール結果がゼロ？
                if diceResult_at1 == 0:
                    # かつ、十の桁にゼロが含まれる？
                    if [i for i in bpResult if i == 0]:
                        # 一の桁がゼロで、十の桁もゼロを含んでいるので救いはない。
                        diceResult.update({'value' : 100,
                                           'comment' : '1 d 100 => 0 + 00 = 100'}
                        )
                        # logger.DEBUG('diceResult :{}'.format(diceResult))
                    else:
                        # 一の桁がゼロだが、十の桁はゼロを含んでいなかった。運が良かったな？
                        diceResultVal = diceResult_at1 + max(bpResult)
                        diceResult.update({'value' : diceResultVal,
                                          'comment' : '1 d {} => {} + {} = {}'
                                          .format(dPara['diceType'],diceResult_at1,bpResult,diceResultVal)}
                        )
                        # logger.DEBUG('diceResult :{}'.format(diceResult))
                elif not diceResult_at1 == 0:
                    # 一の桁がゼロではないので、十の桁は大きい値を選択する。
                    diceResultVal = diceResult_at1 + max(bpResult)
                    diceResult.update({'value' : diceResultVal,
                                      'comment' : '1 d {} => {} + {} = {}'
                                      .format(dPara['diceType'],diceResult_at1,bpResult,diceResultVal)}
                    )
                    # logger.DEBUG('diceResult :{}'.format(diceResult))

    # 100面ダイス×1個の処理を要求された？
    elif dPara['diceType'] == 100 and dPara['d100Pattern'] == 'simple':
        # logger.INFO('「100」面ダイスを1個使用して「100」面ダイスロールを実行します。\n')
        print(('「100」面ダイスを「1」個使用して「100」面ダイスロールを実行します。'))
        dice_at100 = list(range(1, 101 , 1))
        diceResultVal = random.choice(dice_at100)
        diceResult.update({'value' : diceResultVal,
                          'comment' : '1 d {} => {}'
                          .format(dPara['diceType'],diceResultVal)}
        )
        # logger.DEBUG('diceResult :{}'.format(diceResult))
    elif dPara['diceType'] == 'choice':
        diceResultVal = random.choice(dice)
        diceResult.update({'value' : diceResultVal,
                          'comment' : 'choice {} => {}'
                          .format(dPara['rdmList'],diceResultVal)}
        )
    # 100面ダイスではないダイスロールを要求された。
    elif not dPara['diceType'] == 100:
        diceResultVal = random.choice(dice)
        diceResult.update({'value' : diceResultVal,
                          'comment' : '1 d {} => {}'
                          .format(dPara['diceType'],diceResultVal)}
        )
        # logger.DEBUG('diceResult :{}'.format(diceResult))
    
    return diceResult
    