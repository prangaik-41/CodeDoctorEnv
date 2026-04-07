# CodeDoctorEnv

CodeDoctorEnv is an OpenEnv-compliant reinforcement learning environment where an AI agent assumes the role of a *Code Reviewer*. The agent evaluates buggy code snippets, provides a corrected `code_fix`, and justifies the changes via an `explanation`.

## Motivation
With the rise of large language models for code synthesis, there is a critical need to evaluate an LM's ability to **review, explain, and repair** existing codebases rather than just generate code from scratch. CodeDoctorEnv tests this direct ability with clear deterministic grading logic.

## Spaces

### Observation Space
The initial state when resetting (`/reset`) or after executing the `/step` endpoint yields a `CodeDoctorObservation` containing:
- `task_id`: String identifier for the bug task.
- `code`: The buggy code.
- `description`: Instructions on what needs to be fixed.
- `difficulty`: Categorical difficulty rating (`EASY`, `MEDIUM`, `HARD`).

### Action Space
The agent responds with a `CodeDoctorAction` containing:
- `code_fix` (string): The corrected implementation.
- `explanation` (string): An explanation analyzing the problem and the change.

### Reward Function
The reward dynamically assigns values between 0.0 and 1.0 per task based on exact validation:
- Correct code fix matches underlying AST-like heuristics snippets → +0.6
- The quality of the explanation matching core keywords → Up to +0.3
- Identifying a partial fix → +0.2 max
- No correct snippet and poor explanation → 0.0

## Tasks
The environment features 3 distinct, strictly deterministic tasks evaluating syntax, functional, and pythonic logic errors:
- **EASY** (`task_1_easy`): Fix a basic python syntax error (missing parentheses).
- **MEDIUM** (`task_2_medium`): Fix a logical mathematical bug inside a function block.
- **HARD** (`task_3_hard`): Optimize code by migrating from raw index iteration `range(len())` to direct element iteration in python.

## Setup Instructions

This environment uses FastAPI to expose an OpenEnv compliant REST API structure on port `7860`.

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Server:**
   ```bash
   uvicorn api.main:app --host 0.0.0.0 --port 7860
   ```
   Or use the provided Dockerfile:
   ```bash
   docker build -t code-doctor-env .
   docker run -p 7860:7860 code-doctor-env
   ```

## Baselines & Inference

An autonomous evaluation script is included in `inference.py`. It integrates openly via the `OpenAI` standard Python client targeting Hugging Face Spaces.

To evaluate:
```bash
export API_BASE_URL="https://api-inference.huggingface.co/v1/"
export MODEL_NAME="mistralai/Mistral-7B-Instruct-v0.2" # or any compatible model
export HF_TOKEN="<your token>"

python inference.py
```

The script mandates execution using standard OpenEnv outputs adhering exactly to the rules:
```
[START] task=... env=... model=...
[STEP] step=1 action=... reward=... done=... error=null
[END] success=... steps=1 score=... rewards=...
```
