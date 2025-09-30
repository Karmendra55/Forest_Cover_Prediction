import streamlit as st
from utils.theme import section_divider

def captions():
    return [
        "🧭 Navigate the different features from the sidebar.",
        "💡 Tip: The sidebar is your control center.",
        "🎨 Customize your experience with themes!",
        "📧 Want to send Feedback, In About Section open the Feedback and Credit Section.",
        "🧮 About section has everything you can Learn about this Project.",
        "🔉 Hope the Audio does not seems to be Robotic",
        "🌱 Single Patch is has columns to fill, with Tips if you are lost.",
        "😓 No need to Worry as Single Patch, Has nothing you need to enter, just select or type.",
        "🤟 Like to look through Visualization? You can see various Graphs and Charts after Predictions",
        "📩 Want to save your Inputs and the Prediction? The PDF will be generated when the prediction is done.",
        "📄 Want to find more then a few results? Use the Batch Prediction Tool, You can also download it.",
    ]

def show():
    st.markdown(
        """
        <div class="about-card">
            <div class="about-header">🏠 Welcome to the Forest Cover Type Prediction System</div>
            <div class="about-subtext">
                Explore, predict, and analyze forest cover types using advanced Machine Learning.<br>
                Designed for <b>researchers, students, and forestry managers</b> 
                to make better ecological decisions.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    section_divider("What is This Application")
    with st.expander("📘 What is this program?"):
        st.write("""
        The **Forest Cover Type Prediction System** is a machine learning application that classifies forest areas 
        into **7 different cover types** using geographical and environmental features.  

        ✅ Useful for:  
        - Forestry research and conservation  
        - Ecological impact assessments  
        - Educational demonstrations in ML & GIS  
        - Quick exploration of environmental datasets 
        """)

    # 2️⃣ How does it predict?
    with st.expander("🤖 How does it predict?"):
        st.write("""
        - Uses an **XGBoost classifier** trained on around ~15,200 ecological data entries.  
        - Considers **54 features** (elevation, slope, soil type, wilderness area, etc.).  
        - Produces a **probability distribution** across forest types → not just a single guess.  
        - Chooses the most probable class as the prediction.  

        ⚡ Why XGBoost?  
        - High accuracy (~94%)  
        - Handles large datasets efficiently  
        - Works well with mixed numerical & categorical features 
        """)

    section_divider("How does it Work?")
    # 3️⃣ What is this tool?
    with st.expander("🛠 What is this tool?"):
        st.write("""
        This system predicts which type of forest is most likely to grow in a **30m × 30m land patch**.  

        🌍 Features considered:  
        - ⛰ Elevation  
        - 🧭 Aspect  
        - 📐 Slope  
        - 🏞 Soil Type  
        - 🌲 Wilderness Area  

        📌 Example:  
        - A location at **2,800m elevation**, steep slope, in a specific wilderness area → Most likely **Spruce/Fir** forest.  
        """)

    # 4️⃣ How It Works
    with st.expander("📖 How It Works (Batch & Single Patch Prediction)"):
        st.markdown("""
        **📄 Batch Prediction**  
        - Upload a **CSV file** with multiple rows of input data.  
        - Predictions for each row are displayed in a table.  
        - Get **bar & pie chart visualizations** of cover distribution.  
        - Download results as a **timestamped CSV**.  

        **🌱 Single Patch Prediction**  
        - Enter Compressed features manually.  
        - System predicts the cover type instantly.  
        - View detailed probability chart.  
        - Export a **professional PDF report** with inputs + results.  

        🔔 Tip: Start with *Single Patch* to understand inputs before moving to *Batch* mode.
        """)
        
    # 5️⃣ How to Use
    with st.expander("📝 How To Use"):
        st.markdown("""
        1. Navigate to **Batch Prediction** or **Single Patch Prediction** from the sidebar.  
        2. Upload a CSV file or input values manually.  
        3. Review prediction outputs + charts.  
        4. Download results for reporting.  

        ⚠️ CSV Upload Guidelines:  
        - Must include **all 54 feature columns** in the correct format.  
        - Ensure no missing values.  
        - File size: up to ~50MB recommended, But a Maximum of 200MB is allowed.  
        """)

    section_divider("Model and Feedback")
    # 6️⃣ Dataset
    with st.expander("🌍 About the Dataset"):
        st.markdown("""
        - **Source**: Provided By Unified Mentor's – Forest Cover Type Dataset.  
        - **Features**: 54 attributes describing terrain, soil, and wilderness.  
        - **Classes** (forest types):  
          1. 🌲 Spruce/Fir  
          2. 🌲 Lodgepole Pine  
          3. 🌲 Ponderosa Pine  
          4. 🌳 Cottonwood/Willow  
          5. 🍂 Aspen  
          6. 🌲 Douglas-fir  
          7. 🌿 Krummholz  
        """)

    # 7️⃣ Model
    with st.expander("📊 Model Details"):
        st.markdown("""
        - **Algorithm**: XGBoost (Extreme Gradient Boosting)  
        - **Validation Accuracy**: ~94%  
        - **Training Data**: ~15,200 labeled samples  
        - **Optimizations**:  
          - Feature scaling  
          - Hyperparameter tuning  
          - Early stopping to prevent overfitting  

        🚀 Strengths:  
        - Fast inference  
        - Handles imbalance between classes  
        - Scales to large datasets  
        """)

    # 8️⃣ Feedback
    with st.expander("📬 Feedback & Credits"):
        st.markdown("""
        - 👨‍💻 Developed by **Karmendra Bahadur Srivastava**  
        - 📊 Dataset credit: Unified Mentor Provided Dataset
        - 📧 Feedback & bug reports: [karmendra5902@gmail.com](mailto:karmendra5902@gmail.com)  
        - 🔉 Voice synthesis powered by *Mark* (Elevenlabs) → [elevenlabs.io](https://elevenlabs.io)  

        🙏 Special thanks to the open-source community for resources and accessability.  
        """)