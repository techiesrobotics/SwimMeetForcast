import pandas as pd
'''
This program takes in individual data, convert to a formatted file, and calculate the relay points
teh result will be printed to the console
'''
# File paths
input_file = "individual_data.txt"
output_file = "swim_meet_results.csv"

# Read input
with open(input_file, "r", encoding="utf-8") as file:
    lines = file.read().strip().splitlines()

# Parse lines
all_rows = []
event = ""
i = 0
while i < len(lines):
    line = lines[i].strip()
    if line.startswith("#"):
        event = line
        i += 5  # Skip: Pl, Name, Age, Team, Seed
        continue

    if i + 4 >= len(lines):
        break

    place = lines[i].strip()
    name = lines[i + 1].strip()
    age = lines[i + 2].strip()
    team = lines[i + 3].strip()
    seed = lines[i + 4].strip()

    if place.isdigit() or place == "--":
        all_rows.append([event, place, name, age, team, seed])
        i += 5
    else:
        i += 1

# Create DataFrame and save
df = pd.DataFrame(all_rows, columns=["Event", "Place", "Name", "Age", "Team", "Seed"])
df.to_csv(output_file, index=False)
print(f"Results saved to {output_file}")

# Scoring
points_mapping = {"1": 5, "2": 3, "3": 2, "4": 1}
df["Points"] = df["Place"].astype(str).apply(lambda x: points_mapping.get(x, 0))

# Extract event info
df["Event Number"] = df["Event"].str.extract(r"#(\d+)")
df["Event Name"] = df["Event"].str.extract(r"#\d+\s+(.*)")

# Group and sum points
event_points = (
    df.groupby(["Event Number", "Event Name", "Team"])["Points"]
    .sum()
    .reset_index()
)

# Pivot for one-line event summary
pivoted = event_points.pivot_table(index=["Event Number", "Event Name"], columns="Team", values="Points", fill_value=0)
pivoted = pivoted.reset_index()

# Print one-line summaries
print("\n=== One-Line Event Summaries ===")
for _, row in pivoted.iterrows():
    parts = [f"Event #{row['Event Number']} - {row['Event Name']}"]
    for team in pivoted.columns[2:]:
        parts.append(f"{team}: {row[team]}")
    print(" | ".join(parts))

# Total summary
total_points = event_points.groupby("Team")["Points"].sum().reset_index().sort_values(by="Points", ascending=False)
print("\n=== Total Points Summary ===")
print(total_points.to_string(index=False))
