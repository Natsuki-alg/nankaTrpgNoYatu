import re
from dbc2sbc import dbc2sbc


def create_dPara(selectDice,selectV7,bp):

    
    '''
        input   selectDice      '1d100'とか'2d6'の文字列
                selectV7        'True'or'False'
                bp              ボーナスorペナルティダイスの数。もしくは'Default'

        output  dPara{'diceCount'       ダイスの数
                      'diceType'        ダイスの種類
                      'bp'              ボーナスorペナルティダイスの数
                      'errMsg'          エラーメッセージ。メインルーチンに戻ってからエラーを吐かせる。
                                        何もなければ空白文字列’’が入っている。

    '''


    # 文字の揺らぎを除去する
    selectDice_rmvFlick = dbc2sbc(selectDice)

    dPara = {}
    para = {}
    # 何もない時の為の空白errMsg
    errMsg = ''

    # 引数selectDiceの中身が「☆[D|d]☆」(☆は4桁までのゼロにならない数字の並び)以外のパターンの文字列だった？
    if bool(re.search('^[1-9][0-9]?[0-9]?[0-9]?[D|d][1-9][0-9]?[0-9]?[0-9]?$',selectDice_rmvFlick)):
        # 要求がダイスだと判断し、ダイス要素を抽出する。
        # 振るダイスの個数を抽出(連続する4桁までの数字)
        diceCount = int(re.search('^[1-9][0-9]?[0-9]?[0-9]?', selectDice_rmvFlick).group())
        # ダイスの種類を抽出(連続する4桁までの数字)
        diceType = int(re.search('[1-9][0-9]?[0-9]?[0-9]?$', selectDice_rmvFlick).group())
    elif not bool(re.search('^[1-9][0-9]?[0-9]?[0-9]?[D|d][1-9][0-9]?[0-9]?[0-9]?$',selectDice_rmvFlick)):
        # ダイスと判断できない文字列が入れられていたのでエラーメッセージを入れて戻す。
        errMsg = 'SyntaxError (DiceSelect) : ダイスの構文エラーです。dを中心にし、前後にゼロではない整数を入れてください。'
        diceCount = ''
        diceType = ''

    para={'diceCount' : diceCount,
          'diceType' : diceType,
          'selectV7' : selectV7,
          'bp' : bp,
          'errMsg' : errMsg
    }

    dPara.update(para)

    return dPara