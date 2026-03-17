# NexusAI Intern Challenge

This project implements a simplified AI-powered telecom customer support system. It demonstrates async programming, AI integration, database design, and decision-making logic.

---

## 📁 Project Structure

```
nexusai-intern-challenge/
│
├── task1/  # AI Message Handler
├── task2/  # Database Schema & Repository
├── task3/  # Parallel Data Fetcher
├── task4/  # Escalation Decision Engine
├── ANSWERS.md
├── README.md
├── requirements.txt
```

---

## 🚀 Task Overview

### ✅ Task 1 — AI Message Handler

* Async function to process customer messages
* Uses Groq API (LLaMA 3.1 model)
* Handles:

  * Empty input validation
  * Timeout (10 seconds)
  * Retry logic for rate limits
* Returns structured response using dataclass

---

### ✅ Task 2 — Database Schema

* PostgreSQL table: `call_records`
* Includes:

  * Constraints for CSAT (1–5) and confidence (0–1)
  * Indexed columns for performance
* Async repository using `asyncpg`
* Parameterized queries for security

---

### ✅ Task 3 — Parallel Data Fetcher

* Simulates:

  * CRM system
  * Billing system
  * Ticket history
* Implements:

  * Sequential vs Parallel fetching
  * `asyncio.gather()` for concurrency
  * Error handling with partial results
* Demonstrates performance improvement (~2x faster)

---

### ✅ Task 4 — Escalation Decision Engine

* Rule-based system to decide escalation
* Handles:

  * Low confidence
  * Angry customers
  * Repeated complaints
  * VIP + billing issues
  * Service cancellation
* Returns decision with reason

---

### ✅ Task 5 — Design Answers

* Covers system design decisions
* Tradeoffs and improvements discussed in `ANSWERS.md`

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```
git clone <your-repo-link>
cd nexusai-intern-challenge
```

---

### 2. Install Dependencies

```
pip install -r requirements.txt
```

---

### 3. Set API Key (Groq)

**Windows:**

```
set GROQ_API_KEY=your_api_key_here
```

**Mac/Linux:**

```
export GROQ_API_KEY=your_api_key_here
```

---

### 4. Run Tasks

#### Task 1

```
cd task1
python handler.py
```

#### Task 3

```
cd task3
python fetcher.py
```

#### Task 4

```
cd task4
python decision_engine.py
```

---

## 🧠 Design Decisions

* Used async programming for better performance and scalability
* Implemented retry and timeout for robust API handling
* Designed database with constraints and indexes for reliability
* Used rule-based escalation for transparency and control

---

## ⚠️ Notes

* Task 2 uses PostgreSQL schema but does not require a live DB for demonstration
* API key is required only for Task 1
* Mock confidence values are used for simplicity

---

## 💡 Future Improvements

* Replace mock confidence with real model scoring
* Add authentication and logging
* Integrate real database connection
* Improve intent classification using NLP models

---

## 👨‍💻 Author

Abhilash Addagatla
