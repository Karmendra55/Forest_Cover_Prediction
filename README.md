<<<<<<< HEAD
# Forest Cover Type Prediction

An intelligent web application to predict **forest cover types** using geographical and environmental parameters. Built with **Streamlit** and powered by **XGBoost**, this tool enables researchers, forestry managers, and environmental analysts to make data-driven predictions about forest ecology.  

---

## Overview

The **Forest Cover Type Prediction System** classifies forest patches into one of **seven vegetation types** based on environmental features. It supports:  

**Batch Prediction**: Upload a CSV dataset to process multiple forest patches simultaneously.  
**Single Patch Prediction**: Enter 54 environmental parameters for a detailed prediction.  
**Visual Insights**: Interactive charts, probability distributions, and downloadable reports.  
**User Customization**: Multiple themes (Light, Dark, Tree) for an enhanced experience.  
**Intro Voice Assistant**: Provides a guided briefing on first use.  

---

## Developed By
- **Karmendra Bahadur Srivastava**
- **Submitted To:** Unified Mentor  

---

## Technical Details

**Frontend**: [Streamlit](https://streamlit.io/) (custom themes and interactivity)  
**Backend Model**: [XGBoost Classifier](https://xgboost.readthedocs.io/)  
**Dataset**: [UCI Forest Cover Type Dataset](https://archive.ics.uci.edu/ml/datasets/covertype)  
**Accuracy**: ~94% on validation data  
**Features Used**: Elevation, Aspect, Slope, Soil Type, Wilderness Area, Distance to Hydrology/Roads/Fire Points, Hillshade values.  

## Forest Cover Types Mapping

The original dataset used **numbers (1–7)** to denote vegetation types. For improved **readability and usability**, these were mapped to **forest type names**:

| Number | Cover Type Name          |
--------------------------------------
| 1             | Spruce/Fir                       |
| 2             | Lodgepole Pine              |
| 3             | Ponderosa Pine              |
| 4             | Cottonwood/Willow      |
| 5             | Aspen                              |
| 6             | Douglas-fir                     |
| 7             | Krummholz                     |

This conversion ensures users understand predictions without referring back to raw codes.

---

 Run Locally
Clone this repository and execute:  

OR

bash: On a terminal to Run the program
streamlit run main.py 
or
Open the Run.bat file

=======
# Forest_Cover_Prediction
The Forest Cover Type Prediction System is an AI-powered tool designed to classify forest patches into vegetation types based on geographical and environmental parameters. Built with Streamlit and XGBoost, it offers an intuitive interface for researchers, forestry managers, and environmental analysts.
>>>>>>> 62ccee4c8623f54192908242488fcbb5cc0634c1
