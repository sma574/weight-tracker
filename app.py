"""Website for the weight tracker.

Pages:
    /           home screen (main menu)
    /daily      log calories eaten and burned
    /predictor  weight predictor; its JavaScript calls /api/predict for results
"""

from flask import Flask, jsonify, redirect, render_template, request, url_for

import stats
import weight

app = Flask(__name__)


def make_option(weight_lbs, goal_weight, maintenance, amount, losing):
    """Build one result row: daily intake, days to goal, and any warning."""
    sign = -1 if losing else 1
    daily_intake = maintenance + sign * amount
    days = weight.days_to_goal(weight_lbs, goal_weight, maintenance, daily_intake)
    lbs_per_week = amount * 7 / weight.CALORIES_PER_LB

    warning = None
    if daily_intake < weight.MIN_SAFE_INTAKE:
        warning = f"Below {weight.MIN_SAFE_INTAKE} calories a day is very low. Talk to a doctor first."
    elif losing and lbs_per_week > weight.MAX_LOSS_PER_WEEK:
        warning = f"Losing over {weight.MAX_LOSS_PER_WEEK} lbs a week is very aggressive."
    elif not losing and lbs_per_week > weight.MAX_GAIN_PER_WEEK:
        warning = f"Gaining over {weight.MAX_GAIN_PER_WEEK} lb a week is likely to add more fat than muscle."

    return {
        "amount": amount,
        "daily_intake": daily_intake,
        "days": days,
        "weeks": round(days / 7, 1),
        "lbs_per_week": round(lbs_per_week, 2),
        "warning": warning,
    }


@app.route("/")
def home():
    """Home screen: the main menu."""
    return render_template("home.html")


@app.route("/daily", methods=["GET", "POST"])
def daily():
    """Log calories eaten or burned, and show today's totals."""
    message = None
    if request.method == "POST":
        category = request.form.get("category")
        try:
            amount = int(request.form.get("amount", ""))
        except ValueError:
            message = "Please enter a whole number."
        else:
            if category in stats.daily:
                stats.daily[category] += amount
                # Same rule as the terminal version: totals can't go below 0
                if stats.daily[category] < 0:
                    stats.daily[category] = 0
                    message = "Your total can't go below 0, so it's been set to 0."
    return render_template("daily.html", daily=stats.daily, message=message)


@app.route("/daily/reset", methods=["POST"])
def reset_daily():
    """Set today's totals back to 0."""
    stats.daily["eaten"] = 0
    stats.daily["burned"] = 0
    return redirect(url_for("daily"))


@app.route("/predictor")
def predictor():
    """Weight predictor page. The results are filled in by JavaScript."""
    return render_template("predictor.html", activities=weight.ACTIVITY_DESCRIPTIONS)


@app.route("/api/predict", methods=["POST"])
def predict():
    """Take the user's numbers as JSON and send back the prediction as JSON."""
    data = request.get_json(silent=True) or {}

    # Convert and check every input; send back an error message if anything is wrong
    try:
        age = int(data["age"])
        weight_lbs = float(data["weight_lbs"])
        height_in = float(data["height_in"])
        goal_weight = float(data["goal_weight"])
        custom_amount = int(data.get("custom_amount", 500))
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Fill in every box to see your prediction."}), 400

    sex = data.get("sex")
    activity = data.get("activity_level")
    if sex not in ("male", "female") or activity not in weight.ACTIVITY_MULTIPLIERS:
        return jsonify({"error": "Choose a sex and an activity level."}), 400
    if min(age, weight_lbs, height_in, goal_weight) <= 0:
        return jsonify({"error": "All numbers must be greater than 0."}), 400

    maintenance = weight.estimate_maintenance(age, sex, weight_lbs, height_in, activity)
    result = {"maintenance": maintenance, "at_goal": goal_weight == weight_lbs}
    if result["at_goal"]:
        return jsonify(result)

    # Losing needs a deficit (below maintenance); bulking needs a surplus (above)
    losing = goal_weight < weight_lbs
    result["direction"] = "below" if losing else "above"
    result["goal_change"] = round(abs(weight_lbs - goal_weight), 1)
    result["options"] = [
        make_option(weight_lbs, goal_weight, maintenance, amount, losing)
        for amount in weight.CHANGE_OPTIONS
    ]
    result["custom"] = make_option(weight_lbs, goal_weight, maintenance, custom_amount, losing)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)