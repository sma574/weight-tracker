"""Weight predictor: estimate maintenance calories and how long reaching a goal weight takes.

The calculation functions have no input() or print(), so the website (app.py)
can reuse them. Only weight_predictor() talks to the user in the terminal.
"""

import math

import stats


# Settings used by the predictor
CALORIES_PER_LB = 3500      # about 3,500 calories = 1 lb of body weight
MIN_SAFE_INTAKE = 1200      # warn if a daily intake drops below this
MAX_LOSS_PER_WEEK = 2       # lbs; faster than this is aggressive
MAX_GAIN_PER_WEEK = 1       # lbs; faster than this is mostly fat gain
CHANGE_OPTIONS = (250, 500, 750)   # daily deficits/surpluses to compare

# How much each activity level raises daily calorie burn above resting
ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
}

# Shown to the user so they know which activity level to pick
ACTIVITY_DESCRIPTIONS = {
    "sedentary": "little or no exercise",
    "light": "exercise 1-3 days a week",
    "moderate": "exercise 3-5 days a week",
    "active": "hard exercise 6-7 days a week",
}

# The predictor's answers; separate from stats.profile because it's a one-off "what if"
test_profile = {
    "age": None,
    "sex": None,
    "weight_lbs": None,
    "height_in": None,
    "activity_level": None,
}


def estimate_maintenance(age, sex, weight_lbs, height_in, activity_level):
    """Estimate calories burned per day."""
    # Mifflin-St Jeor formula, converted to pounds and inches.
    # BMR is the calories burned at complete rest.
    bmr = 4.536 * weight_lbs + 15.875 * height_in - 5 * age
    if sex == "male":
        bmr += 5
    else:
        bmr -= 161
    # Multiply by activity level to get total calories burned per day
    return round(bmr * ACTIVITY_MULTIPLIERS[activity_level])


def days_to_goal(weight_lbs, goal_weight, maintenance, daily_intake):
    """Estimate days to reach the goal weight (losing or gaining), or None if it won't happen."""
    daily_change = maintenance - daily_intake     # positive = deficit, negative = surplus
    weight_to_lose = weight_lbs - goal_weight     # positive = losing, negative = gaining

    # No change, or eating in the wrong direction (like a surplus while trying to lose)
    if daily_change == 0 or (weight_to_lose > 0) != (daily_change > 0):
        return None

    # When bulking, both numbers are negative and cancel out to positive days.
    # math.ceil rounds up so any real progress shows at least 1 day.
    return math.ceil(weight_to_lose * CALORIES_PER_LB / daily_change)


def weight_after_days(weight_lbs, maintenance, daily_intake, days):
    """Estimate weight after a number of days. Eating above maintenance gives a higher weight."""
    change = (maintenance - daily_intake) * days / CALORIES_PER_LB
    return round(weight_lbs - change, 1)


def weight_predictor():
    """Ask for the user's stats, then show how long reaching a goal weight would take."""
    # Collect the user's info
    test_profile["age"] = int(stats.ask_positive("Enter your age: "))
    test_profile["weight_lbs"] = stats.ask_positive("Enter your weight (lbs): ")
    test_profile["height_in"] = stats.ask_positive("Enter your height (inches): ")

    # Keep asking until the answer is exactly "male" or "female"
    while True:
        sex = input("Enter your sex for calorie estimates (male/female): ").strip().lower()
        if sex in ("male", "female"):
            test_profile["sex"] = sex
            break
        print("Invalid input. Type 'male' or 'female'.")

    # Show the options, then keep asking until the answer is one of them
    print("\nActivity levels:")
    for level, description in ACTIVITY_DESCRIPTIONS.items():
        print(f"  {level}: {description}")
    while True:
        activity = input("Enter your activity level: ").strip().lower()
        if activity in ACTIVITY_MULTIPLIERS:
            test_profile["activity_level"] = activity
            break
        print("Invalid input. Type 'sedentary', 'light', 'moderate', or 'active'.")

    maintenance = estimate_maintenance(
        test_profile["age"],
        test_profile["sex"],
        test_profile["weight_lbs"],
        test_profile["height_in"],
        test_profile["activity_level"],
    )
    print(f"\nEstimated maintenance: about {maintenance} calories per day.")

    goal_weight = stats.ask_positive("Enter your goal weight (lbs): ")
    if goal_weight == test_profile["weight_lbs"]:
        print("You're already at your goal weight. Eat about your maintenance to stay there.")
        return   # exit early, back to the main menu

    # Losing needs a deficit (eat below maintenance); bulking needs a surplus (eat above)
    losing = goal_weight < test_profile["weight_lbs"]
    if losing:
        direction = "below"
        sign = -1
    else:
        direction = "above"
        sign = 1

    # Show the time to goal for each calorie option
    print("\nTime to reach your goal:")
    for amount in CHANGE_OPTIONS:
        daily_intake = maintenance + sign * amount
        days = days_to_goal(test_profile["weight_lbs"], goal_weight, maintenance, daily_intake)
        lbs_per_week = amount * 7 / CALORIES_PER_LB
        day_word = "day" if days == 1 else "days"
        print(f"{amount} calories {direction} maintenance ({daily_intake} per day): "
              f"about {days} {day_word} ({days / 7:.1f} weeks)")

        # Flag plans that are too low in calories or too fast
        if daily_intake < MIN_SAFE_INTAKE:
            print(f"  Warning: below {MIN_SAFE_INTAKE} calories a day is very low. Talk to a doctor first.")
        elif losing and lbs_per_week > MAX_LOSS_PER_WEEK:
            print(f"  Warning: losing over {MAX_LOSS_PER_WEEK} lbs a week is very aggressive.")
        elif not losing and lbs_per_week > MAX_GAIN_PER_WEEK:
            print(f"  Warning: gaining over {MAX_GAIN_PER_WEEK} lb a week is likely to add more fat than muscle.")

    print("\nThese are estimates. Real results vary from person to person.")