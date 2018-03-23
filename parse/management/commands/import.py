from django.core.management import BaseCommand
import json
import sys
import re
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from dateutil.parser import parse
from parse.models import Quiz, Player, Result, Answer


def debug_print(*args, **kwargs):
    if settings.DEBUG:
        print(*args, **kwargs)


class Command(BaseCommand):
    help = (
        'データ取り込み用コマンド'
        )

    PLAYER_NAME_PATTERN = re.compile(r'[^\w]')
    OX = ('x', 'o')

    def add_arguments(self, parser):
        parser.add_argument(
            '-s', '--student-file', dest='student_path',
            help=''
            )

        parser.add_argument(
            '-q', '--quiz-file', dest='quiz_path',
            help=''
            )

        parser.add_argument(
            '-r', '--result-file', dest='result_path',
            help=''
            )

    def handle(self, *args, **options):
        student_path = options['student_path']
        quiz_path = options['quiz_path']
        result_path = options['result_path']
        if not (student_path or result_path or quiz_path):
            self.stderr.write(f"Need at least 1 file.")
            sys.exit(2)

        if student_path:
            self.import_student(student_path)
        if quiz_path:
            self.import_quiz(quiz_path)
        if result_path:
            self.import_result(result_path)

    def import_student(self, student_path):
        # 生徒データ
        with open(student_path) as f:
            student_list = json.load(f)
        for student in student_list:
            Player.objects.create(
                id=student['id'],
                name=student['name']
                )

    def import_quiz(self, quiz_path):
        # クイズの問題データ
        with open(quiz_path) as f:
            quizzes = json.load(f)
        for qz in quizzes:
            quiz = Quiz.objects.create(name=qz['quizId'], date=parse(qz["date"]))
            debug_print(f'----- {quiz.name} -----')
            for q in qz['pages']:
                question = quiz.question_set.create(text=q['question'])
                for text in q['choices']:
                    correct = text in q['answers']
                    question.choice_set.create(text=text, correct=correct)
                    debug_print(f'{self.OX[int(correct)]}: {text}')

    def import_result(self, robot_path):
        # クイズの結果データ
        with open(robot_path) as f:
            data = json.load(f)
        # 回答のみ取り出す
        quiz_answers = data['quizAnswers']

        # プレイヤーの一覧を取得
        player_list = [*Player.objects.all()]
        # テストプレイヤー除外
        exclude_player_name = []
        # いろんな偽名がある生徒に対応
        player_name_alias = {}

        for name, answer_data in quiz_answers.items():
            quiz = Quiz.objects.get(name=name)
            debug_print(quiz.name)
            for question_text, answers in answer_data.items():
                question = quiz.question_set.get(text=question_text)
                debug_print(question.text)
                for answer in answers.values():
                    # スペースなどの記号を取り除く
                    player_name = self.PLAYER_NAME_PATTERN.sub('', answer['name'])
                    if player_name in exclude_player_name:
                        continue
                    player_name = player_name_alias.get(player_name) or player_name

                    try:
                        player = Player.objects.get(
                            name=player_name
                            )
                    except ObjectDoesNotExist:
                        print(f'「{player_name}」に該当する生徒がいませんでした')
                        for player in player_list:
                            print(player.id, player.name)
                        player_id = 0
                        while player_id == 0:
                            player_id = input(
                                '該当する生徒の番号を入力してください。\n'
                                'または何も入力せずにEnterキーを押してください。: ')
                            if player_id:
                                try:
                                    player = Player.objects.get(id=player_id)
                                except ObjectDoesNotExist:
                                    print(f'{player_id}番に該当する生徒はいません')
                                    continue
                                player_name_alias[player_name] = player.name
                                break
                        else:
                            exclude_player_name.append(player_name)
                            continue

                    result, _ = Result.objects.get_or_create(
                        quiz=quiz,
                        player=player,
                        start_time=parse(answer['quizStartTime'])
                        )
                    Answer.objects.create(
                        result=result,
                        choice=question.choice_set.get(text=answer['answer']),
                        answered_time=parse(answer['time'])
                        )
