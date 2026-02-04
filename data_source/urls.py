from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"candidate", viewset=views.CandidateViewSet, basename="candidate")
router.register(r"candidate-data", viewset=views.CandidateVoteDataViewSet, basename="candidate_data")
router.register(r'election-result', viewset=views.ElectionResultViewSet, basename="election_results")
urlpatterns = [
   path("", include(router.urls))
]
