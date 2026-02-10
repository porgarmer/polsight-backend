from rest_framework import serializers
from .models import Candidate, ElectionResult, CandidateVoteData
from django.db.models import Sum
import statistics

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"
        
class ElectionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionResult
        fields = "__all__"
        read_only_fields = ["turnout", "turnout_volatility", "taf"]
        
    def create(self, validated_data):        
        voters_who_voted = validated_data.get("voters_who_voted", 0)
        registered_voters = validated_data.get("registered_voters", 0)

        if registered_voters == 0:
            raise serializers.ValidationError("Cannot divide by zero.")
        
        elif voters_who_voted is None or registered_voters is None:
            raise serializers.ValidationError("Please enter a value for both the registered voters and voters who voted.")
        
        turnout = round(voters_who_voted/registered_voters, 2)
        validated_data["turnout"] = turnout
        
        #calculations for TAF (Turnout adjustment factor). This excludes the current election period being added.
        election_results = ElectionResult.objects.filter(election_year__lt=validated_data["election_year"])
        if election_results:            
            total_turnout = election_results.aggregate(total_turnout=Sum("turnout")).get("total_turnout")
            count = election_results.count()
        #if election results is none, this is the first entry
        else:
            total_turnout = turnout
            count = 1
        average = float(total_turnout / count)
        taf = turnout / average
        validated_data["taf"] = taf
        
        #Turnout volatility
        election_data = list(ElectionResult.objects.values_list("turnout", flat=True))
        #Convert Decimal to float
        election_data = [float(data) for data in election_data]
        #Include latest turnout
        election_data.append(turnout)
        turnout_volatility = statistics.stdev(election_data)
        validated_data["turnout_volatility"] = turnout_volatility
        
        election_result = ElectionResult.objects.create(**validated_data)
        
        return election_result
    
    def update(self, instance, validated_data):
        voters_who_voted = validated_data.get("voters_who_voted", 0)
        registered_voters = validated_data.get("registered_voters", 0)
        
        if registered_voters == 0:
            raise serializers.ValidationError("Cannot divide by zero.")
        
        elif voters_who_voted is None or registered_voters is None:
            raise serializers.ValidationError("Please enter a value for both the registered voters and voters who voted.")
        
        turnout = round(voters_who_voted/registered_voters, 2)
        validated_data["turnout"] = turnout
        
        #calculations for TAF (Turnout adjustment factor). Excludes the current period being updated
        election_results = ElectionResult.objects.filter(election_year__lt=validated_data["election_year"])
        if election_results: 
            total_turnout = election_results.aggregate(total_turnout=Sum("turnout")).get("total_turnout")
            count = election_results.count() 
        #if election results is None, this means the first entry is being updated
        else:
            total_turnout = turnout
            count = 1
        average = float(total_turnout / count)
        taf = turnout / average
        validated_data["taf"] = taf
                
        #Turnout volatility
        election_data = list(ElectionResult.objects.values_list("turnout", flat=True))
        #Convert Decimal to float
        election_data = [float(data) for data in election_data]
        #Include latest turnout
        election_data.append(turnout)
        turnout_volatility = statistics.stdev(election_data)
        validated_data["turnout_volatility"] = turnout_volatility
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        return instance
    
class CandidateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateVoteData
        fields = "__all__"
        read_only_fields = ["esi", "rpi", "normalized_vs"]