# Delcom

Delcom is a full-stack project that automates food ordering and matches user cravings to menu items using AI. It combines a Python backend using Playwright and OpenAI with a frontend (e.g., React) user interface.

---

## 🔧 Project Structure

```
delcom/
├── delcom_backend/       # Python backend (Playwright, OpenAI)
│   ├── gpt_test.py
│   ├── menu_scrape.py
│   ├── playwright_test.py
│   ├── .env              # API keys (not tracked in git)
│   └── requirements.txt
├── delcom_frontend/      # Frontend (React app)
│   └── ...               # React files
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### Backend

1. Navigate to the backend directory:
   ```bash
   cd delcom_backend
   ```

2. Create and activate a virtual environment:
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file:
   ```ini
   OPENAI_API_KEY=your-openai-api-key-here
   ```

---

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd delcom_frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the app:
   ```bash
   npm start
   ```

---

## 📦 .gitignore

Make sure the following are ignored by Git (already included in `.gitignore`):

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
env/
venv/
.env

# Node
node_modules/
build/
dist/
```

---

## 🧠 Tech Stack

- **Python**: Backend logic and automation  
- **Playwright**: Headless browser automation  
- **OpenAI API**: Natural language understanding  
- **React**: Frontend interface (assumed)  
- **dotenv**: Environment variable management  

---

## 📬 Contact

Created by [@williamnyman](https://github.com/williamnyman)
