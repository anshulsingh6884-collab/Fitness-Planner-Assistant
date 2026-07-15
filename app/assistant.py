"""A lightweight, fully-offline rule-based 'AI assistant'.

Matches keywords in the user's question and responds using their own profile
/ targets where possible, so answers feel personalized without needing any
external API or internet connection.
"""

import random

GENERIC_TIPS = [
    "Consistency beats intensity — showing up regularly matters more than a perfect session.",
    "Sleep 7-9 hours; recovery is when your muscles actually grow.",
    "Track your workouts so you can progressively add weight/reps over time.",
]


def _fmt_targets(targets: dict) -> str:
    if not targets:
        return ""
    return (f"(Your targets: {targets['calorie_target']} kcal/day, "
            f"{targets['protein_g']}g protein, {targets['carb_g']}g carbs, {targets['fat_g']}g fat)")


def get_response(question: str, profile: dict, targets: dict) -> str:
    q = question.lower().strip()

    if not q:
        return "Ask me anything about your workouts, diet, or recovery!"

    if any(w in q for w in ["protein", "kitna protein"]):
        if targets:
            return (f"Based on your profile, aim for about {targets['protein_g']}g of protein a day. "
                     f"Spread it across meals — eggs, paneer, dal, chicken, tofu, or a protein shake all work well.")
        return "Generally aim for 1.6-2.2g of protein per kg of bodyweight per day. Fill in your profile for an exact number."

    if any(w in q for w in ["water", "hydration", "pani"]):
        return "Aim for roughly 3-4 litres of water a day, more on workout days or in hot weather. Keep a bottle with you as a reminder."

    if any(w in q for w in ["sleep", "neend", "rest"]):
        return "7-9 hours of quality sleep is when most muscle recovery & growth happens. Try to keep a consistent sleep schedule."

    if any(w in q for w in ["cardio", "running", "jog"]):
        return "2-3 sessions of 20-30 min cardio a week is great for heart health and fat loss, on top of your strength days."

    if any(w in q for w in ["plateau", "stuck", "not losing", "not gaining"]):
        return ("Plateaus are normal. Try: re-check your calorie target (your weight may have changed), "
                "add more protein, increase workout intensity slightly, and make sure you're sleeping enough. "
                f"{_fmt_targets(targets)}")

    if any(w in q for w in ["calorie", "calories", "kitni calorie"]):
        if targets:
            return f"Your current daily target is about {targets['calorie_target']} kcal to support your goal of {profile.get('goal', 'your goal')}."
        return "Generate your plan first (fill the Profile tab) and I'll calculate your exact calorie target."

    if any(w in q for w in ["motivat", "give up", "lazy", "no energy"]):
        return random.choice([
            "Small consistent effort beats occasional bursts. Even a short workout today keeps the streak alive.",
            "You don't need to feel motivated to start — starting is often what creates the motivation.",
            "Progress isn't always visible day to day. Trust the process and look back after 4 weeks.",
        ])

    if any(w in q for w in ["muscle", "bulk", "gain weight"]):
        return ("For muscle gain: eat in a slight calorie surplus, prioritize protein, and progressively overload "
                f"(add weight/reps over time) on your lifts. {_fmt_targets(targets)}")

    if any(w in q for w in ["fat loss", "lose weight", "cut", "slim"]):
        return ("For fat loss: stay in a moderate calorie deficit, keep protein high to preserve muscle, "
                f"and add 2-3 cardio sessions a week. {_fmt_targets(targets)}")

    if any(w in q for w in ["rest day", "off day"]):
        return "Rest days are important — light stretching, walking, or yoga helps recovery without adding fatigue."

    if any(w in q for w in ["hi", "hello", "hey", "namaste"]):
        return "Hey! I'm your fitness assistant. Ask me about protein, calories, workouts, diet, sleep, or motivation."

    # fallback
    return ("I'm a simple offline assistant, so I mainly know about workouts, diet, calories, and recovery. "
            f"Here's a general tip: {random.choice(GENERIC_TIPS)}")
