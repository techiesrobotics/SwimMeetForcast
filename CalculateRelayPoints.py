import pandas as pd
import re

'''
This program takes in relay data, convert to a formatted file, and calculate the relay points
teh result will be printed to the console
'''
# Step 1: Read from input file
input_path = "relay_dta.txt"  # Update to your file path
with open(input_path, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

# Step 2: Extract event data
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

# Step 3: Create DataFrame
df = pd.DataFrame(event_data, columns=["Event Number", "Event", "Place", "Team", "Relay", "Abbrev", "Seed"])

# Step 4: Keep only top 2 teams per event
df_top2 = df.groupby("Event Number").head(2).copy()

# Step 5: Assign points (treat '--' as 2nd place if it's the second team)
def assign_points(row):
    if row["Place"] == "1":
        return 10
    elif row["Place"] == "2" or row["Place"] == "--":
        return 6
    else:
        return 0

df_top2["Points"] = df_top2.apply(assign_points, axis=1)

# Step 6: Print event points table
event_points_table = df_top2[["Event Number", "Event", "Team", "Points"]]
print("=== Event Points by Team ===")
print(event_points_table.to_string(index=False))

# Step 7: Print total points
total_points = df_top2.groupby("Team")["Points"].sum().reset_index().rename(columns={"Points": "Total Points"})
total_points = total_points.sort_values(by="Total Points", ascending=False)
print("\n=== Total Points by Team ===")
print(total_points.to_string(index=False))
