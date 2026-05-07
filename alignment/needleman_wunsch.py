class NeedlemanWunsch:
    def __init__(self, seq1, seq2, match=1, mismatch=-1, gap=-2):
        self.seq1 = seq1
        self.seq2 = seq2
        self.match = match
        self.mismatch = mismatch
        self.gap = gap
        
        self.n = len(seq1)
        self.m = len(seq2)
        
        # Scoring matrix
        self.score_matrix = [[0] * (self.m + 1) for _ in range(self.n + 1)]
        # Traceback matrix (using strings for direction: 'D', 'U', 'L')
        self.traceback_matrix = [[''] * (self.m + 1) for _ in range(self.n + 1)]

    def initialize_matrix(self):
        """
        Phase 5: Matrix Initialization
        - First row and first column filled with gap penalties
        """
        for i in range(self.n + 1):
            self.score_matrix[i][0] = i * self.gap
            self.traceback_matrix[i][0] = 'U' # Up
            
        for j in range(self.m + 1):
            self.score_matrix[0][j] = j * self.gap
            self.traceback_matrix[0][j] = 'L' # Left
            
        self.traceback_matrix[0][0] = 'Done'
        
        return self.score_matrix

    def fill_matrix(self):
        """
        Phase 6: Matrix Filling
        Calculates scores for Diagonal, Up, and Left.
        Records the maximum score and the direction(s) for traceback.
        """
        # Ensure it's initialized first
        self.initialize_matrix()
        
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                # Calculate the three possible scores
                # 1. Diagonal (Match/Mismatch)
                if self.seq1[i-1] == self.seq2[j-1]:
                    diag_score = self.score_matrix[i-1][j-1] + self.match
                else:
                    diag_score = self.score_matrix[i-1][j-1] + self.mismatch
                    
                # 2. Up (Gap in Sequence 2)
                up_score = self.score_matrix[i-1][j] + self.gap
                
                # 3. Left (Gap in Sequence 1)
                left_score = self.score_matrix[i][j-1] + self.gap
                
                # Find maximum score
                max_score = max(diag_score, up_score, left_score)
                self.score_matrix[i][j] = max_score
                
                # Record traceback directions (could be multiple if there's a tie)
                directions = ""
                if max_score == diag_score:
                    directions += "D"
                if max_score == up_score:
                    directions += "U"
                if max_score == left_score:
                    directions += "L"
                    
                self.traceback_matrix[i][j] = directions
                
        return self.score_matrix, self.traceback_matrix

    def get_traceback(self):
        """
        Phase 7: Traceback
        Starts from the bottom-right cell and follows pointers to (0,0).
        Reconstructs the aligned sequences.
        """
        # Ensure matrix is filled
        if self.score_matrix[self.n][self.m] == 0 and self.n > 0 and self.m > 0:
            self.fill_matrix()
            
        aligned_seq1 = ""
        aligned_seq2 = ""
        
        i = self.n
        j = self.m
        
        # Keep track of the cells visited for GUI highlighting
        path = [(i, j)]
        
        while i > 0 or j > 0:
            # If we reach the top row, we can only go left
            if i == 0:
                aligned_seq1 += "-"
                aligned_seq2 += self.seq2[j-1]
                j -= 1
            # If we reach the first column, we can only go up
            elif j == 0:
                aligned_seq1 += self.seq1[i-1]
                aligned_seq2 += "-"
                i -= 1
            else:
                directions = self.traceback_matrix[i][j]
                
                # In case of ties, we arbitrarily pick the first direction recorded
                # Typically prefer Diagonal > Up > Left
                if "D" in directions:
                    aligned_seq1 += self.seq1[i-1]
                    aligned_seq2 += self.seq2[j-1]
                    i -= 1
                    j -= 1
                elif "U" in directions:
                    aligned_seq1 += self.seq1[i-1]
                    aligned_seq2 += "-"
                    i -= 1
                elif "L" in directions:
                    aligned_seq1 += "-"
                    aligned_seq2 += self.seq2[j-1]
                    j -= 1
            
            path.append((i, j))
            
        # The sequences are built backwards, so reverse them
        aligned_seq1 = aligned_seq1[::-1]
        aligned_seq2 = aligned_seq2[::-1]
        
        # Generate match string
        match_str = ""
        matches = 0
        mismatches = 0
        gaps = 0
        
        for char1, char2 in zip(aligned_seq1, aligned_seq2):
            if char1 == char2 and char1 != '-':
                match_str += "|"
                matches += 1
            elif char1 == '-' or char2 == '-':
                match_str += " "
                gaps += 1
            else:
                match_str += " "
                mismatches += 1
                
        final_score = self.score_matrix[self.n][self.m]
        
        return {
            "seq1": aligned_seq1,
            "match_str": match_str,
            "seq2": aligned_seq2,
            "score": final_score,
            "path": path,
            "stats": {
                "matches": matches,
                "mismatches": mismatches,
                "gaps": gaps
            }
        }
