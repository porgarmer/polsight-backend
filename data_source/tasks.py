from django_init import django_init
from .models import CandidateVoteData, Candidate, ESIForecast
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_esi(candidate):
    candites_esi = CandidateVoteData.objects.filter(candidate=candidate).order_by("election_year").values_list("election_year", "esi")
    
    latest_election_cycle = candites_esi.last()[0]
    
    #election is every three years
    election_cyle_interval = 3
    next_election_cyle = latest_election_cycle + election_cyle_interval
    
    candites_esi = [float(esi[1]) for esi in candites_esi]
    
    y = np.array(candites_esi, dtype=float)
    
    X = np.arange(len(y)).reshape(-1, 1)
    
    model = LinearRegression()
    model.fit(X, y)
    
    t_next = np.array([[len(y)]])
    esi_hat = round(model.predict(t_next)[0], 2)
    
    y_pred = model.predict(X)
    residuals = y - y_pred
    
    if len(y) > 2:
        sigma = residuals.std(ddof=1)
    else:
        sigma = 0.05
        
    low = esi_hat - 1.96 * sigma
    high = esi_hat + 1.96 * sigma
    
    return next_election_cyle, esi_hat, low, high

def store_candidate_esi_prediction():
    candidates = Candidate.objects.all()
    
    for candidate in candidates:
        year, predicted_value, lower_bound, upper_bound = predict_esi(candidate)
        ESIForecast.objects.create(
            candidate=candidate,
            election_year=year,
            predicted_value=predicted_value,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            model="Linear Regression"
        )

def generate_ai_insights(candidate):
    candidates = Candidate.objects.all()
    


store_candidate_esi_prediction()