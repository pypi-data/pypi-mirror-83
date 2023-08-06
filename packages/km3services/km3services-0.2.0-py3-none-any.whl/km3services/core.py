import requests


def oscillationprobabilities(events):
    """Dummy accessor"""
    r = requests.post("http://131.188.167.67:30000/probabilities", json=events)
    return r.text
