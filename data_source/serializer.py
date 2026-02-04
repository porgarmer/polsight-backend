from rest_framework import serializers
from .models import Candidate, ElectionResult, CandidateVoteData

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"
        
class ElectionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionResult
        fields = "__all__"
        
class CandidateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateVoteData
        fields = "__all__"