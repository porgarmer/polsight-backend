from django.contrib import admin
from .models import Candidate, CandidateVoteData, ElectionResult, AIInsights, CandidateAchievements
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
    
    list_filter = [
        "candidate"
    ]
    
@admin.register(ElectionResult)
class ElectionResultAdmin(admin.ModelAdmin):
    list_display = [
        "election_year", 
        "registered_voters",
        "voters_who_voted",
        "turnout"
    ]
    
@admin.register(AIInsights)
class AIInishgtsAdmin(admin.ModelAdmin):
    list_display = [
        "candidate", 
        "created_at",
    ]
    
    
@admin.register(CandidateAchievements)
class CandidateAchievementAdmin(admin.ModelAdmin):
    list_display = [
        "candidate", 
        "created_at",
    ]
    
    