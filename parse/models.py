from django.db import models
from datetime import datetime


class Quiz(models.Model):
    name = models.CharField(verbose_name='クイズ名', max_length=128)
    date = models.DateField(verbose_name='実施日', default=datetime.min)

    @property
    def correct_rate(self):
        count = self.result_set.count()
        if count == 0:
            return 0
        return sum(
            result.correct_rate
            for result in self.result_set.all()
            ) / count

    @property
    def question_num(self):
        return self.question_set.count()

    @property
    def average_answer_time(self):
        count = self.result_set.count()
        if count == 0:
            return 0
        return sum(
            result.average_answer_time
            for result in self.result_set.all()
            ) / count


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.CharField(verbose_name='問題文', max_length=128)

    @property
    def correct(self):
        """
        TODO: 正答が複数あることは考えていない
        """
        return self.choice_set.filter(correct=True).first()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(verbose_name='選択肢本文', max_length=128)
    correct = models.BooleanField(verbose_name='正解', default=False)


class Player(models.Model):
    """
    生徒別データ

    id: アンケートの生徒番号を元に設定
    """

    name = models.CharField(verbose_name='名前', max_length=64)

    @property
    def correct_rate(self):
        count = self.result_set.count()
        if count == 0:
            return 0
        return sum(
            result.correct_rate
            for result in self.result_set.all()
            ) / count

    @property
    def average_answer_time(self):
        count = self.result_set.count()
        if count == 0:
            return 0
        return sum(
            result.average_answer_time
            for result in self.result_set.all()
            ) / count

    @classmethod
    def print_fastest_top_x(cls, x):
        player_list = [*cls.objects.all()]
        player_list = sorted(
            filter(lambda p: p.average_answer_time != 0, player_list),
            key=lambda p: p.average_answer_time)
        for rank, player in enumerate(player_list[:x], 1):
            print('{} {}: {:.3f}s'.format(
                    rank, player.name, player.average_answer_time))

    @classmethod
    def print_most_accurate_top_x(cls, x):
        player_list = [*cls.objects.all()]
        player_list = sorted(
            player_list,
            key=lambda p: p.correct_rate,
            reverse=True)
        for rank, player in enumerate(player_list[:x], 1):
            print('{} {}: {:.1f}%'.format(
                    rank, player.name, player.correct_rate))


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name='クイズ開始時間')

    class Meta:
        unique_together = (
            ("quiz", "player", ),
            )

    @property
    def question_num(self):
        return self.quiz.question_num

    @property
    def number_of_correct_answer(self):
        return sum(int(answer.correct) for answer in self.answer_set.all())

    @property
    def correct_rate(self):
        return self.number_of_correct_answer / self.question_num * 100

    @property
    def total_time(self):
        end_time = self.answer_set.order_by('-answered_time').first().answered_time
        total = end_time - self.start_time
        return total.total_seconds()

    @property
    def average_answer_time(self):
        return self.total_time / self.question_num


class Answer(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    answered_time = models.DateTimeField(verbose_name='回答時刻')

    class Meta:
        unique_together = (
            ("result", "choice", ),
            )

    @property
    def correct(self):
        return self.choice.correct

    # @property
    # def passed_time(self):
    #     """
    #     一問一問の回答にかかった時間
    #     TODO: 再度回答した時刻が存在することを考えると、
    #           上手く取得する方法が思いつかなかった
    #     """

    #     delta = self.answered_time - self.result.start_time
    #     return delta.total_seconds()
