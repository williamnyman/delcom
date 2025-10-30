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

This repository showcases the **architecture and implementation** of the system — it’s meant for **reviewing the code**, not self-deployment.

---

## 🧱 Project Structure

delcom/
├── delcom_backend/ # Backend (Python + FastAPI + Playwright + OpenAI)
│ ├── app/ # Core backend logic
│ ├── menu_scrape.py # Delivery menu retrieval
│ ├── ranking.py # Embedding + similarity ranking
│ ├── gpt_test.py # Prompt experimentation
│ ├── requirements.txt
│ └── .env (ignored) # API keys and credentials
├── delcom_frontend/ # Frontend (React + TypeScript)
│ ├── src/
│ └── package.json
├── docs/ # Architecture notes / screenshots
├── .gitignore
└── README.md
---
## 🧠 Tech Stack

| Layer | Tools & Frameworks |
|-------|--------------------|
| **Frontend** | React, TypeScript, Vite |
| **Backend** | Python, FastAPI |
| **Automation** | Playwright |
| **AI / NLP** | OpenAI API (embeddings + LLM parsing) |
| **Hosting / Infra** | Vercel (frontend), Cloudflare Tunnel (backend) |
---

## 📸 UI Preview

*(Screenshots / demo images can go here if desired)*  
markdown
![Delcom UI](docs/ui-home.png)
![Search results](docs/results.png)


---

🔍 Highlights

LLM-powered craving understanding — interprets vague inputs like “something spicy and fried”

Cross-platform menu scraping — pulls data from multiple delivery sites simultaneously

Real-time progress feedback — frontend updates while backend fetches results

Custom ranking pipeline — blends embeddings with keyword heuristics for precise matches

From-scratch architecture — full design, build, and deployment by a single developer

🧾 Note

This repository is intended for showcasing implementation and architecture.
Environment files, API keys, and deployment credentials are intentionally excluded.
Running the full system locally is not required or supported.

🪪 License

© 2025 William Nyman. All rights reserved.

💬 Contact

William Nyman
GitHub
 • LinkedIn
