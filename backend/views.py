from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import status
from backend.serializers import CountrySerializer, QuizSerializer, RecordSerializer
from backend.models import Country, Quiz, Record
from django.db.models import Q
from rest_framework.response import Response

from functools import reduce

class CountryViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows countries to be viewed.
    """

    
    serializer_class = CountrySerializer

    def get_queryset(self):
        queryset = Country.objects.all().order_by('name')
        continent = self.request.GET.get('continent')
        if continent is not None:
            curr_continent = filter(lambda cont: cont in continent.split('-'), ['europe', 'namerica', 'samerica', 'africa', 'oceania', 'asia'])
            
            queryset = queryset.filter(reduce (lambda x,y: x | y, [Q(continent = cont) for cont in curr_continent]))
        return queryset
    

class QuizViewSet(ModelViewSet):

    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()

class RecordViewSet(ModelViewSet):
    serializer_class = RecordSerializer
    
    def get_queryset(self):
        queryset = Record.objects.all().order_by('time')
        quiz = self.request.GET.get('quiz')
        if quiz is not None:
            
            queryset = queryset.filter(quiz=quiz)
        return queryset
    
    def create(self, request, *args, **kwargs):
        # Get the submitted form data from the request object.
        form_data = request.data
        print(form_data)
        # Retrieve the Quiz object referenced by the 'quiz' field in the form data.
        quiz = Quiz.objects.get(id=int(form_data['quiz'].split(r'/')[-2]))
        
        # Check the value of the 'nbr' field in the Quiz object.
        quiz_nbr = quiz.nbr_question

        # Compare the value of 'points' in the form data with the 'nbr' value of the Quiz object.
        points = int(form_data['points'])
        if points > quiz_nbr:
            return Response({'error': "Points cannot be greater than the quiz maximum."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create the Record object
        serializer = self.get_serializer(data=form_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Create your views here.
