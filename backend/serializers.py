from backend.models import Country, Quiz, Record
from rest_framework import serializers

class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ['name', 'shape', 'flag', 'continent', 'capitale', 'pk']

class QuizSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Quiz
        fields = ['nbr_question', 'name', 'continents', 'difficulty', 'answer_difficulty', 'type_questions', 'pk']

class RecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Record
        fields = ['time', 'user', 'device', 'quiz', 'points']


