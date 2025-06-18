import pandas as pd

"""
This program reads individual event data, processes it, calculates points,
and prints event and team summaries.
"""

INPUT_FILE = "individual_data.txt"
OUTPUT_FILE = "swim_meet_results.csv"
POINTS_MAPPING = {"1": 5, "2": 3, "3": 2, "4": 1}

def parse_input_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        lines = file.read().strip().splitlines()

    all_rows = []
    i = 0
    event = ""
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#"):
            event = line
            i += 5  # Skip headers
            continue

        if i + 4 >= len(lines):
            break

        place, name, age, team, seed = [lines[i + j].strip() for j in range(5)]
        if place.isdigit() or place == "--":
            all_rows.append([event, place, name, age, team, seed])
            i += 5
        else:
            i += 1

    return pd.DataFrame(all_rows, columns=["Event", "Place", "Name", "Age", "Team", "Seed"])

def calculate_points(df):
    df["Points"] = df["Place"].astype(str).apply(lambda x: POINTS_MAPPING.get(x, 0))
    df["Event Number"] = df["Event"].str.extract(r"#(\d+)")
    df["Event Name"] = df["Event"].str.extract(r"#\d+\s+(.*)")
    return df

def summarize_events(df):
    event_points = (
        df.groupby(["Event Number", "Event Name", "Team"])["Points"]
        .sum()
        .reset_index()
    )
    return event_points

def print_event_summaries(event_points):
    pivoted = event_points.pivot_table(
        index=["Event Number", "Event Name"],
        columns="Team",
        values="Points",
        fill_value=0
    ).reset_index()

    print("\n=== One-Line Event Summaries ===")
    for _, row in pivoted.iterrows():
        parts = [f"Event #{row['Event Number']} - {row['Event Name']}"]
        for team in pivoted.columns[2:]:
            parts.append(f"{team}: {row[team]}")
        print(" | ".join(parts))

def print_total_summary(event_points):
    total_points = (
        event_points.groupby("Team")["Points"]
        .sum()
        .reset_index()
        .sort_values(by="Points", ascending=False)
    )
    print("\n=== Total Points Summary ===")
    print(total_points.to_string(index=False))

def main():
    df = parse_input_file(INPUT_FILE)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Results saved to {OUTPUT_FILE}")

    df = calculate_points(df)
    event_points = summarize_events(df)
    print_event_summaries(event_points)
    print_total_summary(event_points)

if __name__ == "__main__":
    main()
