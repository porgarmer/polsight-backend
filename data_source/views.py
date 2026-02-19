from django.shortcuts import render
from rest_framework import views, viewsets
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from .serializer import CandidateSerializer, CandidateVoteSerializer, ElectionResultSerializer
from .models import Candidate, ElectionResult, CandidateVoteData
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from electoral_sys_backend.pagination import CustomPageNumberPagination

class CandidateViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.all().order_by("-created_at")
    parser_classes = [MultiPartParser, FormParser, FileUploadParser]
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(data={"detail": "Candidate successfully added."})
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(data={"detail": "Candidate updated added."})


class ElectionResultViewSet(viewsets.ModelViewSet):
    serializer_class = ElectionResultSerializer
    queryset = ElectionResult.objects.all().order_by("-election_year")
    pagination_class = CustomPageNumberPagination
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(data={"detail": "Voter data successfully added."})
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(data={"detail": "Voter data updated added."})
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @action(detail=False, methods=["post"], url_path="bulk")
    def bulk_upsert(self, request):
        updated = request.data.get("updated", [])
        deleted_ids = request.data.get("deleted_ids", [])
        
        if deleted_ids:
            ElectionResult.objects.filter(id__in=deleted_ids).delete()
            
        results = []
        for row in updated:
            obj_id = row.get("id", None)
            
            if obj_id:
                obj = ElectionResult.objects.filter(id=obj_id).first()
                if not obj:
                    return Response(data={"detail": f"Record with id={obj_id} not found."}, status=400)
                
                serializer = self.get_serializer(obj, data=row)

                serializer.is_valid(raise_exception=True)
                serializer.save()
                results.append(serializer.data)
            else:
                return Response(data={"detail": "No record updated."})
            
        return Response(
            {"detail": "Bulk update successful.", "count": len(results)},
            status=200
        )
            
class CandidateVoteDataFilter(django_filters.FilterSet):
    candidate = django_filters.CharFilter("candidate__name", lookup_expr="icontains")
    
class CandidateVoteDataViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateVoteSerializer
    queryset = CandidateVoteData.objects.all().order_by("election_year")
    filter_backends = [DjangoFilterBackend]
    filterset_class = CandidateVoteDataFilter
    pagination_class = CustomPageNumberPagination
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(data={"detail": "Voter data successfully added."})
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(data={"detail": "Voter data updated added."})
    