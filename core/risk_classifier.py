# core/risk_classifier.py

class RiskClassifier:
    def __init__(self, low=0.3, high=0.7):
        self.low_threshold = low
        self.high_threshold = high

    def classify(self, entropy: float) -> str:
        if not isinstance(entropy, (int, float)):
            raise TypeError("entropy 必須是數值")
        if entropy < self.low_threshold:
            return "low"
        elif entropy < self.high_threshold:
            return "medium"
        else:
            return "high"

