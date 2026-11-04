"""Log calories eaten and burned, and keep running totals for the day."""

import stats


def daily_total():
    """Log calories for this meal, add them to the day's totals, and show both."""
    # This meal's totals start at 0 every time; the day's totals live in stats.daily
    eaten = 0
    burned = 0

    while True:
        adjust_choice = input("\nUpdate eaten or burned? (Type 'quit' to stop and view daily stats.) ").strip().lower()

        if adjust_choice == "eaten":
            eaten += stats.ask_int("Type the calories you ate, or a negative number to subtract from your total: ")
            # Negatives can fix earlier meals, but the day's total can't drop below 0,
            # so cap this meal at exactly what brings the day back to 0
            if stats.daily["eaten"] + eaten < 0:
                eaten = -stats.daily["eaten"]
                print("Your total can't go below 0, so it's been set to 0.")

        elif adjust_choice == "burned":
            burned += stats.ask_int("Type the calories you burned, or a negative number to subtract from your total: ")
            # Same 0 cap as eaten
            if stats.daily["burned"] + burned < 0:
                burned = -stats.daily["burned"]
                print("Your total can't go below 0, so it's been set to 0.")

        elif adjust_choice == "quit":
            # Add this meal to the day's totals, then show both
            stats.daily["eaten"] += eaten
            stats.daily["burned"] += burned
            net = stats.daily["eaten"] - stats.daily["burned"]
            print(f"\nCalories eaten this meal: {eaten}")
            print(f"Calories burned this meal: {burned}")
            print(f"Total calories eaten today: {stats.daily['eaten']}")
            print(f"Total calories burned today: {stats.daily['burned']}")
            print(f"Net calories today (eaten minus burned): {net}")
            break

        else:
            print("Invalid input. Type 'eaten', 'burned', or 'quit'.")