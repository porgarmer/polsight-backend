from django.db import models
from django.utils.translation import gettext_lazy as _

    
class ElectionResult(models.Model):
    election_year = models.IntegerField(null=True, blank=True)
    registered_voters = models.IntegerField(null=True, blank=True)
    voters_who_voted = models.IntegerField(null=True, blank=True)
    turnout_volatility = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    turnout = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    
    #Turnout Adjustment Factor
    #A normalization factor that accounts for how participation levels compare to historical norms.
    taf = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    
    def __str__(self):
        return f"Election Year {self.election_year}"
    

class Candidate(models.Model):
    class FamilyGroupChoices(models.TextChoices):
        CHAN = "chan", _("Chan")
        RADAZA = "radaza", _("Radaza")
        CARATAO = "caratao", _("Caratao")
        
    profile = models.ImageField(null=True, blank=True, upload_to="candiate-profile/")
    name = models.CharField(max_length=50, null=True, blank=True)
    family_group = models.TextField(choices=FamilyGroupChoices, null=True, blank=True)
    related_candidate = models.ForeignKey('self', null=True, blank=True, related_name='related_candidates', on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class CandidateVoteData(models.Model):
    class PositionChoices(models.TextChoices):
        MAYOR = "mayor", _("Mayor")
        CONGRESSMAN = "congressman", _("Congressman")
    candidate = models.ForeignKey(Candidate, related_name="data", on_delete=models.PROTECT)
    election_year = models.IntegerField(null=True, blank=True)
    position_ran = models.TextField(choices=PositionChoices, null=True, blank=True)
    was_incumbent = models.BooleanField(default=False)
    candidate_votes = models.IntegerField(null=True, blank=True)
    total_votes_for_position = models.IntegerField(null=True, blank=True)
    is_winner = models.BooleanField(default=False)
    
    #Electoral Strengh Index
    #A composite index that represents a candidate’s general capacity to attract voter support, regardless of position.
    esi = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    
    #Relative Performance Index
    #A measure of how close a candidate’s performance is to the winner in the same contest.
    rpi = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=10)
    
    #Normalized Vote Share 
    #The proportion of votes a candidate received relative to all votes cast for the position they contested.
    normalized_vs = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    

