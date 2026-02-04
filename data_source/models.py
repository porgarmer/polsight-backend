from django.db import models


    
class ElectionResult(models.Model):
    election_year = models.IntegerField(null=True, blank=True)
    registered_votes = models.IntegerField(null=True, blank=True)
    voters_who_voted = models.IntegerField(null=True, blank=True)
    turnout = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)

class Candidate(models.Model):
    class FamilyGroupChoices(models.TextChoices):
        CHAN = "chan", "Chan"
        RADAZA = "radaza", "Radaza"
        CARATAO = "caratao", "Caratao"
        
    profile = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    family_group = models.TextField(choices=FamilyGroupChoices, null=True, blank=True)
    related_candidate = models.ForeignKey('self', null=True, blank=True, related_name='related_candidates', on_delete=models.PROTECT)
    
    def __str__(self):
        return self.name
    
class CandidateVoteData(models.Model):
    candidate = models.ForeignKey(Candidate, related_name="data", on_delete=models.PROTECT)
    election_year = models.IntegerField(null=True, blank=True)
    position_ran = models.CharField(max_length=50, null=True, blank=True)
    was_incumbent = models.BooleanField(null=True, blank=True)
    candidate_votes = models.IntegerField(null=True, blank=True)