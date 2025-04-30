# tests/test_risk_classifier.py
import pytest
from core.risk_classifier import RiskClassifier

def test_classify_low():
    clf = RiskClassifier()
    assert clf.classify(0.1) == "low"

def test_classify_medium():
    clf = RiskClassifier()
    assert clf.classify(0.4) == "medium"

def test_classify_high():
    clf = RiskClassifier()
    assert clf.classify(0.9) == "high"

def test_invalid_input_type():
    clf = RiskClassifier()
    with pytest.raises(TypeError):
        clf.classify("abc")  # 非法輸入類型
if __name__ == "__main__":
    # 執行 pytest，指定當前檔案
    import sys
    sys.exit(pytest.main([__file__]))

