"""Static data: exercise library and food suggestions used by the planner."""

# ---------------------------------------------------------------------------
# Exercises grouped by category. Each entry: (name, default_sets, rep_range)
# ---------------------------------------------------------------------------
EXERCISES = {
    "push": [
        ("Push Ups", 4, "10-15"),
        ("Bench Press (or Dumbbell Press)", 4, "8-12"),
        ("Overhead Shoulder Press", 3, "8-12"),
        ("Incline Dumbbell Press", 3, "10-12"),
        ("Triceps Dips", 3, "10-15"),
        ("Lateral Raises", 3, "12-15"),
    ],
    "pull": [
        ("Pull Ups / Lat Pulldown", 4, "6-12"),
        ("Bent Over Rows", 4, "8-12"),
        ("Seated Cable Row", 3, "10-12"),
        ("Face Pulls", 3, "12-15"),
        ("Bicep Curls", 3, "10-15"),
        ("Deadlifts", 3, "5-8"),
    ],
    "legs": [
        ("Squats", 4, "8-12"),
        ("Lunges", 3, "10-12 each leg"),
        ("Romanian Deadlift", 3, "8-12"),
        ("Leg Press", 3, "10-15"),
        ("Calf Raises", 4, "15-20"),
        ("Glute Bridges", 3, "12-15"),
    ],
    "upper": [
        ("Push Ups", 3, "10-15"),
        ("Bent Over Rows", 3, "8-12"),
        ("Overhead Shoulder Press", 3, "8-12"),
        ("Pull Ups / Lat Pulldown", 3, "6-12"),
        ("Bicep Curls", 2, "10-15"),
        ("Triceps Dips", 2, "10-15"),
    ],
    "lower": [
        ("Squats", 4, "8-12"),
        ("Romanian Deadlift", 3, "8-12"),
        ("Lunges", 3, "10-12 each leg"),
        ("Calf Raises", 4, "15-20"),
        ("Glute Bridges", 3, "12-15"),
    ],
    "full_body": [
        ("Squats", 3, "10-12"),
        ("Push Ups", 3, "10-15"),
        ("Bent Over Rows", 3, "8-12"),
        ("Overhead Shoulder Press", 3, "8-12"),
        ("Plank", 3, "30-45 sec"),
        ("Glute Bridges", 3, "12-15"),
    ],
    "cardio": [
        ("Brisk Walk / Jog", 1, "20-30 min"),
        ("Jump Rope", 3, "2 min rounds"),
        ("Cycling", 1, "20-30 min"),
        ("HIIT Circuit", 1, "15-20 min"),
    ],
    "core": [
        ("Plank", 3, "30-45 sec"),
        ("Bicycle Crunches", 3, "15-20"),
        ("Leg Raises", 3, "12-15"),
        ("Russian Twists", 3, "15-20"),
    ],
}

REST_DAY_TIPS = [
    "Light stretching or a 20 min walk",
    "Foam rolling / mobility work",
    "Yoga (20-30 min) for recovery",
]

# ---------------------------------------------------------------------------
# Food suggestions by diet preference. Rough calorie/protein estimates per
# serving so the planner can pick items that roughly fit the target.
# ---------------------------------------------------------------------------
FOODS = {
    "veg": {
        "breakfast": [
            "Oats with milk, banana & peanut butter",
            "Poha with peanuts & sprouts",
            "Greek yogurt with fruits & granola",
            "Paneer bhurji with 2 multigrain toast",
        ],
        "lunch": [
            "Rajma/chole with brown rice & salad",
            "Paneer curry with 2 rotis & veggies",
            "Dal, rice, sabzi & curd",
            "Quinoa veggie bowl with tofu",
        ],
        "dinner": [
            "Grilled paneer with sauteed vegetables",
            "Moong dal khichdi with curd",
            "Soya chunk curry with roti",
            "Vegetable stir fry with tofu & brown rice",
        ],
        "snacks": [
            "Roasted chana",
            "Fruit + a handful of almonds",
            "Protein shake (plant based)",
            "Sprouts salad",
        ],
    },
    "non_veg": {
        "breakfast": [
            "3-4 egg omelette with toast",
            "Boiled eggs with oats",
            "Greek yogurt with fruits",
            "Chicken sausage with multigrain toast",
        ],
        "lunch": [
            "Grilled chicken breast with rice & salad",
            "Fish curry with brown rice",
            "Chicken breast wrap with veggies",
            "Egg curry with roti",
        ],
        "dinner": [
            "Grilled fish with steamed vegetables",
            "Chicken stir fry with brown rice",
            "Turkey/chicken mince bowl with veggies",
            "Prawn curry with a small portion of rice",
        ],
        "snacks": [
            "Boiled eggs",
            "Protein shake (whey)",
            "Roasted chana",
            "Greek yogurt",
        ],
    },
    "vegan": {
        "breakfast": [
            "Oats with almond milk, banana & flax seeds",
            "Tofu scramble with veggies",
            "Smoothie: banana, oats, peanut butter, plant milk",
            "Chickpea flour (besan) chilla",
        ],
        "lunch": [
            "Rajma/chole with brown rice",
            "Tofu stir fry with quinoa",
            "Lentil (dal) soup with roti & salad",
            "Buddha bowl: chickpeas, veggies, tahini",
        ],
        "dinner": [
            "Tofu & vegetable curry with rice",
            "Soya chunk curry with roti",
            "Lentil khichdi with sauteed greens",
            "Stir fried tempeh with vegetables",
        ],
        "snacks": [
            "Roasted chana",
            "Handful of mixed nuts",
            "Plant based protein shake",
            "Fruit + peanut butter",
        ],
    },
}
