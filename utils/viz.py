import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

from utils.logger import log_error, log_info
from utils.colors import get_palette
from utils.exceptions import VisualizationError

pio.kaleido.scope.default_format = "png"
pio.kaleido.scope.default_width = 800
pio.kaleido.scope.default_height = 600

# --- UTILITY ---
def save_plotly(fig, save_path):
    try:
        fig.write_image(save_path)
        log_info("viz", f"Plotly figure saved at {save_path}")
    except Exception as e:
        log_error("viz", e)
        raise VisualizationError(f"Could not save Plotly figure: {e}") from e


def save_matplotlib(fig, save_path):
    try:
        fig.tight_layout()
        fig.savefig(save_path, bbox_inches="tight")
        log_info("viz", f"Matplotlib figure saved at {save_path}")
    except Exception as e:
        log_error("viz", e)
        raise VisualizationError(f"Could not save Matplotlib figure: {e}") from e
    
# -------------------------------
# --- Single Patch Prediction ---
# -------------------------------
def plot_probability_radar_chart(probabilities, cover_type_map, save_path=None, theme="dark"):
    try:
        labels = list(cover_type_map.values())
        values = list(probabilities) + [probabilities[0]]
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]

        palette = get_palette(theme)

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        fig.patch.set_facecolor(palette["BACKGROUND"])
        ax.set_facecolor("#121212")

        ax.plot(angles, values, color=palette["PRIMARY"], linewidth=2, marker="o")
        ax.fill(angles, values, color=palette["PRIMARY"], alpha=0.3)

        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=10, fontweight="bold", color=palette["TEXT"])

        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels([f"{int(y*100)}%" for y in [0.2, 0.4, 0.6, 0.8, 1.0]], color=palette["TEXT"])
        ax.grid(color="#555555", linestyle="--", linewidth=0.7)

        for label, angle in zip(ax.get_xticklabels(), angles):
            label.set_horizontalalignment("center")
            label.set_rotation(angle * 180 / np.pi - 90)
            label.set_rotation_mode("anchor")

        ax.set_title("Prediction Probabilities", fontsize=16, fontweight="bold", color=palette["TEXT"], pad=20)
        ax.spines["polar"].set_visible(False)

        if save_path:
            save_matplotlib(fig, save_path)

        st.pyplot(fig)
        log_info("viz", "Radar chart rendered")
        return fig

    except Exception as e:
        log_error("viz", e)
        raise VisualizationError("Failed to render radar chart") from e

def plot_patch_grid(probabilities, cover_type_map, grid_size=(30, 30), save_path=None, theme="dark"):
    try:
        palette = get_palette(theme)

        fig, ax = plt.subplots(figsize=(7, 7))
        fig.patch.set_facecolor(palette["BACKGROUND"])
        ax.set_facecolor("#121212")

        cmap = plt.cm.get_cmap("Set3", len(probabilities))
        num_cells = grid_size[0] * grid_size[1]
        class_counts = (probabilities * num_cells).astype(int)

        flat_data = []
        for class_idx, count in enumerate(class_counts):
            flat_data += [class_idx] * count
        while len(flat_data) < num_cells:
            flat_data.append(np.argmax(probabilities))

        np.random.shuffle(flat_data)
        data = np.array(flat_data).reshape(grid_size)

        ax.imshow(data, cmap=cmap, aspect="equal")
        ax.set_title("30x30 Forest Cover Patch", fontsize=16, fontweight="bold", color=palette["TEXT"], pad=15)

        ax.set_xticks(np.arange(-0.5, grid_size[0], 1), minor=True)
        ax.set_yticks(np.arange(-0.5, grid_size[1], 1), minor=True)
        ax.grid(which="minor", color="#555555", linestyle="-", linewidth=0.5, alpha=0.5)

        ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)

        handles = [plt.Rectangle((0, 0), 1, 1, color=cmap(i)) for i in range(len(probabilities))]
        labels = [f"{cover_type_map[i+1]} ({probabilities[i]*100:.1f}%)" for i in range(len(probabilities))]
        ax.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, -0.15),
                  fontsize=9, ncol=2, frameon=True, facecolor="#121212", edgecolor="#888", labelcolor=palette["TEXT"])

        if save_path:
            save_matplotlib(fig, save_path)

        st.pyplot(fig)
        log_info("viz", "Patch grid rendered")
        return fig

    except Exception as e:
        log_error("viz", e)
        raise VisualizationError("Failed to render patch grid") from e

def plot_prediction_probabilities(probabilities, cover_type_map, save_path=None, preview=True):
    try:
        cover_types = list(cover_type_map.values())

        fig_plotly = go.Figure(
            data=[
                go.Bar(
                    x=cover_types,
                    y=probabilities,
                    marker_color="forestgreen",
                    marker_line_color="darkgreen",
                    marker_line_width=1.5,
                    hovertemplate='<b>%{x}</b><br>Probability: %{y:.2f}<extra></extra>',
                    customdata=cover_types,
                    name="Probability",
                    width=0.6,
                )
            ]
        )

        fig_plotly.update_traces(
            marker=dict(
                color="forestgreen",
                line=dict(color="darkgreen", width=1.5),
            ),
            hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial"),
            selected=dict(marker=dict(color="orange")),
            unselected=dict(marker=dict(opacity=0.6)),
        )

        fig_plotly.update_layout(
            title="Prediction Probabilities",
            xaxis_title="Cover Type",
            yaxis_title="Probability",
            hovermode="x unified",
            transition=dict(duration=500, easing="cubic-in-out"),
        )

        if preview:
            st.plotly_chart(fig_plotly, use_container_width=True, key="prediction_probabilities")

        if save_path:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(cover_types, probabilities, color="forestgreen", edgecolor="darkgreen")
            ax.set_title("Prediction Probabilities")
            ax.set_xlabel("Cover Type")
            ax.set_ylabel("Probability")
            save_matplotlib(fig, save_path)
            plt.close(fig)

        return fig_plotly
    except Exception as e:
        log_error("viz.plot_prediction_probabilities", e)
        return None

# ------------------------------
# --- Batch Patch Prediction ---
# ------------------------------
def plot_batch_bar_chart(predictions, cover_type_map, save_path=None, preview=True):
    try:
        counts = pd.Series(predictions).value_counts().sort_index()
        df = pd.DataFrame({
            "Cover Type": [cover_type_map.get(i, "Unknown") for i in counts.index],
            "Count": counts.values
        })

        fig_plotly = px.bar(
            df,
            x="Cover Type",
            y="Count",
            color="Count",
            color_continuous_scale="Greens",
            text="Count",
            title="📊 Cover Type Distribution (Interactive)",
        )

        fig_plotly.update_traces(
            textposition="outside",
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>',
            marker=dict(line=dict(color="white", width=1)),
            textfont=dict(color='white', size=12),
        )

        fig_plotly.update_layout(
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(color='white', size=12),
            title=dict(font=dict(color='white', size=18)),
            hovermode="x unified",
            transition=dict(duration=300, easing='cubic-in-out'),
            clickmode='event+select',
        )

        if save_path:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(df["Cover Type"], df["Count"], color="forestgreen", edgecolor="darkgreen")
            ax.set_title("Cover Type Distribution")
            ax.set_xlabel("Cover Type")
            ax.set_ylabel("Count")
            save_matplotlib(fig, save_path)
            plt.close(fig)

        return fig_plotly
    except Exception as e:
        log_error("viz.plot_batch_bar_chart", e)
        return None

def plot_batch_pie_chart(predictions, cover_type_map, save_path=None, preview=True):
    try:
        counts = pd.Series(predictions).value_counts().sort_index()
        df = pd.DataFrame({
            "Cover Type": [cover_type_map.get(i, "Unknown") for i in counts.index],
            "Count": counts.values
        })

        fig_plotly = px.pie(
            df,
            names="Cover Type",
            values="Count",
            title="🥧 Cover Type Percentage (Interactive)",
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.3,
        )

        fig_plotly.update_traces(
            pull=[0.05] * len(df),
            hovertemplate='<b>%{label}</b><br>Percentage: %{percent}<extra></extra>',
            textinfo='percent+label',
            textfont=dict(color='blue', size=14),
        )

        fig_plotly.update_layout(
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(color='blue'),
            title=dict(font=dict(color='white', size=18)),
            legend=dict(font=dict(color='white', size=12)),
        )


        if save_path:
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(df["Count"], labels=df["Cover Type"], autopct="%1.1f%%", startangle=90)
            ax.set_title("Cover Type Percentage")
            save_matplotlib(fig, save_path)
            plt.close(fig)

        return fig_plotly
    except Exception as e:
        log_error("viz.plot_batch_pie_chart", e)
        return None

def plot_feature_boxplots(data, predictions, cover_type_map, features=None, save_path=None, preview=True):
    try:
        df = data.copy()
        df["Predicted Cover Type"] = [cover_type_map.get(i, "Unknown") for i in predictions]

        if features is None:
            features = ["Elevation"]

        figs = []
        for feature in features:
            if feature not in df.columns:
                if preview:
                    st.warning(f"⚠️ Feature '{feature}' not found in dataset.")
                continue

            fig_plotly = px.box(
                df,
                x="Predicted Cover Type",
                y=feature,
                color="Predicted Cover Type",
                title=f"📊 {feature} by Predicted Cover Type",
                template="plotly_dark",
                points="all",
            )

            fig_plotly.update_traces(
                hovertemplate=f"<b>%{{x}}</b><br>{feature}: %{{y}}<extra></extra>",
                jitter=0.5,
                whiskerwidth=0.2,
            )
            fig_plotly.update_layout(
                xaxis_title="Predicted Cover Type",
                yaxis_title=feature,
                transition=dict(duration=300, easing="cubic-in-out"),
                showlegend=False,
            )

            if preview:
                st.plotly_chart(fig_plotly, use_container_width=True)

            figs.append(fig_plotly)

            if save_path:
                fig, ax = plt.subplots(figsize=(8, 5))
                sns.boxplot(x="Predicted Cover Type", y=feature, data=df, palette="Set3", ax=ax)
                ax.set_title(f"{feature} by Predicted Cover Type")
                save_matplotlib(fig, save_path)
                plt.close(fig)

        return figs
    except Exception as e:
        log_error("viz.plot_feature_boxplots", e)
        return []