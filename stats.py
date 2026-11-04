"""Shared data and input helpers used by the other files.

Every file that imports stats sees the same dictionaries, so changes made in
one file show up everywhere. Keep this file free of imports from the other
project files to avoid circular imports.
"""

# Running calorie totals
daily = {"eaten": 0, "burned": 0}
weekly = {"eaten": 0, "burned": 0}

# The user's saved info (None means not filled in yet)
profile = {
    "age": None,
    "sex": None,
    "weight_lbs": None,
    "height_in": None,
    "activity_level": None,
}

# The user's saved weight plan, for a future feature
plan = {
    "goal_weight": None,
    "deadline_days": None,
    "maintenance": None,
    "daily_target": None,
}


def ask_int(question):
    """Ask the user a question and keep asking until they enter a whole number."""
    while True:
        answer = input(question).strip()
        try:
            return int(answer)   # return exits the loop and the function
        except ValueError:       # the answer wasn't a whole number, like "abc" or "2.5"
            print("Invalid input. Please enter a whole number.")


def ask_positive(question):
    """Ask until the user enters a positive number."""
    while True:
        try:
            number = float(input(question).strip())   # float allows decimals
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue   # skip the positive check and ask again
        if number > 0:
            return number
        print("Invalid input. Please enter a positive number.")