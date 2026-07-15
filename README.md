# Strive AI — Fitness Planner (Desktop App)

Python desktop app (CustomTkinter) jo tumhare profile se **AI-based workout +
diet plan** generate karta hai, aur ek **offline AI assistant** bhi deta hai
fitness questions ke liye. Koi internet/API key nahi chahiye — sab kuch
formula/rule-based engine se locally chalta hai.

## Features
- **Profile tab** — age, weight, height, goal, activity level, diet
  preference, workout days/week
- **Dashboard** — BMI, BMR, TDEE, daily calorie target, protein/carb/fat
  macros (Mifflin-St Jeor formula use hota hai)
- **Workout Plan** — poore hafte ka split (Full Body / Upper-Lower / Push-Pull-Legs)
  tumhare workout days ke hisaab se automatically choose hota hai
- **Diet Plan** — Veg / Non-Veg / Vegan meal suggestions with calorie split
- **AI Assistant** — chat-style tab jo protein, calories, sleep, motivation,
  plateau jaise questions ka jawab deta hai (tumhare hi targets use karke)
- Data automatically save hota hai (`~/.fitness_ai_planner/data.json`) —
  app dobara kholo toh plan wapas load ho jayega

## Project Structure
```
fitness_ai_planner/
├── main.py                 # Entry point — python main.py
├── requirements.txt
└── app/
    ├── gui.py               # CustomTkinter UI (sidebar + all screens)
    ├── planner.py           # BMI/BMR/TDEE calc + workout/diet generation
    ├── assistant.py         # Rule-based offline AI assistant
    ├── data.py              # Exercise & food database
    └── storage.py           # Save/load local JSON data
```

## Run karne ke liye

1. Dependencies install karo:
   ```
   pip install -r requirements.txt
   ```

2. App run karo:
   ```
   python main.py
   ```

3. **Profile** tab me apni details bharo → **"Generate My AI Plan"** dabao →
   Dashboard, Workout Plan, Diet Plan automatically ban jayenge.

## Ise "asli AI" jaisa smart kaise banaye (optional upgrade)

Abhi ye ek **rule-based recommendation engine** hai (fast, offline, free).
Agar tum isko real LLM (OpenAI/Anthropic/Gemini) se connect karna chaho taaki
plans aur zyada varied/smart bane:

1. `app/planner.py` me `generate_workout_plan()` aur `generate_diet_plan()`
   ke andar, exercise database use karne ke bajaye ek API call kar sakte ho
   (user ka profile JSON banake prompt me bhejo, response parse karo).
2. `app/assistant.py` ke `get_response()` ko bhi isi tarah API call se
   replace kar sakte ho for more natural conversation.
3. API key ke liye `.env` file ya Settings tab add karna hoga.

Bata dena agar ye upgrade bhi chahiye — main wo bhi bana dunga.

## Next steps (agar chaho)
- Progress tracking (weight log over time, chart)
- Multiple saved profiles / login
- Export plan as PDF
- Reminders/notifications for water & workouts
