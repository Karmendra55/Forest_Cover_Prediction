import pandas as pd
from utils.randomizer import randomize_batch_row

def get_csv_template(n_rows: int = 3, use_random: bool = True):
    columns = [
        "S_No","Elevation", "Aspect", "Slope", "Horizontal_Distance_To_Hydrology",
        "Vertical_Distance_To_Hydrology", "Horizontal_Distance_To_Roadways",
        "Hillshade_9am", "Hillshade_Noon", "Hillshade_3pm",
        "Horizontal_Distance_To_Fire_Points",
        *[f"Wilderness_Area{i}" for i in range(1, 5)],
        *[f"Soil_Type{i}" for i in range(1, 41)]
    ]
    
    data = []
    if n_rows > 0:
        if use_random:
            for i in range(1, n_rows + 1):
                data.append(randomize_batch_row(i, columns))
        else:
            examples = [
                [1, 2596, 51, 3, 258, 0, 510, 221, 232, 148, 6279, *[1,0,0,0], *[0]*39+[1]],
                [2, 2804, 139, 9, 268, 65, 3180, 234, 238, 135, 6121, *[0,1,0,0], *[0]*10+[1]+[0]*29],
                [3, 2590, 56, 2, 212, -6, 390, 220, 235, 151, 6225, *[0,0,1,0], *[0]*20+[1]+[0]*19],
            ]
            for i in range(n_rows):
                data.append(examples[i % len(examples)]) 
    
    df = pd.DataFrame(data, columns=columns)
    return df