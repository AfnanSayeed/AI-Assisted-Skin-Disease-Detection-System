def predict_symptoms(data):
    """
    data: dictionary of symptoms
    returns: disease, risk
    """
    # fake prediction for testing
    import random
    classes = ["Nevus", "Melanoma", "BasalCellCarcinoma", "ActinicKeratosis"]
    risk_map = {"Nevus":"Low", "Melanoma":"High", "BasalCellCarcinoma":"High", "ActinicKeratosis":"Medium"}
    
    disease = random.choice(classes)
    risk = risk_map[disease]
    return disease, risk
