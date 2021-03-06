# nankaTrpgNoYatu
TRPGのなんかを作ろう！

## やりたいこと案
セッション中、GMがよりマスタリングに集中できるようにサポートするツールが欲しい。

ターゲットにしているTRPGシステム：ベーシック・ロールプレイング

⇒PLの負担も少なくし、互いにストレス少なくセッションを遊べるようにしたい。

### GMしてる時にやっている作業の抜粋
シナリオ進行
イベントの管理・シナリオチャートの確認・判定の判断
事前準備（シナリオの目的とキーポイントの設定）

アドリブ
（これは経験と知見を増やして対応）
想定外への対応。
（これは経験と知見を増やして対応）
モブキャラの昇格。
（パラメータの簡易作成）
ルールによる裁定の確認
（ルルブ読み。付箋など、事前準備）

-----------------------

### 即席NPCパラメータ設定ツール
シナリオ進行中に湧き出したNPCにパラメータ設定しなければならなくなった時、ワンプッシュでパラメータを生成できるツール。
ワイルドカード：特定のパラメータの決め打ち。

-----------------------

### 判定簡略化ツール
例えば、PL1が「目星」と発言したらPL1のキャラクターの能力値で目星判定を実行して結果を返してくれるようなツール。

今のところ
1. PLによる宣言
2. GMの対象選択（発狂によるランダムチョイス等もここで選択かな？）
3. 判定の実行
4. Discordに結果を返す

という挙動を検討中。

ランダムチョイスする為、全登場キャラクターの中で「この場面に出ているキャラクター」かどうかを判定できるようにしたいね。

-----------------------

### GM補助ウィンドウ
パラメータウィンドウ表示ツールとして検討していたモノ。

PL側にもこの機能を提供するためにはハードルが跳ね上がるので、GMのみで使用する方針で進める。
（画面共有で表示して共有するという手はある。操作はGMのみが可能）
ゆくゆくアップデートする可能性は捨てないでおく。

-----------------------

### PCパラメータ取得ツール
PLが作成したPC情報、およびGMが作成したエネミー情報を取得してデータベースに取り込むツール。

セッション後、成長ロールした結果を反映したPC情報を出力してPLへ渡せる機能もつけておきたいね。

-----------------------

### ダイスロール機能
引数に合わせてダイスロール結果を返してくれるツール。

引数も6版7版切替とか、対抗ロールとか、技能名打てば自動で達成値を入れつつ結果を返してきたりとか、思いついた楽に繋がる仕組みを全て盛り込んでいきたい。

6版と7版で判定のクセが違うのでその辺は気を付ける。

時代も時代なので7版から先に作り始める？

ランダムチョイス機能はダイスロール機能の一部とする。（ダイス目の代わりにキャラクターを選ぶだけなので）

-----------------------

### フィールド常時監視ツール
「今いる場」と「ゲーム全体」のオブジェクト情報を取得し、各ツールに最適な動作をさせるためのツール。

シナリオチャプター管理もここに咬ませたい。

シナリオチャプター管理を別ツールに分けるかどうかはまだ不明。今のところは統合しておいていい気がしている。

私がやりたいコトの肝はこのツールなのでは？

### 機能ブロック図（初期）

言葉だけではなかなか難しい気がするので、図を起こした。

![image](https://user-images.githubusercontent.com/64512699/144745691-f94e47b4-9e00-419c-86c7-76264cd7f735.png)
![image](https://user-images.githubusercontent.com/94184859/145712325-17329232-5131-4f34-ab3b-8dd245180faf.png)



