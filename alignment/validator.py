import re

def identify_type(seq: str) -> str:
    if not seq:
        return "Empty"
    if re.match(r'^[ACGT]+$', seq):
        return "DNA"
    if re.match(r'^[ACGU]+$', seq):
        return "RNA"
    if re.match(r'^[ACDEFGHIKLMNPQRSTVWY]+$', seq):
        return "Protein"
    return "Unknown"

def validate_sequences(seq1: str, seq2: str):
    """
    Validates two biological sequences.
    Returns: (is_valid, error_message, sequence_type)
    """
    seq1 = seq1.strip().upper()
    seq2 = seq2.strip().upper()
    
    if not seq1 or not seq2:
        return False, "Both sequences must be provided.", ""
        
    type1 = identify_type(seq1)
    type2 = identify_type(seq2)
    
    if type1 == "Unknown":
        return False, "Sequence 1 contains invalid biological characters.", ""
    if type2 == "Unknown":
        return False, "Sequence 2 contains invalid biological characters.", ""
        
    if type1 != type2:
        return True, "Sequence types differ, treating as Protein.", "Protein"
        
    return True, f"Valid {type1} sequences.", type1
