import pandas as pd

def parse_individual_file(text):
    lines = text.strip().splitlines()
    all_rows = []
    i = 0
    event = ""
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#"):
            event = line
            i += 5
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

def individual_points(df):
    points_map = {"1": 5, "2": 3, "3": 2, "4": 1}
    df["Points"] = df["Place"].astype(str).apply(lambda x: points_map.get(x, 0))
    df["Event Number"] = df["Event"].str.extract(r"#(\d+)")
    df["Event Name"] = df["Event"].str.extract(r"#\d+\s+(.*)")
    return df

def summarize_individual(df):
    return df.groupby(["Event Number", "Event Name", "Team"])["Points"].sum().reset_index()

def print_individual_summaries(event_points):
    pivoted = event_points.pivot_table(
        index=["Event Number", "Event Name"],
        columns="Team",
        values="Points",
        fill_value=0
    ).reset_index()
    print("=== Individual Event Summaries ===")
    for _, row in pivoted.iterrows():
        parts = [f"Event #{row['Event Number']} - {row['Event Name']}"]
        for team in pivoted.columns[2:]:
            parts.append(f"{team}: {row[team]}")
        print(" | ".join(parts))

def print_individual_totals(event_points):
    total_points = (
        event_points.groupby("Team")["Points"]
        .sum()
        .reset_index()
        .sort_values(by="Points", ascending=False)
    )
    print("\n=== Individual Total Points ===")
    print(total_points.to_string(index=False))
