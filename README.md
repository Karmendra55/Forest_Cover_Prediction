# Forest Cover Type Prediction

An intelligent Streamlit-based web application to predict forest cover types using geographical and environmental parameters. Powered by XGBoost, this tool enables researchers, forestry managers, and environmental analysts to make data-driven predictions about forest ecology.

## Dataset Layout

The Dataset and Models are already in place, If you want to change the files you can replace these:

``` markdown
> dataset/
>    forest_cover_prediction.csv
>    new_forest_data

> model/
>    xgb_model.pkl
```

The Dataset folder has both cleaned and the orginal that can be found in the `dataset/` folder in `.csv` format.
Make sure not to delete any files.

## Quickstart

1) Create and activate a virtual environment
```bash
python -m venv .venv
```
For Linux or Max:
```bash
source .venv/bin/activate
```
For Windows:
```bash
.venv\Scripts\activate
```

2) Now Run the file to install the dependencies
```bash
install_modules.bat
```

Run the Application
3a) Option A
```bash
run.bat
```

3b) Option B
- Open the command/bash and do the follow:
```bash
cd {"Drive:/file/.../Forest_Cover_Prediction/"}
```
and type
```bash
streamlit run main.py
```

Make sure all files are placed as shown in the dataset layout, Once started, the application will open in your default web browser.

## Overview

The **Forest Cover Type Prediction System** classifies forest patches into one of seven vegetation types based on environmental features. It supports:  
- Batch Prediction: Upload a CSV dataset to process multiple forest patches simultaneously.  
- Single Patch Prediction: Enter 54 environmental parameters for a detailed prediction.  
- Visual Insights: Interactive charts, probability distributions, and downloadable reports.  
- User Customization: Multiple themes (Light, Dark, Tree) for an enhanced experience.  
- Intro Voice Assistant: Provides a guided briefing on first use.   

## Forest Cover Types Mapping

Numeric codes in the dataset are mapped to cover type names for better readability:
```Markdown
| Number | Cover Type Name   |
------------------------------
| 1      | Spruce/Fir        |
| 2      | Lodgepole Pine    |
| 3      | Ponderosa Pine    |
| 4      | Cottonwood/Willow |
| 5      | Aspen             |
| 6      | Douglas-fir       |
| 7      | Krummholz         |
```

## Model

- Algorithm: XGBoost classifier trained on environmental and geographical features.
- Features: 54 environmental parameters for prediction.
- Inputs: The User can upload batches of inputs and just one input for predictions.
- Output: Forest cover type classification with probability scores.

  ## Features

- Single patch prediction.
- Batch prediction via CSV upload.
- Interactive visualizations of predictions.
- Theme customization and voice-guided introduction.
