import pandas as pd
import re

"""
This script reads relay event data, extracts top teams per event,
assigns points based on placement, and prints event and total team scores.
"""

INPUT_FILE = "relay_data.txt"

def read_relay_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def parse_relay_events(lines):
    event_data = []
    i = 0

    while i < len(lines):
        line = lines[i]
        if line.startswith("#"):
            match = re.match(r"#(\d+)\s+(.+)", line)
            if match:
                event_number = int(match.group(1))
                event_name = match.group(2)
                i += 1
                while i < len(lines) and not lines[i].startswith("#"):
                    if re.match(r"^\d+$|^--$", lines[i]):
                        place = lines[i]
                        team = lines[i + 1]
                        relay = lines[i + 2]
                        abbrev = lines[i + 3]
                        seed = lines[i + 4]
                        event_data.append([
                            event_number,
                            event_name,
                            place,
                            team,
                            relay,
                            abbrev,
                            seed
                        ])
                        i += 9  # Skip swimmer lines
                    else:
                        i += 1
            else:
                i += 1
        else:
            i += 1

    return pd.DataFrame(event_data, columns=["Event Number", "Event", "Place", "Team", "Relay", "Abbrev", "Seed"])

def assign_relay_points(place):
    if place == "1":
        return 10
    elif place == "2" or place == "--":
        return 6
    return 0

def calculate_points(df):
    df_top2 = df.groupby("Event Number").head(2).copy()
    df_top2["Points"] = df_top2["Place"].apply(assign_relay_points)
    return df_top2

def print_event_points_table(df):
    print("=== Event Points by Team ===")
    print(df[["Event Number", "Event", "Team", "Points"]].to_string(index=False))

def print_total_points(df):
    total = (
        df.groupby("Team")["Points"]
        .sum()
        .reset_index()
        .rename(columns={"Points": "Total Points"})
        .sort_values(by="Total Points", ascending=False)
    )
    print("\n=== Total Points by Team ===")
    print(total.to_string(index=False))

def main():
    lines = read_relay_file(INPUT_FILE)
    df = parse_relay_events(lines)
    df_top2 = calculate_points(df)
    print_event_points_table(df_top2)
    print_total_points(df_top2)

if __name__ == "__main__":
    main()
