import pandas as pd
import re

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
                            event_number, event_name, place, team, relay, abbrev, seed
                        ])
                        i += 9
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

def relay_points(df):
    df_top2 = df.groupby("Event Number").head(2).copy()
    df_top2["Points"] = df_top2["Place"].apply(assign_relay_points)
    return df_top2

def print_relay_event_points(df):
    print("=== Relay Event Points ===")
    print(df[["Event Number", "Event", "Team", "Points"]].to_string(index=False))

def print_relay_totals(df):
    total = (
        df.groupby("Team")["Points"]
        .sum()
        .reset_index()
        .rename(columns={"Points": "Total Points"})
        .sort_values(by="Total Points", ascending=False)
    )
    print("\n=== Relay Total Points ===")
    print(total.to_string(index=False))
