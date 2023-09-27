from django.db import models

class Country(models.Model):

    name = models.CharField(max_length=200)
    shape = models.CharField(max_length=200)
    flag = models.CharField(max_length=200)
    continent = models.CharField(max_length=200)
    capitale = models.CharField(max_length=200)
    iso = models.CharField(max_length=3, primary_key=True)
    lat = models.FloatField(default=0)
    lon = models.FloatField(default=0)
    

    def __str__(self) -> str:
        return f"Capital: {self.capitale}"

class Quiz(models.Model):
    nbr_question = models.IntegerField()
    name = models.CharField(max_length=200)
    continents = models.CharField(max_length=200)
    difficulty = models.IntegerField()
    answer_difficulty = models.IntegerField()
    type_questions = models.CharField(max_length=400, default="")

    def get_continents(self):
        return self.continents.split(';')


class Record(models.Model):
    time = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    device = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
# Create your models here.
