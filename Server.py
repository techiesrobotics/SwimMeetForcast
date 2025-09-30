from flask import Flask, render_template, request
import io, sys

# Import separate modules
import individual
import relay

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/individual", methods=["GET", "POST"])
def individual_page():
    result_text = None
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if uploaded_file and uploaded_file.filename:
            text = uploaded_file.read().decode("utf-8", errors="ignore")
            df = individual.parse_individual_file(text)
            if not df.empty:
                df = individual.individual_points(df)
                event_points = individual.summarize_individual(df)
                buffer = io.StringIO()
                sys_stdout = sys.stdout
                sys.stdout = buffer
                individual.print_individual_summaries(event_points)
                individual.print_individual_totals(event_points)
                sys.stdout = sys_stdout
                result_text = buffer.getvalue()
            else:
                result_text = "⚠️ No valid individual rows found."
    return render_template("individual.html", result=result_text)

@app.route("/relay", methods=["GET", "POST"])
def relay_page():
    result_text = None
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if uploaded_file and uploaded_file.filename:
            text = uploaded_file.read().decode("utf-8", errors="ignore")
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            df = relay.parse_relay_events(lines)
            if not df.empty:
                df_top2 = relay.relay_points(df)
                buffer = io.StringIO()
                sys_stdout = sys.stdout
                sys.stdout = buffer
                relay.print_relay_event_points(df_top2)
                relay.print_relay_totals(df_top2)
                sys.stdout = sys_stdout
                result_text = buffer.getvalue()
            else:
                result_text = "⚠️ No valid relay rows found."
    return render_template("relay.html", result=result_text)

if __name__ == "__main__":
    app.run(debug=True)
