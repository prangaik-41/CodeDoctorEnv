---
title: CodeDoctor OpenEnv
emoji: 🧑‍💻
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# 🧑‍💻 CodeDoctor — AI Code Review Environment (OpenEnv)

## 🚀 Overview
This project implements a deterministic reinforcement learning environment that simulates real-world code review and debugging workflows.

The agent is tasked with:
* Identifying bugs in code
* Fixing the code correctly
* Explaining the issue clearly

⚠️ This is NOT a code execution system. It is a structured simulation for evaluating reasoning and debugging ability.

---

## 🎯 Objective
Given a buggy code snippet, the agent must:
1. Produce a correct fix
2. Provide a clear explanation of the issue

---

## 🧠 Environment Design

### 🔁 Single-Episode Decision Process
Each task represents a realistic debugging scenario:
* The agent receives buggy code
* The agent proposes a fix and explanation
* The environment evaluates correctness and reasoning

---

## 📥 Observation Space

```json
{
  "task_id": "task_1_easy",
  "code": "print('Hello'",
  "description": "Fix syntax error and explain the issue",
  "difficulty": "easy"
}
```

---

## 🎮 Action Space

```json
{
  "code_fix": "print('Hello')",
  "explanation": "Missing closing parenthesis"
}
```

---

## 🧩 Tasks

* **🟢 Easy — Syntax Error**: Simple syntax issues such as missing brackets or typos
* **🟡 Medium — Logic Bug**: Incorrect logic (e.g., wrong operators or flawed conditions)
* **🔴 Hard — Optimization / Refactor**: Inefficient code that must be improved for readability or performance

---

## 🏆 Reward Design

| Component | Reward |
|-----------|--------|
| Correct fix | +0.6 |
| Correct explanation | +0.3 |
| Optimization improvement | +0.1 |
| Partial correctness | +0.2 |
| Incorrect | 0.0 |

👉 The reward system provides partial feedback and emphasizes both correctness and reasoning.

---

## 🧪 Grading

Final score is normalized between 0.0 and 1.0:
* **1.0** → Fully correct fix with explanation
* **0.7** → Mostly correct with minor issues
* **0.3** → Partial understanding
* **0.0** → Incorrect solution

---

## 🤖 Baseline Agent

A deterministic fallback policy is used to ensure reproducibility:
* Matches task type (easy / medium / hard)
* Returns predefined fixes and explanations
* Ensures consistent baseline performance

---

## ⚙️ Setup & Run

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Run API**
```bash
uvicorn api.main:app --reload --port 7860
```

3. **Open API docs**
Navigate to `http://localhost:7860/docs` in your browser.

---

## 🐳 Docker

```bash
docker build -t code-doctor-env .
docker run -p 7860:7860 code-doctor-env
```

---

## 📊 Baseline Score

Typical baseline performance:
~`0.60 – 0.90` depending on task

---

## 🌍 Motivation

Code review is a critical part of software development where:
* Bugs must be identified quickly
* Fixes must be correct and safe
* Explanations improve team understanding

This environment simulates these real-world requirements in a deterministic and testable framework.

---

## ✅ Key Features

* Deterministic and reproducible
* Real-world developer workflow simulation
* Combined evaluation of correctness + reasoning
* Partial reward shaping for better learning signals
* OpenEnv compliant

---

## 🏁 Conclusion

This project demonstrates how reinforcement learning environments can model real-world developer workflows while remaining:
* Practical
* Interpretable
* Scalable for evaluation of AI coding agents
