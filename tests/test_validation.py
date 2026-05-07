import pytest
from alignment.validator import identify_type, validate_sequences

def test_identify_type():
    assert identify_type("ACTG") == "DNA"
    assert identify_type("ACGU") == "RNA"
    assert identify_type("ACDEFGHIKLMNPQRSTVWY") == "Protein"
    assert identify_type("12345") == "Unknown"
    assert identify_type("") == "Empty"

def test_validate_sequences_valid():
    is_valid, msg, t = validate_sequences("ACTG", "TGCA")
    assert is_valid is True
    assert t == "DNA"
    
def test_validate_sequences_empty():
    is_valid, msg, t = validate_sequences("", "ACTG")
    assert is_valid is False
    assert "Both sequences must be provided" in msg

def test_validate_sequences_invalid():
    is_valid, msg, t = validate_sequences("ACTGZ", "ACTG")
    assert is_valid is False
    assert "invalid" in msg.lower()
