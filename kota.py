# -*- coding:utf-8 -*-

import sys
import argparse
import re
#import pyodbc      ※SQL Serverへの接続用。pyodbcをインストールしてコメント外してください。

#def write_to_db(list):
#    この関数で「DB接続 → 書き出し → DB切断」する。
#
#    ※書き出し時のメモ（以下のように操作すれば、レコードごとの各項目の値がみれるはず）
#    for key in list:
#        list[key]["date"]  #これは日付
#        list[key]["count"]  #これはカウント

def summary(list):
    results = {}
    pat = re.compile("^(.+?) .+" \
                    "アクション名:(.+?) " \
                    "コントローラ名:(.+?) " \
                    "SessionID:(.+?) " \
                    "UserID:(.+)")
    for l in list:
        for match in pat.finditer(l):
            key = (match.group(3), match.group(4))
            getval = results.get(key)
            if getval:
                getval["count"] = getval["count"] + 1
                results[key] = getval
            else:
                results[key] = {"date": match.group(1), \
                                "control": match.group(3), \
                                "user": match.group(5), \
                                "session": match.group(4), \
                                "count": 1}
    return results

def is_OnActionExecuting(line):
    pat = re.compile(".+ OnActionExecuting\(\):.+")
    return pat.match(line)

def filter_OnActionExecuting(lines):
    return [i for i in lines if is_OnActionExecuting(i)]

def read_file_to_list(fpath, enc):
    with open(fpath, 'r', encoding=enc) as f:
        return f.readlines()

def main():
    # 実行時の引数定義（ファイルパス、ファイルの文字コード）
    parser = argparse.ArgumentParser(description='This script is unko!.')
    parser.add_argument(
        'file_path',
        action='store',
        nargs=None,
        const=None,
        default=None,
        type=str,
        choices=None,
        help='ターゲットのログファイルのパスを指定する.',
        metavar=None)
    parser.add_argument(
        '-e', '--encoding',
        action='store',
        nargs='?',
        const=None,
        default='utf-8',
        type=str,
        choices=None,
        help='ログファイルの文字コード指定オプション. 例）cp932 （default: utf-8）',
        metavar=None)
    args = parser.parse_args()

    # 主処理
    l = read_file_to_list(args.file_path, args.encoding)    #ファイル読んでリストにするだけ
    l = filter_OnActionExecuting(l)                         #"OnActionExecuting"行だけ抽出
    l = summary(l)                                          #コントローラ＆セッション別に集計

    # 【確認用】コントローラ＆セッション別の集計結果を表示してみる
    for key in l:
        print("--------------------")
        print(key)
        for col in l[key]:
            print(" ", col, ":", l[key][col])

    # 集計結果を SQL Server に書き出す ※この関数は作ってないし、あくまでサンプル
    #write_to_db(l)

if __name__ == '__main__':
    main()
