# Weight Tracker

A calorie tracker and weight predictor built with Python and Flask. Log the calories you eat and burn each day, and estimate how long it will take to reach a goal weight, whether you're losing weight or bulking.

## Features

- **Daily stats:** log calories eaten and burned, see your daily totals and net calories, and fix mistakes with negative numbers (totals never go below 0)
- **Weight predictor:** estimates your maintenance calories with the Mifflin-St Jeor formula, then shows how long reaching your goal would take at different calorie deficits or surpluses
- **Live results:** predictions update as you type, with a slider to try any deficit or surplus
- **Safety warnings:** flags very low daily intakes and unrealistically fast weight change
- **Terminal version:** the same features also run as a menu in the terminal

## How to run it

1. Clone the repository:
   ```
   git clone https://github.com/[sma574]/weight-tracker.git
   cd weight-tracker
   ```
2. Install Flask:
   ```
   pip install -r requirements.txt
   ```
3. Start the website:
   ```
   python app.py
   ```
4. Open http://127.0.0.1:5000 in your browser.

To use the terminal version instead, run `python calories.py`.

## Project structure

```
app.py            Flask routes for the website
weight.py         Predictor math: maintenance calories and time to goal
stats.py          Shared data and input helpers
daily_cals.py     Terminal version of daily calorie logging
calories.py       Terminal version's main menu
templates/        HTML pages (home, daily stats, predictor)
static/           CSS styling and JavaScript for live updates
```

## How it works

Maintenance calories are estimated with the Mifflin-St Jeor equation, adjusted for activity level. Time to goal uses the common estimate that about 3,500 calories equals 1 pound of body weight. Results are estimates, and real progress varies from person to person.

## Built with

- Python
- Flask
- HTML, CSS and JavaScript

## Future plans

-