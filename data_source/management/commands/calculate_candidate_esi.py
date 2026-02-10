from django.core.management.base import BaseCommand
from data_source.models import CandidateVoteData, Candidate, ElectionResult

class Command(BaseCommand):
    
    help = "Calculate candidate Electoral Strength Index"
    
    def handle(self, *args, **options):
        candidates = Candidate.objects.all()
        
        for candidate in candidates:
            candidate_vote_data = CandidateVoteData.objects.filter(candidate=candidate)
            
            for cand_data in candidate_vote_data:
                taf = ElectionResult.objects.filter(election_year=cand_data.election_year).first().taf
                esi = (0.5*float(cand_data.normalized_vs)) + (0.3*float(cand_data.rpi)) + (0.2*float(taf))
                
                cand_data.esi = esi
                cand_data.save()