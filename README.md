# クイズデータ解析ツール

## Description
ロボット君のクイズ結果を解析する。

## Features
- Djangoのモデルを利用したデータ構造
- 回答速度TOP5、正確性TOP5など
- 生徒ごと、クイズごとのデータの取得

## Requirements
- Python 3.6+

## Usage
```
$ python manage.py migrate
$ python manage.py import -s student.json -q quiz.json -r result.json
$ python manage.py shell_plus
In [1]: Player.print_fastest_top_x(5)
1 生徒名: XX.XXXs
2 生徒名: XX.XXXs
3 生徒名: XX.XXXs
4 生徒名: XX.XXXs
5 生徒名: XX.XXXs
In [2]: Player.print_most_accurate_top_x(5)
1 生徒名: XX.X%
2 生徒名: XX.X%
3 生徒名: XX.X%
4 生徒名: XX.X%
5 生徒名: XX.X%
```

### import command
```
$ python manage.py import -s student.json
$ python manage.py import -q quiz.json
$ python manage.py import -r result.json
```

## Installation
```
$ git clone https://github.com/Learning-Programing-at-UEC/robot-quiz-analyzer.git
$ pip install -r requirements.txt
```
