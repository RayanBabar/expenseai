import random

def get_synthetic_profile():
    """
    Generates a synthetic user profile for testing purposes.
    Returns a dictionary with keys: income, family_size, utility_bills_paid
    """
    profile = {
        "income": random.choice([20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]),
        "family_size": random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        "utility_bills_paid": random.choice([True, False])
    }
    return profile