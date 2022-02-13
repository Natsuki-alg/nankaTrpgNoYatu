import re
from dbc2sbc import dbc2sbc

# まだ使いこなせていないlogger機能…。
from logging import getLogger, FileHandler, DEBUG, StreamHandler, INFO, Formatter 
logger = getLogger(__name__)


def create_dPara(selectDice,d100Pattern,bp,rdmList):

    
    '''
        input   selectDice      '1d100'とか'2d6'の文字列
                d100Pattern     'calc'or'simple'
                bp              ボーナスorペナルティダイスの数
                rdmList         ランダムチョイスしたい名詞リスト

        output  dPara{'diceCount'       ダイスの数
                      'diceType'        ダイスの種類orランダムチョイス用の文字列'choice'
                      'bp'              ボーナスorペナルティダイスの数
                      'rdmList'         ランダムチョイスしたい名詞リスト
                      'errMsg'          エラーメッセージ。メインルーチンに戻ってからエラーを吐かせる。何もなければ空白文字列’’が入っている。
        }
    '''


    logger.setLevel(DEBUG)

    # 文字の揺らぎを除去する
    selectDice_rmvFlick = dbc2sbc(selectDice)
    # logger.DEBUG('selectDice :{}\n'.format(selectDice))
    # logger.DEBUG('selectDice_rmvFlick :{}\n'.format(selectDice_rmvFlick))

    dPara = {}
    para = {}
    # 何もない時の為の空白errMsg
    errMsg = ''

    # 正規表現でchoiceらしきものが引っかからなかった？
    if not re.search('^[C|c]hoice$',selectDice) == [None]:
        # 要求はchoiceでないので、ダイス要素を抽出する。

        # 振るダイスの個数を抽出(連続する3桁までの数字)
        diceCount = int(re.search('^[0-9]?[0-9]?[0-9]', selectDice_rmvFlick).group())
        # logger.DEBUG('diceCount :{}\n'.format(diceCount))

        # ダイスの種類を抽出(連続する4桁までの数字)
        diceType = int(re.search('[0-9]?[0-9]?[0-9]?[0-9]$', selectDice_rmvFlick).group())
        # logger.DEBUG('diceType :{}\n'.format(diceType))

    # 正規表現でchoiceらしきものが引っかかった？
    elif re.search('^[C|c]hoice$',selectDice) == [None]:
        # 要求はchoiceのようなので、そっち方面の準備をする。
        if not rdmList:
                # rdmListが無いのでchoiceを実行できない。エラーメッセージを戻す。
                errMsg = 'Nothing random list : ランダムチョイス用のリストが設定されていません。'
        elif rdmList:
                # チョイスしたいようなのでdParaのdiceTypeに'choice'を入れる。
                diceType = 'choice'
                # とりあえず1に固定する。
                # TODO: 回数を増やして「チョイス100回の最多な対象を選択する」とかいう遊びもできそう。
                diceCount = 1

    para={'diceCount' : diceCount,
          'diceType' : diceType,
          'd100Pattern' : d100Pattern,
          'bp' : bp,
          'rdmList' : rdmList,
          'errMsg' : errMsg
    }

    dPara.update(para)

    # logger.DEBUG('dPara:{}'.format(dPara))
    return dPara