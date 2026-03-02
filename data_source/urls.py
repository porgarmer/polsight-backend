from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .custom_drf_views.views import CookieTokenObtainPairView, CookieTokenRefreshView, CookieLogoutView
router = DefaultRouter()
router.register(r"candidate", viewset=views.CandidateViewSet, basename="candidate")
router.register(r"candidate-data", viewset=views.CandidateVoteDataViewSet, basename="candidate_data")
router.register(r'election-result', viewset=views.ElectionResultViewSet, basename="election_results")
urlpatterns = [
   path("auth/login/", CookieTokenObtainPairView.as_view(), name="jwt_login"),
   path("auth/refresh/", CookieTokenRefreshView.as_view(), name="jwt_refresh"),
   path("auth/logout/", CookieLogoutView.as_view(), name="jwt_logout"),
   path("auth/me/", view=views.MeView.as_view()),
   
   path("", include(router.urls)),
   path("esi-forecast/", view=views.ESIForecastView.as_view(), name="esi_forecast")
]
