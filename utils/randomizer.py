import random

def randomize_inputs():
    return {
        "elevation": random.randint(1500, 4500),
        "aspect": random.randint(0, 360),
        "slope": random.randint(0, 75),
        "horz_dist_hydro": random.randint(0, 2000),
        "vert_dist_hydro": random.randint(-200, 800),
        "horz_dist_road": random.randint(0, 8000),
        "horz_dist_fire": random.randint(0, 8000),
        "hillshade_9am": random.randint(0, 255),
        "hillshade_noon": random.randint(0, 255),
        "hillshade_3pm": random.randint(0, 255),
        "wilderness_area": random.choice(["Wilderness_Area1", "Wilderness_Area2", "Wilderness_Area3", "Wilderness_Area4"]),
        "soil_type": f"Soil_Type{random.randint(1, 40)}"
    }

def randomize_batch_row(s_no: int, columns: list):
    inp = randomize_inputs()
    
    row = [
        s_no,
        inp["elevation"],
        inp["aspect"],
        inp["slope"],
        inp["horz_dist_hydro"],
        inp["vert_dist_hydro"],
        inp["horz_dist_road"],
        inp["hillshade_9am"],
        inp["hillshade_noon"],
        inp["hillshade_3pm"],
        inp["horz_dist_fire"]
    ]
    
    wilderness = [1 if f"Wilderness_Area{i}" == inp["wilderness_area"] else 0 for i in range(1, 5)]
    row.extend(wilderness)
    soil = [1 if f"Soil_Type{i}" == inp["soil_type"] else 0 for i in range(1, 41)]
    row.extend(soil)
    
    return row