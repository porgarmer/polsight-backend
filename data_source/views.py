from django.shortcuts import render
from rest_framework import views, viewsets
from .serializer import CandidateSerializer, CandidateVoteSerializer, ElectionResultSerializer
from .models import Candidate, ElectionResult, CandidateVoteData
from rest_framework.response import Response

class CandidateViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.all()
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(data={"detail": "Candidate successfully added."})
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(data={"detail": "Candidate updated added."})


class ElectionResultViewSet(viewsets.ModelViewSet):
    serializer_class = ElectionResultSerializer
    queryset = ElectionResult.objects.all()
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(data={"detail": "Voter data successfully added."})
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(data={"detail": "Voter data updated added."})
    
class CandidateVoteDataViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateVoteSerializer
    queryset = CandidateVoteData.objects.all()
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(data={"detail": "Voter data successfully added."})
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(data={"detail": "Voter data updated added."})