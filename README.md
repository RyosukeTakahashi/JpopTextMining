# About

1. アーティストの歌詞を抽出して、（実装済み）
2. それを元にWordcloudを作るスクリプト（2017/06/01実装中）


# これを作るに至った経緯

Jpopってどいつもこいつも、瞳を閉じて、翼生やして、ナンバーワンよりオンリーワンって言ってやがる！青臭くて中二病で**最高じゃねーか！**

っていう言説が主に自分の中にあったので、「本当に青臭いのかどうか」を客観的に視覚的に表すツールを作れないかということで作りました。

# 環境

- anaconda4(python3)

- Phantom.jsをインストール。
  - Windowsなら以下参照。
  - https://gist.github.com/maechabin/7632c460ceede823cbde


# 実行方法

`scrapephantom.py`の

```python

if __name__ == '__main__':
    artist_name = "スガシカオ"
    main(artist_name)
    wordcloud.main(artist_name)

```
の`artist_name`を任意のアーティスト名に変えて、

```bash
python scrapephantom.py
```
を実行。

# 
