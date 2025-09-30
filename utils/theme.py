import streamlit as st
import base64
import os
from utils.colors import get_palette

def get_base64_img(img_path: str) -> str:
    if not os.path.exists(img_path):
        return ""
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def home_style():
    st.markdown(
        """
        <style>
            body { background-color: #f9f9f9; }
            .main { padding: 20px; }
            h1, h2, h3 {
                color: #2e7d32;
                font-family: 'Segoe UI', sans-serif;
            }
            hr { margin: 20px 0; border: 1px solid #ddd; }
            .footer {
                text-align: center;
                color: #666;
                font-size: 13px;
                margin-top: 20px;
            }
            .stButton>button {
                background: #99a39a;
                color: white;
                border-radius: 8px;
                padding: 0.6em 1.2em;
                border: none;
                font-weight: 600;
            }
            .stButton>button:hover {
                background: linear-gradient(90deg, #1b5e20, #43a047);
                transition: 0.3s;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def apply_global_styles():
    st.markdown(
        """
        <style>
        html, body, .stApp {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            -webkit-font-smoothing: antialiased;
        }
        .result-card {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #e0e0e0;
            margin-bottom: 20px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
        }
        .result-title { font-size: 20px; font-weight: 600; margin-bottom: 0.5rem; }
        .confidence { font-size: 16px; font-weight: 500; margin-top: 8px; }
        .footer {
            margin-top: 2rem;
            text-align: center;
            font-size: 0.8rem;
            opacity: 0.7;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def apply_batch_styles():
    st.markdown(
        """
        <style>
        .stFileUploader > div {
            border: 2px dashed #4CAF50;
            background-color: #F9FFF9;
            border-radius: 10px;
            padding: 15px;
            transition: all 0.3s ease;
        }
        .stFileUploader > div:hover {
            background-color: #E8F5E9;
            border-color: #2E7D32;
        }
        .custom-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #e0e0e0;
            margin-top: 15px;
            margin-bottom: 20px;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
        }
        .custom-title { font-size: 18px; font-weight: 600; margin-bottom: 8px; }
        .custom-sub { font-size: 15px; color: #555; }
        .highlight { font-weight: 600; color: #1b5e20; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def section_divider(title: str, emoji="✨"):
    if "theme" not in st.session_state:
        color = "#000000"
    else:
        color_map = {
            "default": "#000000",
            "dark": "#FF9800",
            "tree": "#63c968"
        }
        color = color_map.get(st.session_state["theme"].lower(), "#000000")
    
    st.markdown(
        f"""
        <div style="border-top:1.5px solid {color}; padding-top:1.5rem; margin-top:1.5rem; margin-bottom:1.5rem; font-weight:600;">
            {emoji} {title}
        </div>
        """,
        unsafe_allow_html=True,
    )

def themed_divider():
    if "theme" not in st.session_state:
        color = "#000000"
    else:
        color_map = {
            "default": "#000000",
            "dark": "#FF9800",
            "tree": "#63c968"
        }
        color = color_map.get(st.session_state["theme"].lower(), "#000000")
    
    st.markdown(
        f'<div style="border-top:1.5px solid {color}; margin:1rem 0;"></div>',
        unsafe_allow_html=True
    )

def apply_theme(selected_theme: str): 
    palette = get_palette(selected_theme)

    css = ""
    if selected_theme.lower() == "default":
        css = f"""
        <style>
            html, body, .stApp {{
                background-color: {palette['BACKGROUND']} !important;
                color: {palette['TEXT']} !important;
            }}
            .stSidebar, .stSidebarContent, header {{
                background-color: #e6f5e9 !important;
                border-right: 1px solid #cce3cf;
            }}
            /* Buttons */
            .stButton>button, .stDownloadButton>button {{
                background: linear-gradient(90deg, {palette['PRIMARY']}, {palette['SECONDARY']});
                color: white !important;
                border-radius: 8px !important;
                border: none !important;
                font-weight: 600;
                transition: 0.3s;
            }}
            .stButton>button:hover {{
                background: linear-gradient(90deg, #1b5e20, #43a047);
            }}
            /* Multiselect chips */
            div[data-baseweb="tag"] {{
                background-color: {palette['PRIMARY']} !important;
                color: white !important;
                border-radius: 6px !important;
            }}
            /* Tabs */
            div[data-baseweb="tab"] > button {{
                background-color: #e6f5e9 !important;
                color: {palette['TEXT']} !important;
                border-radius: 6px !important;
                font-weight: 600 !important;
                padding: 6px 16px !important;
                margin-right: 6px !important;
                border: none !important;
            }}
            div[data-baseweb="tab"] > button[aria-selected="true"] {{
                background-color: {palette['PRIMARY']} !important;
                color: white !important;
            }}
            
            .about-card {{
                background: #f9fff9;
                border: 1px solid {palette['SECONDARY']};
                border-radius: 10px;
                padding: 1.5rem;
                color: {palette['TEXT']};
                box-shadow: 0 1px 5px rgba(0,0,0,0.05);
                width: 100%;
                box-sizing: border-box;
                margin-bottom: 2rem;
            }}
            .about-header {{
                font-size: 1.6rem;
                font-weight: 700;
                color: {palette['PRIMARY']};
                margin-bottom: .5rem;
            }}
            .about-subtext {{
                font-size: 1rem;
                line-height: 1.5;
            }}
            
            .footer {{
                text-align: center;
                color: #000000;
                font-size: 13px;
                margin-top: 20px;
            }}
        </style>
        """

    elif selected_theme.lower() == "dark":
        css = f"""
        <style>
            html, body, .stApp {{
                background-color: {palette['BACKGROUND']} !important;
                color: {palette['TEXT']} !important;
                font-family: 'Roboto', sans-serif;
            }}
            .stSidebar, .stSidebarContent, header {{
                background-color: #2c2c2c !important;
                color: {palette['TEXT']} !important;
            }}
            .stButton>button, .stDownloadButton>button {{
                background-color: #3c3c3c !important;
                color: {palette['TEXT']} !important;
                border-radius: 6px !important;
                border: 1px solid #666 !important;
            }}
            .stButton>button:hover {{
                color: {palette['PRIMARY']} !important;
                border-color: {palette['PRIMARY']} !important;
            }}
            /* Multiselect chips */
            div[data-baseweb="tag"] {{
                background-color: {palette['PRIMARY']} !important;
                color: #000 !important;
            }}
            /* Base pill button */
            div[data-baseweb="tab"] > button {{
                color: #ffffff !important;                     /* unselected text */
                background-color: rgba(0,0,0,0.2) !important; /* dark semi-transparent background */
                border-radius: 20px !important;               /* pill shape */
                padding: 6px 18px !important;
                font-weight: 600 !important;
                margin-right: 6px !important;
                border: none !important;
                outline: none !important;
                box-shadow: none !important;
                transition: 0.3s;
            }}

            /* Selected pill */
            div[data-baseweb="tab"] > button[aria-selected="true"] {{
                color: #ffffff !important;         /* text */
                background-color: #2e7d32 !important; /* green highlight */
            }}

            /* Hover / Focus / Active */
            div[data-baseweb="tab"] > button:hover,
            div[data-baseweb="tab"] > button:focus,
            div[data-baseweb="tab"] > button:active {{
                background-color: rgba(46,125,50,0.8) !important; /* lighter green on hover */
                color: #ffffff !important;
                outline: none !important;
                box-shadow: none !important;
            }}

            /* Remove cyan underline / inkbar entirely */
            div[data-baseweb="tab"] > button::after {{
                display: none !important;
            }}
            
            .about-card {{
                background: #333;
                border-radius: 10px;
                padding: 1.5rem;
                color: {palette['TEXT']};
                box-shadow: 0 2px 6px rgba(0,0,0,0.4);
                width: 100%;
                box-sizing: border-box;
                margin-bottom: 2rem;
            }}
            .about-header {{
                font-size: 1.6rem;
                font-weight: 700;
                color: {palette['PRIMARY']};
                margin-bottom: .5rem;
            }}
            .about-subtext {{
                font-size: 1rem;
                line-height: 1.5;
            }}
            
            .stMetric label {{
                color: #FFFFFF !important;  /* metric label color */
                font-weight: 600;
            }}
            .stMetric div[data-testid="stMetricValue"] {{
                color: {palette['SECONDARY']};

            }}
            .stMetric svg {{
                fill: #FF9800 !important; /* arrow up/down icon color */
            }}
            
            .stSidebar, .stSidebarContent, header {{
                background-color: #2c2c2c !important;
                color: {palette['TEXT']} !important;
            }}
            .stSidebar label {{
                color: white !important;
            }}
            .stSidebar h2, .stSidebar h3 {{
                color: white !important;
            }}
            
            .css-1kyxreq p,       /* Streamlit markdown paragraphs */
            .stMarkdown p, 
            .stMarkdown small, 
            .stSlider label,       /* Slider labels */
            .stCaption,            /* st.caption text */
            .stText,               /* st.text */
            .stMultiSelect label, 
            .stNumberInput label {{
                color: #ffffff !important;  /* white text for visibility */
            }}

            /* Optional: make slider value stand out */
            .stSlider span {{
                color: #ffffff !important;
            }}
            
            .footer {{
                text-align: center;
                color: #ffffff;
                font-size: 13px;
                margin-top: 20px;
            }}

        </style>
        """

    elif selected_theme.lower() == "tree":
        img_base64 = get_base64_img("img/treebg-min.jpg")
        css = f"""
        <style>
            html, body, .stApp {{
                color: {palette['TEXT']} !important;
                font-family: "Georgia", serif !important;
            }}
            .css-1kyxreq p, .stMarkdown p, .stMarkdown small {{
                color: #ffffff !important;
            }}
            .stSidebar, .stSidebarContent, header {{
                background: rgba(38,41,38,0.9) !important;
                color: white !important;
            }}
            .stExpander {{
                background-color: linear-gradient(90deg, #2e7d32, #66bb6a); !important;
                border: 1px solid {palette['PRIMARY']} !important;
                border-radius: 12px !important;
                color: #ffffff;
            }}
            .stButton>button {{
                background-color: #b6b8b6 !important;
                color: #030303 !important;
                border-radius: 8px !important;
                border: 1px solid {palette['PRIMARY']} !important;
            }}
            .stButton>button:hover {{
                background-color: {palette['PRIMARY']} !important;
                color: white !important;
            }}
            div[data-baseweb="tag"] {{
                background-color: {palette['PRIMARY']} !important;
                color: white !important;
            }}
            div[data-baseweb="tab"] > button {{
                background-color: #c8e6c9 !important;
                color: {palette['TEXT']} !important;
            }}
            div[data-baseweb="tab"] > button[aria-selected="true"] {{
                background-color: {palette['PRIMARY']} !important;
                color: white !important;
            }}
            .stApp::before {{
                content: "";
                position: fixed; top: 0; left: 0;
                width: 100%; height: 100%;
                background: url("data:image/jpg;base64,{img_base64}") no-repeat center center fixed;
                background-size: cover;
                opacity: 0.8;
            }}
            
            .about-card {{
                background: #1c361d;
                border-radius: 12px;
                padding: 1.5rem;
                backdrop-filter: blur(4px);
                box-shadow: 0 3px 8px rgba(0,0,0,0.2);
                color: #1b5e20;
                width: 100%;
                box-sizing: border-box;
                margin-bottom: 2rem;
            }}
            .about-header {{
                font-size: 1.6rem;
                font-weight: 700;
                color: {palette["SECONDARY"]};
                margin-bottom: .5rem;
                text-shadow: 0 1px 2px rgba(255,255,255,0.8);
            }}
            .about-subtext {{
                font-size: 1.05rem;
                color: {palette['TEXT']};
                line-height: 1.6;
            }}
            
            .stMetric label {{
                color: {palette['TEXT']} !important;  /* metric label color */
                font-weight: 600;
            }}
            .stMetric div[data-testid="stMetricValue"] {{
                color: {palette['SECONDARY']};

            }}
            .stMetric svg {{
                fill: #FF9800 !important; /* arrow up/down icon color */
            }}
            
            .stSidebar, .stSidebarContent, header {{
                background-color: #2c2c2c !important;
                color: {palette['TEXT']} !important;
            }}
            .stSidebar label {{
                color: white !important;
            }}
            .stSidebar h2, .stSidebar h3 {{
                color: white !important;
            }}
            
            .stAlert {{
                color: #ffffff !important;               /* text color */
                background-color: rgba(0, 0, 0, 0.5) !important;  /* semi-transparent overlay */
                border-left: 6px solid #43a047 !important;        /* green border for success */
            }}

            /* Success alerts */
            .stAlert.stAlert-success {{
                color: #1b5e20 !important;           /* text */
                background-color: rgba(198, 239, 206, 0.8) !important; /* light green background */
                border-left: 6px solid #43a047 !important;
            }}

            /* Info alerts */
            .stAlert.stAlert-info {{
                color: #0d47a1 !important;
                background-color: rgba(197, 202, 233, 0.85) !important;
                border-left: 6px solid #1976d2 !important;
            }}

            /* Warning alerts */
            .stAlert.stAlert-warning {{
                color: #7f6000 !important;
                background-color: rgba(255, 243, 205, 0.85) !important;
                border-left: 6px solid #ffb300 !important;
            }}
            
            div[data-baseweb="tab"] > button {{
                color: #ffffff !important;            /* text visible on green bg */
                background-color: rgba(0,0,0,0.2) !important; /* slightly transparent */
            }}
            div[data-baseweb="tab"] > button[aria-selected="true"] {{
                color: #ffffff !important;           /* selected tab text */
                background-color: #2e7d32 !important; /* dark green highlight */
            }}
            
            .stDownloadButton>button {{
                color: #000000 !important;        /* black text for tree theme */
                background-color: #b6b8b6 !important; /* keep the current button bg */
                border-radius: 8px !important;
                border: 1px solid {palette['PRIMARY']} !important;
                font-weight: 600;
            }}
            .stDownloadButton>button:hover {{
                color: white !important;
                background-color: {palette['PRIMARY']} !important;
            }}
                        
            .css-1kyxreq p,       /* Streamlit markdown paragraphs */
            .stMarkdown p, 
            .stMarkdown small, 
            .stSlider label,       /* Slider labels */
            .stCaption,            /* st.caption text */
            .stText,               /* st.text */
            .stMultiSelect label, 
            .stNumberInput label {{
                color: #ffffff !important;  /* white text for visibility */
            }}

            /* Optional: make slider value stand out */
            .stSlider span {{
                color: #ffffff !important;
            }}
            
            .footer {{
                text-align: center;
                color: #ffffff;
                font-size: 13px;
                margin-top: 20px;
            }}
                        
        </style>
        """ if img_base64 else """
        <style>
            .stApp::before {
                content: "";
                position: fixed; top: 0; left: 0;
                width: 100%; height: 100%;
                background: #e8f5e9;
            }
        </style>
        """

    if css:
        st.markdown(css, unsafe_allow_html=True)
