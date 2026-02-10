from django.core.management.base import BaseCommand
from data_source.models import CandidateVoteData, Candidate

class Command(BaseCommand):
    help = "Command to calculate candidate vote metrics"
    
    def handle(self, *args, **options):
        candidates = Candidate.objects.all()
        
        for candidate in candidates:
            candidate_vote_data = CandidateVoteData.objects.filter(candidate=candidate)
            
            for cand_data in candidate_vote_data:
                #Calculate candidate vote share
                vote_share = round(cand_data.candidate_votes / cand_data.total_votes_for_position, 2)
                cand_data.normalized_vs = vote_share
                
                #Calculate relative performance index
                #logic here
                
                cand_data.save()
