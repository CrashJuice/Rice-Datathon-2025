import json
import csv

# File paths (update with actual paths)
geojson_file = "counties.geojson"  # Your GeoJSON file
lila_csv_file = "LILAavgFinal.csv"  # LILA data CSV
combined_csv_file = "combineddatafinal.csv"  # Additional data CSV
output_file = "us_counties_slim.geojson"  # Merged output file

# Step 1: Load LILA Data into a Dictionary (FIPS -> Avg_LILATracts)
columns_to_grab = [4,5,6,10,19,20,21,22,24,25,27,29]
data_dict = {}
with open(lila_csv_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        fips_code = row["FIPS"].zfill(5)  # Ensure 5-digit FIPS
        data_dict[fips_code] = {"Avg_LILATracts": float(row["Avg_LILATracts"])}  # Convert to float

# Step 2: Load Additional Data from combineddata.csv
with open(combined_csv_file, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        fips_code = row["FIPS"].zfill(5)  # Ensure 5-digit FIPS
        if fips_code not in data_dict:
            data_dict[fips_code] = {}  # Create entry if missing
        
        # Only grab the specified columns
        for idx in columns_to_grab:
            key = list(row.keys())[idx]  # Get the column name
            try:
                data_dict[fips_code][key] = float(row[key])  # Convert to float if possible
            except ValueError:
                data_dict[fips_code][key] = row[key]  # Keep as string if conversion fails

# Step 3: Load GeoJSON File
with open(geojson_file, "r", encoding="utf-8") as file:
    geojson_data = json.load(file)

# Step 4: Merge Data into GeoJSON
for feature in geojson_data["features"]:
    geoid = feature["properties"]["GEOID"]  # Get GEOID from GeoJSON
    if geoid in data_dict:
        # Merge all data into properties
        feature["properties"].update(data_dict[geoid])

        # Remove specific unwanted properties
        keys_to_remove = ["STATEFP", "COUNTYFP", "COUNTYNS", "AFFGEOID","GEOID","LSAD","ALAND","AWATER"]
        for key in keys_to_remove:
            if key in feature["properties"]:
                del feature["properties"][key]

# Step 5: Save Updated GeoJSON
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(geojson_data, file, indent=4)

print("Merging complete. Saved as:", output_file)
