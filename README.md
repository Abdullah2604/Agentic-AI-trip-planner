# Agentic AI Trip Planner - Complete Setup Guide

This guide will walk you through running the entire project step-by-step, assuming you're new to this.

## ✅ Quick Checklist

Follow these steps in order:

- [ ] **Step 1:** Open terminal and navigate to project folder
- [ ] **Step 2:** Activate virtual environment (`.\venv\Scripts\Activate.ps1`)
- [ ] **Step 3:** Install Python dependencies (`pip install -r requirements.txt`)
- [ ] **Step 4:** (Optional) Create `.env` file for API keys
- [ ] **Step 5:** Start backend server (`uvicorn backend.app.main:app --reload --port 8000`)
- [ ] **Step 6:** Open NEW terminal, go to `frontend` folder
- [ ] **Step 7:** Install frontend dependencies (`npm install`)
- [ ] **Step 8:** Start frontend server (`npm run dev`)
- [ ] **Step 9:** Open browser to http://localhost:5173

**💡 Tip:** Want even faster? Use the batch scripts: `start_backend.bat` and `start_frontend.bat` (see QUICK_START.md)

---

## 📋 Prerequisites

Before starting, make sure you have:
- **Python 3.8+** installed (check with `python --version` in terminal)
- **Node.js and npm** installed (check with `node --version` and `npm --version`)
- A terminal (PowerShell, Command Prompt, or Git Bash)

---

## 🚀 Step-by-Step Setup

### **STEP 1: Open Your Terminal**

1. Open **PowerShell** or **Command Prompt**
2. Navigate to your project folder:
   ```powershell
   cd "C:\Users\mahme\Downloads\Capstone project"
   ```
   *(Replace with your actual project path if different)*

---

### **STEP 2: Activate the Virtual Environment (venv)**

The virtual environment (venv) is like a separate Python workspace for this project. You **must** activate it before running anything.

#### **In PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

#### **In Command Prompt (cmd):**
```cmd
venv\Scripts\activate.bat
```

#### **In Git Bash:**
```bash
source venv/Scripts/activate
```

**✅ Success indicator:** You should see `(venv)` at the start of your terminal prompt, like this:
```
(venv) PS C:\Users\mahme\Downloads\Capstone project>
```

**⚠️ If you get an error** about execution policy in PowerShell, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activating again.

---

### **STEP 3: Install Python Dependencies**

While your venv is activated (you should see `(venv)`), install all required Python packages:

```powershell
pip install -r requirements.txt
```

This will take a few minutes. Wait until you see "Successfully installed..." messages.

**✅ Check it worked:** Try importing a package:
```powershell
python -c "import fastapi; print('FastAPI installed!')"
```

---

### **STEP 4: (Optional) Create .env File**

The app can run without this, but if you want to use real LLM APIs later, create a `.env` file in the project root:

1. Create a file named `.env` (no extension, just `.env`)
2. Add these lines (replace with your actual API key):
   ```
   SQLITE_PATH=db.sqlite
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

   **To get a Gemini API key:**
   - Go to https://makersuite.google.com/app/apikey
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the key and paste it in your `.env` file

**Note:** If you skip this step, the app will work with basic rule-based responses (no AI). With a Gemini key, you'll get intelligent AI-generated itineraries!

---

### **STEP 5: Start the Backend Server**

Keep your venv activated and run:

```powershell
uvicorn backend.app.main:app --reload --port 8000
```

**✅ Success indicator:** You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**🎉 The backend is now running!** Keep this terminal window open.

**Test it:** Open your browser and go to:
- **API Docs:** http://localhost:8000/docs
- **Alternative docs:** http://localhost:8000/redoc

You should see a Swagger UI where you can test the API endpoints.

---

### **STEP 6: Open a NEW Terminal for the Frontend**

**Important:** Keep the backend terminal running, and open a **second terminal window**.

1. Open a new PowerShell/Command Prompt window
2. Navigate to the project folder again:
   ```powershell
   cd "C:\Users\mahme\Downloads\Capstone project"
   ```
3. Navigate into the frontend folder:
   ```powershell
   cd frontend
   ```

---

### **STEP 7: Install Frontend Dependencies**

In your new terminal (in the `frontend` folder), install Node.js packages:

```powershell
npm install
```

This will take a few minutes. Wait for "added X packages" message.

**✅ Check it worked:** You should see a `node_modules` folder created in `frontend/`.

---

### **STEP 8: Start the Frontend Development Server**

Still in the `frontend` folder, run:

```powershell
npm run dev
```

**✅ Success indicator:** You should see output like:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**🎉 The frontend is now running!**

---

### **STEP 9: Open the App in Your Browser**

Open your browser and go to: **http://localhost:5173**

You should see the Trip Planner interface!

---

## 🧪 Testing the App

1. **In the browser** (http://localhost:5173):
   - Type a prompt like: *"I want to visit Dubai for 3 days, I love shopping and modern architecture"*
   - Click **"Plan my trip"**
   - Wait a few seconds
   - You should see:
     - An itinerary text description
     - Day-by-day activity cards
     - A map with markers showing the attractions

2. **Test the API directly** (http://localhost:8000/docs):
   - Click on `POST /plan`
   - Click "Try it out"
   - Enter: `{"prompt": "Dubai 2 days shopping"}`
   - Click "Execute"
   - See the JSON response

---

## 🛑 How to Stop Everything

- **Stop the backend:** Go to the backend terminal and press `Ctrl + C`
- **Stop the frontend:** Go to the frontend terminal and press `Ctrl + C`
- **Deactivate venv** (optional): Type `deactivate` in the terminal

---

## 📁 Project Structure Overview

```
Capstone project/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── main.py      # Main API server
│   │   ├── models.py    # Database models
│   │   ├── schemas.py   # API request/response schemas
│   │   ├── services/    # Business logic
│   │   └── ranker/      # ML ranking engine
│   └── tests/           # Unit tests
├── frontend/            # React TypeScript frontend
│   ├── src/
│   │   ├── App.tsx      # Main React component
│   │   └── components/  # UI components
│   └── package.json     # Node.js dependencies
├── requirements.txt     # Python dependencies
├── venv/               # Python virtual environment
└── db.sqlite           # SQLite database (created on first run)
```

---

## 🐛 Troubleshooting

### **"uvicorn: command not found"**
- Make sure venv is activated (you see `(venv)` in prompt)
- Run: `pip install uvicorn` again

### **"npm: command not found"**
- Install Node.js from https://nodejs.org/
- Restart your terminal after installing

### **Backend won't start / Port 8000 already in use**
- Change the port: `uvicorn backend.app.main:app --reload --port 8001`
- Update frontend API URL in `frontend/src/App.tsx` (change `8000` to `8001`)

### **Frontend can't connect to backend**
- Make sure backend is running (check http://localhost:8000/docs)
- Check that the API URL in `frontend/src/App.tsx` matches your backend port

### **Database errors**
- Delete `db.sqlite` if it exists
- Restart the backend (it will recreate the database)

### **"Module not found" errors**
- Make sure venv is activated
- Run `pip install -r requirements.txt` again

---

## 🎯 Quick Reference Commands

**Activate venv:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Start backend:**
```powershell
uvicorn backend.app.main:app --reload --port 8000
```

**Start frontend (in new terminal, in frontend/ folder):**
```powershell
npm run dev
```

**Deactivate venv:**
```powershell
deactivate
```

---

## 📚 Next Steps

Once everything is running:
1. Try different trip prompts
2. Explore the API docs at http://localhost:8000/docs
3. Check the database: `db.sqlite` will be created in the project root
4. Customize the frontend UI in `frontend/src/`
5. Add more attractions in `backend/app/data/seed_dubai.py`

---

## 💡 Tips

- **Always activate venv** before running Python commands
- **Keep both terminals open** (backend + frontend) while developing
- **Use the API docs** (http://localhost:8000/docs) to test endpoints
- **Check terminal output** for error messages if something doesn't work

---

Happy coding! 🚀
#   A g e n t i c - A I - t r i p - p l a n n e r  
 