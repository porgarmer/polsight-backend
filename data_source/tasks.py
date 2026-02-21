from django_init import django_init
from .models import CandidateVoteData
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_esi():
    candites_esi = CandidateVoteData.objects.filter(candidate__name="Paz Radaza").order_by("election_year").values_list("esi", flat=True)
    candites_esi = [float(esi) for esi in candites_esi]
    print(candites_esi)
    y = np.array(candites_esi, dtype=float)
    
    X = np.arange(len(y)).reshape(-1, 1)
    
    model = LinearRegression()
    model.fit(X, y)
    
    t_next = np.array([[len(y)]])
    esi_hat = model.predict(t_next)[0]
    
    y_pred = model.predict(X)
    residuals = y - y_pred
    
    if len(y) > 2:
        sigma = residuals.std(ddof=1)
    else:
        sigma = 0.05
        
    low = esi_hat - 1.96 * sigma
    high = esi_hat + 1.96 * sigma
    
    return esi_hat, low, high

def generate_ai_insights(candidate):
    pass

print(predict_esi())