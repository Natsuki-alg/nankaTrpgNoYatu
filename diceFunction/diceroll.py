# ランダム処理を使用する
import random


def diceroll(dPara):
    
    '''
    引数:dPara[1×3 dict]
        selectDice  : "1d100"や"2d6"など、ダイス個数とダイス種類を表す文字列。
                      "choice"の文字列が入っていた場合、要素3のリスト(タプルになるかも)からランダムチョイスする。
        selectV7    : d100のロールパターン。処理パターンは下表の通り。
                            |   value   |    process     |
                            | :------:  |  :----------:  |
                            |  'False'  |  100面ダイス×1  |
                            |  'True'   |  10面ダイス×2   |
        bp          : CoC7版だった場合のボーナスダイスorペナルティダイス。
                      selectV7=Trueかつbp='Default'の場合、エラーで止める。
    
    戻り値:diceResult[dict]
        ダイスロール結果とコメントをまとめたもの。
                            |    key    |     value      |
                            | :------:  |  :----------:  |
                            |  'value'  | 判定結果(int)、もしくは'error' |
                            | 'comment' | 1 d 100 => 3 + 20 = 23 のような文字列、もしくはエラーメッセージ。  |
    '''
    

    diceResult ={}

    # シンプルタイプのダイスロール(100面ダイス×1個含む)を要求された。
    # -v7オプション無しで-bpオプションが使用されている。
    if not dPara['selectV7'] and not dPara['bp'] == 'Default':
        # エラーで止める。
        diceResult.update({'value' : 'error',
                           'comment' : 'オプション「-bp」はオプション「-v7」との組み合わせが必須です。\nオプション設定を再確認し、再度dice.pyを実行してください。'
        })
    # シンプルなダイスロールをする。
    elif not dPara['selectV7'] or\
             dPara['selectV7'] and not dPara['diceType'] == 100:
        # -bpオプションが使用されている？
        if not dPara['bp'] == 'Default':
            # -bpオプションを使わない旨をアナウンス。
            # TODO:エラーで止めた方がいいかもね。
            print('「-bp」オプションが選択されていますが、ダイスパターンがd100でないため無効化します。')

        # diceTypeをベースにダイスを作成する
        dice = list(range(1,dPara['diceType']+1))
        diceResultVal = random.choice(dice)
        diceResult.update({'value' : diceResultVal,
                          'comment' : '1 d {} => {}'
                          .format(dPara['diceType'],diceResultVal)}
        )
    # -v7オプションありでd100を要求された？
    elif dPara['selectV7'] and dPara['diceType'] == 100:
        # 一の桁ダイスと十の桁ダイスを表現するリストを作成
        dice_at1 = list(range(0, 10))
        dice_at10 = list(range(0, 100 ,10))
        # 10面ダイス×2個でd100ロールすることをアナウンス
        print(('「10」面ダイスを「2」個使用して「100」面ダイスロールを実行します。'))
        # 1の桁を示す10面ダイスはボーナスダイス有無に関係なく振られるので、ここで処理。
        diceResult_at1=random.choice(dice_at1)
        # ボーナスorペナルティダイスの有無による処理分岐。
        if dPara['bp'] == 0 or dPara['bp'] == 'Default':
            # ボーナスダイスが0個(bpオプション未使用時のゼロと見なす)なので、そのまま10面ダイスを振る。
            diceResult_at10=random.choice(dice_at10)
            # 両方ともゼロだった場合、ファンブルで0が出力される仕様になるので、100が入るようにする。
            if diceResult_at1 == 0 and diceResult_at10 == 0:
                diceResult.update({'value' : 100,
                                   'comment' : '1 d 100 => 0 + 00 = 100'}
                )
            else:
                diceResultVal = diceResult_at1 + diceResult_at10
                diceResult.update({'value' : diceResultVal,
                                   'comment' : '1 d {} => {} + {} = {}'
                                   .format(dPara['diceType'],diceResult_at1,diceResult_at10,diceResultVal)}
                )
        elif not dPara['bp'] == 0 or dPara['bp'] == 'Default':
            # ボーナスorペナルティダイスがあるので、それ専用のリストを用意
            bpResult = []
    
            # 10の位のダイスを1+abs(dPara[bp])個振る
            for iat10 in range(0,abs(dPara['bp'])+1):
                bpResultDice=random.choice(dice_at10)
                bpResult.append(bpResultDice)

            # ボーナスダイス(プラス)側だった？
            if dPara['bp'] > 0:
                # ボーナスダイスの個数をアナウンス
                print('ボーナスダイスは 「{}」 個です。'.format(dPara['bp']))
    
                # 一の桁ロール結果がゼロで、十の桁ロール結果が全て0？
                if diceResult_at1 == 0:
                    # 十の桁群の状態によって処理を分岐
                    if [i for i in bpResult if not i == 0]:
                        # 十の桁のゼロ以外で最も小さい値を採用
                        diceResultVal = diceResult_at1 + min([i for i in bpResult if not i == 0])
                        diceResult.update({'value' : diceResultVal,
                                           'comment' : '1 d {} => {} + best{} = {}'
                                           .format(dPara['diceType'],diceResult_at1,bpResult,diceResultVal)}
                        )
                    else:
                        # 一の桁がゼロで十の桁も全てゼロなので救いはない。
                        diceResult.update({'value' : 100,
                                           'comment' : '1 d 100 => 0 + best{} = 100'.format(bpResultDice)}
                        )
                else:
                    # 一の桁がゼロではないので、十の桁は小さい値を採用
                    diceResultVal = diceResult_at1 + min(bpResult)
                    diceResult.update({'value' : diceResultVal,
                                      'comment' : '1 d {} => {} + best{} = {}'
                                      .format(dPara['diceType'],diceResult_at1,bpResult,diceResultVal)}
                    )
    
            # ペナルティダイス(マイナス)側だった？
            elif dPara['bp'] < 0:
                # ペナルティダイスの個数をアナウンス
                print('ペナルティダイスは 「{}」 個です。'.format(abs(dPara['bp'])))
                # 一の桁ロール結果がゼロ？
                if diceResult_at1 == 0:
                    # かつ、十の桁にゼロが含まれる？
                    if [i for i in bpResult if i == 0]:
                        # 一の桁がゼロで、十の桁もゼロを含んでいるので救いはない。
                        diceResult.update({'value' : 100,
                                           'comment' : '1 d 100 => 0 + worst{} = 100'.format(bpResultDice)}
                        )
                    else:
                        # 一の桁がゼロだが、十の桁はゼロを含んでいなかった。運が良かったな？
                        diceResultVal = diceResult_at1 + max(bpResult)
                        diceResult.update({'value' : diceResultVal,
                                          'comment' : '1 d {} => {} + worst{} = {}'
                                          .format(dPara['diceType'],diceResult_at1,bpResult,diceResultVal)}
                        )
                elif not diceResult_at1 == 0:
                    # 一の桁がゼロではないので、十の桁は大きい値を選択する。
                    diceResultVal = diceResult_at1 + max(bpResult)
                    diceResult.update({'value' : diceResultVal,
                                      'comment' : '1 d {} => {} + worst{} = {}'
                                      .format(dPara['diceType'],diceResult_at1,bpResult,diceResultVal)}
                    )

    return diceResult
    