# Strive AI - Fitness Planner

A desktop fitness planner app built with Python. You fill in some basic info about yourself (age, weight, height, goal, activity level) and it works out a daily calorie target, a weekly workout split, and a diet plan for you. There's also a small offline assistant tab you can ask fitness-related questions to.

I built this as a personal project to combine a bit of nutrition science (Mifflin-St Jeor formula for BMR/TDEE) with a simple rule-based recommendation system, wrapped in a clean desktop UI using CustomTkinter.

![Python](https://img.shields.io/badge/python-3.9+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## What it does

- **Profile setup** - enter your age, weight, height, gender, activity level, goal (lose weight / maintain / gain muscle), diet preference, and how many days a week you want to train.
- **Dashboard** - shows your BMI, BMR, TDEE, daily calorie target, and a protein/carbs/fat breakdown.
- **Workout plan** - automatically builds a weekly split (Full Body, Upper/Lower, or Push/Pull/Legs depending on how many days you picked) with sets and reps for each exercise.
- **Diet plan** - suggests meals for breakfast, lunch, dinner and snacks based on your diet preference (veg / non-veg / vegan), with an approximate calorie split per meal.
- **AI Assistant** - a simple chat tab that answers common questions (protein intake, hydration, sleep, motivation, plateaus, etc.) using your own numbers from the Dashboard.
- Everything is saved locally to a JSON file, so your plan is still there next time you open the app.

## Why "AI" if there's no API call?

There's no external LLM being called here - I didn't want the app to depend on an API key or an internet connection to work. Instead it's a rule/formula based engine: BMR and TDEE come from the Mifflin-St Jeor equation, and the workout/diet logic picks from a set of exercise and food templates based on your goal and preferences.

If you want to hook it up to a real LLM (OpenAI, Anthropic, etc.) for more varied/natural plans and conversation, the two places to change are `generate_workout_plan()` / `generate_diet_plan()` in `app/planner.py`, and `get_response()` in `app/assistant.py`. Everything else (the UI, the storage) stays the same.

## Screenshots

**Dashboard** - BMI, BMR, TDEE, calorie target and macro breakdown at a glance.

![Dashboard](screenshots/dashboard.png)

**Workout plan** - a weekly split generated based on your goal and how many days you picked.

![Workout plan](screenshots/workout-plan.png)

**Diet plan** - meal suggestions with an approximate calorie split per meal.

![Diet plan](screenshots/diet-plan.png)

**AI Assistant** - ask it about protein, calories, sleep, motivation, and more.

![AI Assistant](screenshots/assistant.png)

## Tech stack

- Python 3.9+
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the UI
- Plain JSON for local storage (no database needed)

## Getting started

Clone the repo and install the one dependency:

```bash
git clone https://github.com/<your-username>/strive-ai-fitness-planner.git
cd strive-ai-fitness-planner
pip install -r requirements.txt
```

Then run it:

```bash
python main.py
```

Fill in the Profile tab and hit **Generate My AI Plan**. That's it.

## Project structure

```
fitness_ai_planner/
├── main.py                # entry point
├── requirements.txt
└── app/
    ├── gui.py              # CustomTkinter UI - sidebar + all screens
    ├── planner.py          # BMI/BMR/TDEE math + workout/diet generation
    ├── assistant.py        # rule-based offline assistant
    ├── data.py             # exercise & food database
    └── storage.py          # saves/loads your plan to ~/.fitness_ai_planner/data.json
```

## Roadmap / ideas

Things I might add later, or feel free to open a PR:

- [ ] Weight log over time with a progress chart
- [ ] Multiple saved profiles
- [ ] Export your plan as a PDF
- [ ] Water/workout reminders
- [ ] Optional LLM integration for smarter, more varied plans

## Contributing

Open an issue or a PR if you spot a bug or want to add something. Nothing formal here, just keep it reasonably clean.

## License

MIT - do whatever you want with it.
