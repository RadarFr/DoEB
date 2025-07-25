import json
import random
from datetime import datetime

with open("music.json", "r", encoding="utf-8") as d:
    data = json.load(d)

cutoffPeriod = input("Please input the cutoff date. (auto to midnight): ")
cutoff = datetime.fromisoformat(cutoffPeriod + "T00:00:00+00:00")

filtered = [
    entry for entry in data
    if datetime.fromisoformat(entry["ts"].replace("Z", "+00:00")) >= cutoff
]

with open("filtered.json", "w") as f:
    json.dump(filtered, f, indent=2)

def cut():
    with open("filtered.json", "r", encoding="utf-8") as d:
        data = json.load(d)

    random_entry = random.choice(data)
    random_name = random_entry["master_metadata_track_name"]
    selection = input("Keep or cut: " + random_name + ", by " + random_entry["master_metadata_album_artist_name"] + " : ")

    if selection == "k":
        print("================================================")
        return False
    elif selection == "c":
        toCut = []

        filtered = [
            entry for entry in data
            if entry["master_metadata_track_name"] != toCut
        ]

        # Save
        with open("filtered.json", "w") as f:
            json.dump(filtered, f, indent=2)
        
        print(f"Cut {len(filtered)} songs")
        print("================================================")
        return True
    


while True:
    cut()
