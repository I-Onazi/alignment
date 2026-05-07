import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from alignment.needleman_wunsch import NeedlemanWunsch

def test_matrix_initialization():
    nw = NeedlemanWunsch("A", "T", gap=-2)
    matrix = nw.initialize_matrix()
    
    assert matrix[0][0] == 0
    assert matrix[0][1] == -2
    assert matrix[1][0] == -2
    
def test_matrix_filling():
    nw = NeedlemanWunsch("A", "A", match=1, mismatch=-1, gap=-2)
    matrix, traceback = nw.fill_matrix()
    
    # 0  -2
    # -2 1
    assert matrix[1][1] == 1
    assert "D" in traceback[1][1]

def test_traceback():
    nw = NeedlemanWunsch("GATTACA", "GCATGCU")
    nw.fill_matrix()
    results = nw.get_traceback()
    
    assert results["score"] is not None
    assert isinstance(results["seq1"], str)
    assert isinstance(results["seq2"], str)
    assert len(results["seq1"]) == len(results["seq2"])
