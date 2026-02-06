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
        
    def create(self, validated_data):
        voters_who_voted = validated_data.get("voters_who_voted", 0)
        registered_voters = validated_data.get("registered_voters", 0)
        
        if registered_voters == 0:
            raise serializers.ValidationError("Cannot divide by zero.")
        
        turnout = round(voters_who_voted/registered_voters, 2)

        election_result = ElectionResult.objects.create(turnout=turnout, **validated_data)
        
        return election_result
    
    def update(self, instance, validated_data):
        print("HERE")
        voters_who_voted = validated_data.get("voters_who_voted", 0)
        registered_voters = validated_data.get("registered_voters", 0)
        
        if registered_voters == 0:
            raise serializers.ValidationError("Cannot divide by zero.")
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        turnout = round(voters_who_voted/registered_voters, 2)

        instance.turnout = turnout
        
        instance.save()
        
        return instance
    
class CandidateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateVoteData
        fields = "__all__"