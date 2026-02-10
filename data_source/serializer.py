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
        
    def create(self, validated_data):
        candidate_votes = validated_data.get("candidate_votes", 0)
        total_votes_for_position = validated_data.get("total_votes_for_position", 0)
        
        if total_votes_for_position == 0:
            raise serializers.ValidationError("Cannot divide by zero.")
        
        elif candidate_votes is None or total_votes_for_position is None:
            raise serializers.ValidationError("Please enter a value for both the candidate votes and total votes for position.")
        
        normalized_vs = round(candidate_votes / total_votes_for_position, 2)
        validated_data["normalized_vs"] = normalized_vs
        
        is_winner = validated_data.get("is_winner")
        #if the candidate is the winner, the relative performance index (RPI) is 1.00
        
        election_year = validated_data.get("election_year")
        position = validated_data.get("position_ran")
        if is_winner:
            rpi = 1.00
        else:
            winner_candidate = float(CandidateVoteData.objects.filter(election_year=election_year, position_ran=position, is_winner=True).first())
            
            if not winner_candidate:
                serializers.ValidationError("The winner candidate for that election year, for that position does not exist. Please enter it first")
            
            rpi = round(normalized_vs / winner_candidate.normalized_vs)
        validated_data["rpi"] = rpi
        
        taf = ElectionResult.objects.filter(election_year=election_year).first().taf
        esi = (0.5*float(normalized_vs)) + (0.3*float(rpi)) + (0.2*float(taf))
        validated_data["esi"] = esi
        
        candidate_vote_data = CandidateVoteData.objects.create(**validated_data)
        
        return candidate_vote_data
    
    def update(self, instance, validated_data):
        candidate_votes = validated_data.get("candidate_votes", 0)
        total_votes_for_position = validated_data.get("total_votes_for_position", 0)
        
        if total_votes_for_position == 0:
            raise serializers.ValidationError("Cannot divide by zero.")
        
        elif candidate_votes is None or total_votes_for_position is None:
            raise serializers.ValidationError("Please enter a value for both the candidate votes and total votes for position.")
        
        normalized_vs = round(candidate_votes / total_votes_for_position, 2)
        validated_data["normalized_vs"] = normalized_vs
        
        is_winner = validated_data.get("is_winner")
        #if the candidate is the winner, the relative performance index (RPI) is 1.00
        
        election_year = validated_data.get("election_year")
        position = validated_data.get("position_ran")
        if is_winner:
            rpi = 1.00
        else:
            winner_candidate = float(CandidateVoteData.objects.filter(election_year=election_year, position_ran=position, is_winner=True).first())
            
            if not winner_candidate:
                serializers.ValidationError("The winner candidate for that election year, for that position does not exist. Please enter it first")
            
            rpi = round(normalized_vs / winner_candidate.normalized_vs)
        validated_data["rpi"] = rpi
        
        taf = ElectionResult.objects.filter(election_year=election_year).first().taf
        esi = (0.5*float(normalized_vs)) + (0.3*float(rpi)) + (0.2*float(taf))
        validated_data["esi"] = esi
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        
        return instance