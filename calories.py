"""Main menu for the weight tracker. Run this file to start the program."""

import daily_cals
import weight
import stats

# Ctrl + C anywhere in the program jumps to the except below instead of crashing
try:
    while True:
        # Main menu (text stays against the left edge so it prints without extra spaces)
        print("""\nWhat would you like to do?
1. View/update daily stats
2. Weight predictor
3. Quit""")
        what_u_want = stats.ask_int("Enter your number choice (1-3): ")

        # Keep asking until the choice is between 1 and 3
        while what_u_want > 3 or what_u_want < 1:
            what_u_want = stats.ask_int("Invalid input. Enter a number (1-3): ")

        # Run the chosen feature, then the loop shows the menu again
        if what_u_want == 1:
            daily_cals.daily_total()
        elif what_u_want == 2:
            weight.weight_predictor()
        elif what_u_want == 3:
            print("You have officially quit the program.")
            break
except KeyboardInterrupt:
    print("\nYou have officially quit the program.")