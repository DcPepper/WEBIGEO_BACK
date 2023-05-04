from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import permissions
from backend.serializers import CountrySerializer, QuizSerializer
from backend.models import Country, Quiz
from django.db.models import Q

from functools import reduce

class CountryViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows countries to be viewed.
    """

    
    serializer_class = CountrySerializer

    def get_queryset(self):
        queryset = Country.objects.all().order_by('name')
        continent = self.request.GET.get('continent')
        print(continent)
        if continent is not None:
            curr_continent = filter(lambda cont: cont in continent.split('-'), ['europe', 'namerica', 'samerica', 'africa', 'oceania', 'asia'])
            queryset = queryset.filter(reduce (lambda x,y: x | y, [Q(continent = cont) for cont in curr_continent]))
        return queryset
    

class QuizViewSet(ReadOnlyModelViewSet):

    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()

# Create your views here.
