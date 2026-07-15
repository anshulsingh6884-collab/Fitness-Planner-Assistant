"""Core 'AI' planning engine.

No external API calls needed — this is a self-contained rule/formula based
recommendation engine (Mifflin-St Jeor for calories, a simple split-selection
algorithm for workouts). Swap `generate_workout_plan` / `generate_diet_plan`
for real LLM calls later if you want smarter, more varied plans.
"""

import random
from app.data import EXERCISES, FOODS, REST_DAY_TIPS

ACTIVITY_MULTIPLIERS = {
    "Sedentary (little/no exercise)": 1.2,
    "Lightly active (1-3 days/week)": 1.375,
    "Moderately active (3-5 days/week)": 1.55,
    "Very active (6-7 days/week)": 1.725,
}

GOAL_CALORIE_ADJUST = {
    "Lose Weight": -500,
    "Maintain Weight": 0,
    "Gain Muscle": 300,
}

WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)


def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Healthy"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    # Mifflin-St Jeor Equation
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    return base + 5 if gender == "Male" else base - 161


def calculate_tdee(bmr: float, activity_level: str) -> float:
    return bmr * ACTIVITY_MULTIPLIERS.get(activity_level, 1.375)


def calculate_targets(profile: dict) -> dict:
    """Returns bmi, bmr, tdee, calorie target and macro breakdown (g)."""
    bmi = calculate_bmi(profile["weight"], profile["height"])
    bmr = calculate_bmr(profile["weight"], profile["height"], profile["age"], profile["gender"])
    tdee = calculate_tdee(bmr, profile["activity_level"])
    calorie_target = tdee + GOAL_CALORIE_ADJUST.get(profile["goal"], 0)
    calorie_target = max(calorie_target, 1200)  # safety floor

    # Protein: higher for muscle gain, moderate for others
    protein_per_kg = 2.0 if profile["goal"] == "Gain Muscle" else 1.8
    protein_g = protein_per_kg * profile["weight"]
    protein_cal = protein_g * 4

    fat_cal = calorie_target * 0.25
    fat_g = fat_cal / 9

    carb_cal = max(calorie_target - protein_cal - fat_cal, 0)
    carb_g = carb_cal / 4

    return {
        "bmi": bmi,
        "bmi_category": bmi_category(bmi),
        "bmr": round(bmr),
        "tdee": round(tdee),
        "calorie_target": round(calorie_target),
        "protein_g": round(protein_g),
        "fat_g": round(fat_g),
        "carb_g": round(carb_g),
    }


def _choose_split(days_per_week: int) -> list:
    """Return a list of category keys (one per workout day) for the week."""
    if days_per_week <= 3:
        return ["full_body"] * days_per_week
    if days_per_week == 4:
        return ["upper", "lower", "upper", "lower"]
    if days_per_week == 5:
        return ["push", "pull", "legs", "upper", "lower"]
    # 6 or 7
    return ["push", "pull", "legs", "push", "pull", "legs"]


def generate_workout_plan(profile: dict) -> dict:
    """Returns {day_name: {"type": str, "exercises": [(name, sets, reps), ...]}}"""
    days_per_week = profile["workout_days"]
    split = _choose_split(days_per_week)
    goal = profile["goal"]

    plan = {}
    workout_day_indices = sorted(random.sample(range(7), days_per_week)) if days_per_week < 7 else list(range(7))

    split_idx = 0
    for i, day in enumerate(WEEK_DAYS):
        if i in workout_day_indices:
            category = split[split_idx % len(split)]
            split_idx += 1
            exercises = list(EXERCISES[category])
            # Fat loss goal: add a cardio finisher
            if goal == "Lose Weight":
                exercises = exercises[:5] + [random.choice(EXERCISES["cardio"])]
            plan[day] = {
                "type": category.replace("_", " ").title(),
                "exercises": exercises,
            }
        else:
            plan[day] = {"type": "Rest / Active Recovery", "exercises": [(random.choice(REST_DAY_TIPS), "-", "-")]}
    return plan


def _pick_meals(diet_pref: str) -> dict:
    key = {"Vegetarian": "veg", "Non-Vegetarian": "non_veg", "Vegan": "vegan"}.get(diet_pref, "veg")
    foods = FOODS[key]
    return {
        "Breakfast": random.choice(foods["breakfast"]),
        "Lunch": random.choice(foods["lunch"]),
        "Dinner": random.choice(foods["dinner"]),
        "Snacks": random.choice(foods["snacks"]),
    }


def generate_diet_plan(profile: dict, targets: dict) -> dict:
    """Returns meal suggestions + approximate calorie split per meal."""
    calorie_target = targets["calorie_target"]
    meals = _pick_meals(profile["diet_pref"])
    split_pct = {"Breakfast": 0.25, "Lunch": 0.35, "Dinner": 0.30, "Snacks": 0.10}
    return {
        meal: {
            "suggestion": item,
            "approx_calories": round(calorie_target * split_pct[meal]),
        }
        for meal, item in meals.items()
    }
