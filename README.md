# 🥡 Delcom

Delcom is a full-stack AI project that connects **user cravings** to **real delivery menu items**.  
It blends **natural language understanding**, **live menu scraping**, and **custom ranking logic** to recommend the best food delivery options — bringing intelligence to everyday ordering.

---

## 🚀 Overview

Built from the ground up with a **Python/FastAPI backend** and a **React/TypeScript frontend**, Delcom automatically:
- Interprets user cravings using OpenAI embeddings and prompt logic  
- Fetches live menus from delivery platforms via Playwright automation  
- Scores and ranks menu items by similarity, style, and keyword relevance  
- Displays the top matches through a responsive web interface  

This repository showcases the **architecture and implementation** of the system — isn't meant for self deployment, to test visit delcom.vercel.app

---

## 🧱 Project Structure

```
delcom/
├── delcom_backend/                # Backend (Python + FastAPI + Playwright + OpenAI)
│   ├── app/                       # Core backend logic
|   ├── authentication_util.py     # Playwright calls to gather session cookies
|   ├── main.py                    # FastAPI handling
│   ├── menu_scrape.py             # Delivery menu retrieval
│   ├── ranker.py                  # Embedding + similarity ranking
│   ├── gpt_test.py                # GPT encoding logic
│   ├── uber_parse_util.py         # Functions for parsing each different response from UberEats backend API
│   ├── requirements.txt           # Requirements.txt
│   ├── Dockerfile                 # Dockerfile for deployment 
│   └── .env (ignored)             # API keys and credentials
├── delcom_frontend/               # Frontend (React + TypeScript)
│   ├── src/
|   |   ├── components             # Webpage componests (.tsx)
|   |   └── pages                  # Pages (Home, Loading, Results)
│   └── package.json
├── docs/                    # Architecture notes / screenshots
├── .gitignore
└── README.md
```

---

## 🧠 Tech Stack

| Layer | Tools & Frameworks |
|-------|--------------------|
| **Frontend** | React, TypeScript, Vite |
| **Backend** | Python, FastAPI |
| **Automation** | Playwright |
| **AI / NLP** | OpenAI API (embeddings + LLM parsing) |

---

## 📸 UI Preview

*(Screenshots / demo images can go here if desired)*

```markdown
![Delcom UI](docs/ui-home.png)
![Search results](docs/results.png)
```

---

## 🔍 Highlights

- **LLM-powered craving understanding** — interprets vague inputs like "something spicy and fried"
- **Cross-platform menu scraping** — pulls data from UberEats using backend API reverse engineering
- **Real-time progress feedback** — frontend updates while backend fetches results
- **Ranking pipeline** — embedding comparisons used to find precise matches
- **From-scratch architecture** — full design, build, and deployment by a single developer

---

## 🧾 Note

This repository is intended for showcasing implementation and architecture.  
Environment files, API keys, and deployment credentials are intentionally excluded.  
Running the full system locally is not required or supported.

## 💬 Contact

**William Nyman**  
[GitHub](#) • [LinkedIn](#)
