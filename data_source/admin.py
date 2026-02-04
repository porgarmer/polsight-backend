from django.contrib import admin
from .models import Candidate, CandidateVoteData, ElectionResult
# Register your models here.

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ["profile", "name"]

@admin.register(CandidateVoteData)
class CandidateVoteAdmin(admin.ModelAdmin):
    list_display = [
        "candidate",
        "election_year", 
        "position_ran",
        "was_incumbent",
        "candidate_votes"
    ]
    
@admin.register(ElectionResult)
class ElectionResultAdmin(admin.ModelAdmin):
    list_display = [
        "election_year", 
        "registered_votes",
        "voters_who_voted",
        "turnout"
    ]