# 🚀 Quick Start Guide (Even Faster!)

If you want to skip the detailed instructions, use these **one-click startup scripts**:

## Option 1: Use the Batch Scripts (Easiest!)

### **Step 1: Start Backend**
Double-click `start_backend.bat` in the project folder.

Wait until you see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### **Step 2: Start Frontend** 
Open a **new** terminal/PowerShell window, navigate to the project folder, and double-click `start_frontend.bat`.

Or manually:
```powershell
cd frontend
npm install
npm run dev
```

### **Step 3: Open Browser**
Go to: **http://localhost:5173**

---

## Option 2: Manual Commands (If scripts don't work)

### Terminal 1 - Backend:
```powershell
cd "C:\Users\mahme\Downloads\Capstone project"
.\venv\Scripts\Activate.ps1
uvicorn backend.app.main:app --reload --port 8000
```

### Terminal 2 - Frontend:
```powershell
cd "C:\Users\mahme\Downloads\Capstone project\frontend"
npm install
npm run dev
```

---

## ✅ Verify It's Working

1. **Backend:** http://localhost:8000/docs (should show Swagger UI)
2. **Frontend:** http://localhost:5173 (should show trip planner UI)

---

## 🆘 Still Having Issues?

Read the full **README.md** for detailed troubleshooting!
