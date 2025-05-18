from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)
CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {
            "mode": "motion",
            "minutes": 1,
            "start_action": "off",
            "motion_action": "dim",
            "end_action": "off"
        }

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        mode = request.form.get("mode")
        minutes = request.form.get("minutes")
        start_action = request.form.get("start_action")
        motion_action = request.form.get("motion_action")
        end_action = request.form.get("end_action")

        try:
            minutes = int(minutes)
        except (ValueError, TypeError):
            minutes = 1

        config = {
            "mode": mode,
            "minutes": minutes,
            "start_action": start_action,
            "motion_action": motion_action,
            "end_action": end_action
        }

        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)

        return redirect(url_for("home"))

    config = load_config()
    return render_template("index.html", config=config)

if __name__ == "__main__":
    app.run(debug=True)
