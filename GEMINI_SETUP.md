# 🔑 Setting Up Google Gemini API

The app now uses **Google Gemini** for AI-powered trip planning! Here's how to set it up:

## Step 1: Get Your Gemini API Key

1. Go to **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the API key (it will look like: `AIzaSy...`)

## Step 2: Add the Key to Your Project

1. In your project root folder, create a file named `.env` (if it doesn't exist)
2. Add this line:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
   
   Replace `your_actual_api_key_here` with the key you copied.

3. Save the file

## Step 3: Install the Gemini Package

Make sure you've installed the required package. In your activated venv, run:

```powershell
pip install google-generativeai
```

Or reinstall all requirements:

```powershell
pip install -r requirements.txt
```

## Step 4: Restart the Backend

1. Stop your backend server (Ctrl+C)
2. Start it again:
   ```powershell
   uvicorn backend.app.main:app --reload --port 8000
   ```

## ✅ Verify It's Working

1. Go to http://localhost:5173
2. Type a trip request like: *"I want to visit Dubai for 3 days, I love shopping and modern architecture"*
3. Click "Plan my trip"
4. You should see a **much more detailed and intelligent itinerary** compared to the basic template!

## 🎯 What Gemini Does

With Gemini enabled, the app will:
- **Intelligently extract** your preferences (destination, days, interests, budget) from natural language
- **Generate detailed itineraries** with:
  - Natural language descriptions
  - Suggested time windows for each activity
  - Helpful notes and tips
  - Logical grouping of nearby attractions

## 🆘 Troubleshooting

**"ModuleNotFoundError: No module named 'google.generativeai'"**
- Run: `pip install google-generativeai`

**"API key not found"**
- Make sure your `.env` file is in the project root (same folder as `requirements.txt`)
- Make sure the file is named exactly `.env` (not `.env.txt`)
- Restart the backend server after adding the key

**Still getting basic responses**
- Check that your API key is correct (no extra spaces)
- Check the backend terminal for error messages
- Verify the key works by testing it at https://makersuite.google.com/app/apikey

---

**Note:** The app will work without a Gemini key, but you'll get basic rule-based responses instead of AI-generated content.
