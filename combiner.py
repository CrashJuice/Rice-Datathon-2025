import json
import csv

# File paths (update with actual paths)
geojson_file = "counties.geojson"  # Your GeoJSON file
csv_file = "LILAavg.csv"  # Your CSV file
output_file = "us_counties_LILA.geojson"  # Merged output file

# Step 1: Load CSV Data into a Dictionary (FIPS -> Avg_LILATracts)
data_dict = {}
with open(csv_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        fips_code = row["FIPS"].zfill(5)  
        data_dict[fips_code] = float(row["Avg_LILATracts"])  # Convert to float

# Step 2: Load GeoJSON File
with open(geojson_file, "r", encoding="utf-8") as file:
    geojson_data = json.load(file)

# Step 3: Merge Data into GeoJSON
for feature in geojson_data["features"]:
    geoid = feature["properties"]["GEOID"]  # Get GEOID from GeoJSON
    feature["properties"]["Avg_LILATracts"] = data_dict.get(geoid, None)  # Assign data or None if missing

# Step 4: Save Updated GeoJSON
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(geojson_data, file, indent=4)

print("✅ Merging complete! Saved as:", output_file)
