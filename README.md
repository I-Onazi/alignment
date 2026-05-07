# Needleman-Wunsch Global Alignment Application

A professional bioinformatics web application that computes the optimal global alignment between two sequences (DNA, RNA, or Protein) using the Needleman-Wunsch algorithm.

## Features
- **Educational UI**: Animates the initialization, matrix filling, and traceback phases dynamically to teach dynamic programming concepts.
- **Robust Validation**: Automatically detects and validates strict biological sequences (DNA, RNA, Protein).
- **Customizable Scoring**: User-editable match, mismatch, and gap penalty scores.
- **Render Ready**: Built with FastAPI and vanilla web technologies to allow easy deployment on cloud hosts like Render.

## Tech Stack
- **Backend**: Python 3.10+, FastAPI, Pydantic
- **Frontend**: Vanilla HTML5, CSS3, ES6 JavaScript
- **Algorithm**: Needleman-Wunsch (Dynamic Programming)

## Project Architecture
```text
nw_alignment_gui/
├── main.py                   # FastAPI server entry point
├── requirements.txt          # Python dependencies
├── alignment/                # Core bioinformatics logic
│   ├── needleman_wunsch.py   # Matrix engine and traceback
│   └── validator.py          # Biological string validation
├── static/                   # Frontend assets
│   ├── index.html            # Web interface
│   ├── app.js                # UI logic and API calls
│   └── styles.css            # Dark mode Catppuccin theme
└── tests/                    # Pytest unit tests
    ├── test_algorithm.py
    └── test_validation.py
```

## Local Installation

1. Clone or download the repository.
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --port 8080
   ```
4. Open your web browser and navigate to: `http://localhost:8080`

## Testing
To run the automated tests, ensure you have `pytest` installed, and then run:
```bash
pytest tests/
```

## Algorithm Explanation
The Needleman-Wunsch algorithm finds the optimal global alignment between two strings by breaking the problem into overlapping subproblems using dynamic programming.
1. **Matrix Initialization**: Populating the edge boundaries with cumulative gap penalties.
2. **Matrix Filling**: Evaluating the cost of aligning characters (Diagonal), or introducing gaps (Up/Left), and storing the maximum score at each cell.
3. **Traceback**: Following the optimal recorded pointers from the final cell backwards to the start to reconstruct the highest-scoring alignment.
