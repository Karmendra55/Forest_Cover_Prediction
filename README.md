Forest Cover Type Prediction

An intelligent web application to predict **forest cover types** using geographical and environmental parameters. Built with **Streamlit** and powered by **XGBoost**, this tool enables researchers, forestry managers, and environmental analysts to make data-driven predictions about forest ecology.  

Dataset Layout

The Dataset both cleaned and the orginal can be found in the `dataset/` folder in `.csv` format.

Overview

The **Forest Cover Type Prediction System** classifies forest patches into one of seven vegetation types based on environmental features. It supports:  

Batch Prediction: Upload a CSV dataset to process multiple forest patches simultaneously.  
Single Patch Prediction: Enter 54 environmental parameters for a detailed prediction.  
Visual Insights: Interactive charts, probability distributions, and downloadable reports.  
User Customization: Multiple themes (Light, Dark, Tree) for an enhanced experience.  
Intro Voice Assistant: Provides a guided briefing on first use.   

Forest Cover Types Mapping

The original dataset used has numbers and cover types to denote vegetation types. For improved **readability and usability**, these were mapped to **forest type names**:

| Number | Cover Type Name   |
------------------------------
| 1      | Spruce/Fir        |
| 2      | Lodgepole Pine    |
| 3      | Ponderosa Pine    |
| 4      | Cottonwood/Willow |
| 5      | Aspen             |
| 6      | Douglas-fir       |
| 7      | Krummholz         |

This conversion ensures users understand predictions without referring back to raw codes.

Run the `install_modules.bat` file 
then follow the steps below

Run Locally
> Clone this repository and execute:  
bash: On a terminal to Run the program
streamlit `run main.py` 

OR

Open the `Run.bat` file in the root folder
