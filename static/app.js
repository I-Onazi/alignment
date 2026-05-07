document.addEventListener("DOMContentLoaded", () => {
    const seq1Input = document.getElementById("seq1");
    const seq2Input = document.getElementById("seq2");
    const btnRun = document.getElementById("btn-run");
    const btnClear = document.getElementById("btn-clear");
    const btnExample = document.getElementById("btn-example");
    
    const errorMsg = document.getElementById("validation-error");
    const successMsg = document.getElementById("validation-success");

    btnExample.addEventListener("click", () => {
        seq1Input.value = "GATTACA";
        seq2Input.value = "GCATGCU";
        validateInputs();
    });

    btnClear.addEventListener("click", () => {
        seq1Input.value = "";
        seq2Input.value = "";
        errorMsg.classList.add("hidden");
        successMsg.classList.add("hidden");
        document.getElementById("score-display").innerText = "Score: --";
        document.getElementById("alignment-display").innerText = "Run alignment...";
        document.getElementById("matrix-container").innerHTML = '<div class="placeholder-text">Enter sequences to initialize the matrix.</div>';
    });

    async function validateInputs() {
        const seq1 = seq1Input.value.trim().toUpperCase();
        const seq2 = seq2Input.value.trim().toUpperCase();

        if (!seq1 || !seq2) {
            showError("Both sequences must be provided.");
            return false;
        }

        try {
            const response = await fetch("/api/validate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ seq1, seq2 })
            });

            const data = await response.json();

            if (!response.ok) {
                showError(data.detail);
                return false;
            }

            showSuccess(`Detected ${data.type} sequences. Valid!`);
            return true;
        } catch (e) {
            showError("Network error during validation.");
            return false;
        }
    }

    function showError(msg) {
        errorMsg.innerText = msg;
        errorMsg.classList.remove("hidden");
        successMsg.classList.add("hidden");
    }

    function showSuccess(msg) {
        successMsg.innerText = msg;
        successMsg.classList.remove("hidden");
        errorMsg.classList.add("hidden");
    }

    // Input listeners to trigger validation automatically
    seq1Input.addEventListener("input", validateInputs);
    seq2Input.addEventListener("input", validateInputs);

    btnRun.addEventListener("click", async () => {
        const isValid = await validateInputs();
        if (isValid) {
            const seq1 = seq1Input.value.trim().toUpperCase();
            const seq2 = seq2Input.value.trim().toUpperCase();
            const matchScore = parseInt(document.getElementById("match-score").value);
            const mismatchScore = parseInt(document.getElementById("mismatch-score").value);
            const gapScore = parseInt(document.getElementById("gap-score").value);

            try {
                // Call the FILL endpoint to get the final matrix
                const response = await fetch("/api/fill", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ 
                        seq1: seq1, 
                        seq2: seq2,
                        match: matchScore,
                        mismatch: mismatchScore,
                        gap: gapScore
                    })
                });

                if (!response.ok) {
                    showError("Error calculating matrix.");
                    return;
                }

                const data = await response.json();
                
                // Animate rendering
                btnRun.disabled = true; // prevent re-clicking during animation
                document.getElementById("score-display").innerText = "Status: Calculating...";
                
                const cellRefs = await animateMatrixFill(data.matrix, data.rows, data.cols);
                
                document.getElementById("score-display").innerText = "Status: Calculating Traceback...";
                
                await animateTraceback(cellRefs, data.results.path);
                
                // Phase 8: Final Results Update
                document.getElementById("score-display").innerText = `Final Global Alignment Score: ${data.results.score}`;
                document.getElementById("alignment-display").innerText = `${data.results.seq1}\n${data.results.match_str}\n${data.results.seq2}\n\nStats -> Matches: ${data.results.stats.matches} | Mismatches: ${data.results.stats.mismatches} | Gaps: ${data.results.stats.gaps}`;
                
                btnRun.disabled = false;

            } catch (e) {
                showError("Network error during calculation.");
                btnRun.disabled = false;
            }
        }
    });

    async function animateMatrixFill(matrix, rowSeq, colSeq) {
        const container = document.getElementById("matrix-container");
        container.innerHTML = ""; // Clear existing

        const table = document.createElement("table");
        table.className = "dp-matrix";

        // Header row
        const headerRow = document.createElement("tr");
        headerRow.appendChild(createCell("th", "")); // empty top-left
        headerRow.appendChild(createCell("th", "Gap"));
        for (let j = 0; j < colSeq.length; j++) {
            headerRow.appendChild(createCell("th", colSeq[j]));
        }
        table.appendChild(headerRow);

        // Build data rows empty first (except bounds)
        const cellRefs = [];
        for (let i = 0; i < matrix.length; i++) {
            const row = document.createElement("tr");
            cellRefs[i] = [];
            
            // Row header
            if (i === 0) {
                row.appendChild(createCell("th", "Gap"));
            } else {
                row.appendChild(createCell("th", rowSeq[i-1]));
            }

            for (let j = 0; j < matrix[i].length; j++) {
                const cell = createCell("td", "");
                if (i === 0 || j === 0) {
                    cell.innerText = matrix[i][j];
                    cell.classList.add("init-cell");
                }
                cellRefs[i][j] = cell;
                row.appendChild(cell);
            }
            table.appendChild(row);
        }
        container.appendChild(table);

        // Calculate a reasonable animation delay based on matrix size
        // Max 50ms, minimum 1ms
        let delay = Math.max(1, Math.min(50, 1000 / (matrix.length * matrix[0].length)));

        // Animate internal cells
        for (let i = 1; i < matrix.length; i++) {
            for (let j = 1; j < matrix[i].length; j++) {
                // Highlight current cell
                cellRefs[i][j].classList.add("active-cell");
                
                // Sleep for animation effect
                await new Promise(r => setTimeout(r, delay)); 
                
                // Set value and remove highlight
                cellRefs[i][j].innerText = matrix[i][j];
                cellRefs[i][j].classList.remove("active-cell");
                cellRefs[i][j].classList.add("filled-cell");
            }
        }
        return cellRefs;
    }

    async function animateTraceback(cellRefs, path) {
        // Traceback path goes from bottom-right to top-left
        for (let k = 0; k < path.length; k++) {
            const [i, j] = path[k];
            
            // Add traceback path styling
            cellRefs[i][j].classList.add("traceback-cell");
            
            // Short delay to animate the path tracing backwards
            await new Promise(r => setTimeout(r, 100));
        }
    }

    function createCell(tag, text) {
        const el = document.createElement(tag);
        el.innerText = text;
        return el;
    }
});
