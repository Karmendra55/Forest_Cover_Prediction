from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import streamlit as st

from utils.logger import log_error, log_info
from utils.exceptions import AppError
from utils.pdf import generate_single_patch_pdf
from utils.colors import get_palette
from utils.theme import themed_divider
# -----------------------
# Constants & Paths
# -----------------------
HISTORY_FILE: Path = Path("dataset/history.json")
HISTORY_BACKUP_DIR: Path = Path("dataset/history_backup")
SAVE_ROOT: Path = Path("Saved_Predictions")

MAX_DISPLAY_RECORDS = 200

COVER_TYPE_MAP = {
    1: "Spruce/Fir",
    2: "Lodgepole Pine",
    3: "Ponderosa Pine",
    4: "Cottonwood/Willow",
    5: "Aspen",
    6: "Douglas-fir",
    7: "Krummholz",
}

# -----------------------
# Helpers / JSON encoder
# -----------------------
class NpEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return super().default(obj)


def _sanitize_for_json(obj: Any) -> Any:
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.ndarray, list)):
        return [_sanitize_for_json(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _sanitize_for_json(v) for k, v in obj.items()}
    return obj


# -----------------------
# I/O & caching
# -----------------------
@st.cache_data(ttl=300)
def _read_history_file() -> Dict[str, List[Dict[str, Any]]]:
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, "r", encoding="utf-8") as fh:
                data = json.load(fh)
                if not isinstance(data, dict):
                    raise ValueError("History file format invalid")
                data.setdefault("single", [])
                data.setdefault("batch", [])
                for k in ("single", "batch"):
                    if len(data[k]) > 5000:
                        data[k] = data[k][-5000:]
                return data
        else:
            return {"single": [], "batch": []}
    except Exception as exc:
        try:
            HISTORY_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = HISTORY_BACKUP_DIR / f"history_corrupt_{ts}.json"
            HISTORY_FILE.rename(backup_path)
            log_error("history._read_history_file", f"Corrupted history backed up to {backup_path}: {exc}")
        except Exception as backup_exc:
            log_error("history._read_history_file", f"Failed to backup corrupted history: {backup_exc}")
        return {"single": [], "batch": []}


def _write_history_file(data: Dict[str, List[Dict[str, Any]]]) -> None:
    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = HISTORY_FILE.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, default=_sanitize_for_json, ensure_ascii=False)
        tmp.replace(HISTORY_FILE)
        log_info("history._write_history_file", f"Wrote history to {HISTORY_FILE}")
    except Exception as exc:
        log_error("history._write_history_file", exc)
        raise


def _ensure_history_loaded() -> None:
    if "history" not in st.session_state:
        st.session_state.history = _read_history_file()

def load_history() -> Dict[str, List[Dict[str, Any]]]:
    try:
        _ensure_history_loaded()
        return st.session_state.history
    except Exception as exc:
        log_error("history.load_history", exc)
        return {"single": [], "batch": []}


def save_to_history(tab: str, record: Dict[str, Any]) -> None:
    try:
        if tab not in ("single", "batch"):
            raise ValueError("tab must be 'single' or 'batch'")

        _ensure_history_loaded()

        # --- Normalize record and add timestamp server-side ---
        record = {**record}
        record.setdefault("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        record = _sanitize_for_json(record)

        st.session_state.history.setdefault(tab, []).append(record)

        _write_history_file(st.session_state.history)

        # --- update cached function by invalidating it ---
        try:
            if "_read_history_file" in st.cache_data.__wrapped__.__name__:
                pass
        except Exception:
            # not critical; just log
            log_info("history.save_to_history", "Unable to manually invalidate cache; relying on TTL.")
        log_info("history.save_to_history", f"Saved record to history tab={tab}")
    except Exception as exc:
        log_error("history.save_to_history", exc)
        st.error("⚠️ Failed to save history. Check logs for details.")


# -----------------------
# History Viewer
# -----------------------
def _summary_metrics(records_single: List[Dict[str, Any]], records_batch: List[Dict[str, Any]]) -> None:
    try:
        total_single = len(records_single)
        total_batch = len(records_batch)
        avg_conf = 0.0
        confidences = [r.get("confidence", 0) for r in records_single if isinstance(r.get("confidence", None), (int, float))]
        if confidences:
            avg_conf = sum(confidences) / len(confidences)

        palette = get_palette(st.session_state.get("theme", "default"))
        c1, c2, c3 = st.columns(3)
        c1.metric("Single Predictions", f"{total_single:,}")
        c2.metric("Batch Predictions", f"{total_batch:,}")
        c3.metric("Avg. Confidence (Single)", f"{avg_conf:.2f}%")
    except Exception as exc:
        log_error("history._summary_metrics", exc)


def _export_records_as_csv(records: List[Dict[str, Any]], filename_prefix: str = "history") -> bytes:
    try:
        df = pd.DataFrame(records)
        return df.to_csv(index=False).encode("utf-8")
    except Exception as exc:
        log_error("history._export_records_as_csv", exc)
        raise


def show() -> None:
    _ensure_history_loaded()

    st.subheader("📜 Prediction History")
    st.caption("Review, filter and export previously saved Single and Batch predictions.")
    themed_divider()

    single_records_all = st.session_state.history.get("single", [])[-MAX_DISPLAY_RECORDS:]
    batch_records_all = st.session_state.history.get("batch", [])[-MAX_DISPLAY_RECORDS:]

    # --- Top metrics ---
    _summary_metrics(single_records_all, batch_records_all)

    # --- Filters ---
    col_f1, _, col_f2, col_f3 = st.columns([3, 0.5, 2, 2])
    with col_f1:
        all_labels = []
        for rec in single_records_all + batch_records_all:
            all_labels.append(rec.get("timestamp", ""))
            all_labels.append(str(rec.get("file", "")))
            all_labels.append(str(rec.get("prediction_name", "")))
        all_labels = sorted({lbl for lbl in all_labels if lbl})

        search_text = st.selectbox(
            "🔎 Search",
            options=[""] + all_labels, 
            index=0,
            help="Start typing to search by timestamp, file, or prediction name.",
        )
    with col_f2:
        date_from = st.date_input("From", value=None)
    with col_f3:
        date_to = st.date_input("To", value=None)

    themed_divider()
    # --- Tabs: Single / Batch ---
    TAB_LABELS = ["🌿 Single Patch", "📂 Batch Predictions"]

    if "history_active_tab" not in st.session_state:
        st.session_state.history_active_tab = TAB_LABELS[0]

    active_tab = st.pills(
        "History View",
        options=TAB_LABELS,
        default=st.session_state.history_active_tab,
        key="history_active_tab"
    )
    themed_divider()
        # --- Single ---
    if active_tab == TAB_LABELS[0]:
        if st.session_state.history_active_tab == TAB_LABELS[0]:
            st.markdown("### Recent Single Patch Records")
            if not single_records_all:
                st.info("No single patch history yet.")
            else:
                filtered = []
                for rec in reversed(single_records_all): 
                    text_blob = json.dumps(rec, default=str).lower()
                    if search_text and search_text.lower() not in text_blob:
                        continue
                    if date_from:
                        try:
                            ts = datetime.strptime(rec.get("timestamp", ""), "%Y-%m-%d %H:%M:%S")
                            if ts.date() < date_from:
                                continue
                        except Exception:
                            pass
                    if date_to:
                        try:
                            ts = datetime.strptime(rec.get("timestamp", ""), "%Y-%m-%d %H:%M:%S")
                            if ts.date() > date_to:
                                continue
                        except Exception:
                            pass
                    filtered.append(rec)

                st.markdown(f"Showing **{len(filtered)}** records (most recent first)")
                labels = [f"{r.get('timestamp','?')} — {r.get('prediction_name','-')}" for r in filtered]
                selected = st.multiselect("Select records to export / preview", options=labels, key="history_single_select")

                if selected:
                    sel_indices = [labels.index(s) for s in selected]
                    sel_records = [filtered[i] for i in sel_indices]

                    # --- Export options ---
                    ts_now = datetime.now().strftime("%Y%m%d_%H%M%S")
                    col1, col2 = st.columns(2)
                    with col1:
                        try:
                            csv_bytes = _export_records_as_csv(sel_records, filename_prefix=f"single_history_{ts_now}")
                            st.download_button("⬇️ Download CSV (Selected)", csv_bytes, file_name=f"single_history_{ts_now}.csv", mime="text/csv")
                        except Exception as e:
                            log_error("history.show.single.csv", e)
                            st.error("Could not prepare CSV.")
                    with col2:
                        try:
                            json_bytes = json.dumps(sel_records, indent=2, default=_sanitize_for_json)
                            st.download_button("⬇️ Download JSON (Selected)", json_bytes, file_name=f"single_history_{ts_now}.json", mime="application/json")
                        except Exception as e:
                            log_error("history.show.single.json", e)
                            st.error("Could not prepare JSON.")

                    st.markdown("### Preview / PDF Export")
                    for rec in sel_records:
                        with st.expander(f"Record — {rec.get('timestamp','?')} — {rec.get('prediction_name','Unknown')}"):
                            st.write("**Prediction Details**")
                            st.json({
                                "prediction": rec.get("prediction"),
                                "prediction_name": rec.get("prediction_name"),
                                "confidence": rec.get("confidence"),
                                "inputs": rec.get("inputs"),
                            })

                            probs = rec.get("probabilities", [])
                            if probs:
                                st.write("Probabilities (top 7):")
                                st.write([round(float(x), 4) for x in (probs[:7] if isinstance(probs, (list, tuple)) else probs)])

                            # --- PDF export per record ---
                            col_pdf1, col_pdf2, _ = st.columns([2, 4, 2])
                            with col_pdf1:
                                try:
                                    pdf_bytes = generate_single_patch_pdf(
                                        user_inputs=rec.get("inputs", {}),
                                        predicted_class=int(rec.get("prediction", 0)),
                                        predicted_name=rec.get("prediction_name", "Unknown"),
                                        probabilities=rec.get("probabilities", []),
                                        cover_type_map=COVER_TYPE_MAP,
                                        charts=[str(Path(rec.get("path", "")) / p) for p in ("radar.png", "grid.png", "bar.png")],
                                    )
                                    st.download_button(f"⬇️ PDF ({rec.get('timestamp')})", data=pdf_bytes, file_name=f"single_{rec.get('timestamp')}.pdf", mime="application/pdf")
                                except Exception as e:
                                    log_error("history.show.single.pdf", e)
                                    st.warning("PDF generation failed for this record.")
                            with col_pdf2:
                                p = Path(rec.get("path", ""))
                                if p.exists():
                                    imgs = []
                                    for img_name in ("radar.png", "grid.png", "bar.png"):
                                        img_path = p / img_name
                                        if img_path.exists():
                                            imgs.append(str(img_path))
                                    if imgs:
                                        st.markdown("Saved visualizations:")
                                        for im in imgs:
                                            st.image(im, use_container_width=True)
                else:
                    st.info("Select records above to preview or export.")

    # --- Batch ---
    if active_tab == TAB_LABELS[1]:
        st.markdown("### Recent Batch Records")
        if not batch_records_all:
            st.info("No batch history yet.")
        else:
            filtered_batch = []
            for rec in reversed(batch_records_all):
                text_blob = json.dumps(rec, default=str).lower()
                if search_text and search_text.lower() not in text_blob:
                    continue
                if date_from:
                    try:
                        ts = datetime.strptime(rec.get("timestamp", ""), "%Y-%m-%d %H:%M:%S")
                        if ts.date() < date_from:
                            continue
                    except Exception:
                        pass
                if date_to:
                    try:
                        ts = datetime.strptime(rec.get("timestamp", ""), "%Y-%m-%d %H:%M:%S")
                        if ts.date() > date_to:
                            continue
                    except Exception:
                        pass
                filtered_batch.append(rec)

            st.markdown(f"Showing **{len(filtered_batch)}** batch records (most recent first)")

            labels_b = [
                f"{r.get('timestamp','?')} — {r.get('file', 'batch')}" for r in filtered_batch
            ]

            sel_b = st.multiselect(
                "Select batch records to export/preview",
                options=labels_b,
                key="history_batch_select",
                on_change=lambda: st.session_state.update(history_active_tab=TAB_LABELS[1]),
            )

            if sel_b:
                sel_idx = [labels_b.index(lbl) for lbl in sel_b]
                sel_recs = [filtered_batch[i] for i in sel_idx]

                ts_now = datetime.now().strftime("%Y%m%d_%H%M%S")
                with st.expander("📥 Export Selected Batch Records"):
                    csv_frames = []
                    json_list = []
                    for rec in sel_recs:
                        p = Path(rec.get("path", "")) / "predictions.csv"
                        if p.exists():
                            try:
                                csv_frames.append(pd.read_csv(p))
                            except Exception as exc:
                                log_error("history.show.batch.read_csv", exc)
                        else:
                            if rec.get("predictions_preview"):
                                json_list.append({"predictions_preview": rec.get("predictions_preview")})

                    if csv_frames:
                        try:
                            combined = pd.concat(csv_frames, ignore_index=True)
                            st.download_button(
                                "⬇️ Download Combined CSV",
                                combined.to_csv(index=False).encode("utf-8"),
                                file_name=f"batch_combined_{ts_now}.csv",
                                mime="text/csv",
                            )
                        except Exception as exc:
                            log_error("history.show.batch.concat", exc)
                            st.error("Failed to combine CSVs.")

                    st.download_button(
                        "⬇️ Download JSON (Selected Batch)",
                        json.dumps(sel_recs, indent=2, default=_sanitize_for_json),
                        file_name=f"batch_history_{ts_now}.json",
                        mime="application/json",
                    )

                for rec in sel_recs:
                    with st.expander(f"Batch: {rec.get('file','batch')} — {rec.get('timestamp')}"):
                        st.write(f"Rows processed: {rec.get('rows', 'Unknown')}")
                        csv_path = Path(rec.get("path", "")) / "predictions.csv"
                        if csv_path.exists():
                            try:
                                df_preview = pd.read_csv(csv_path)
                                st.markdown("**Preview (first 10 rows)**")
                                st.dataframe(df_preview.head(10), use_container_width=True)
                            except Exception as exc:
                                log_error("history.show.batch.preview", exc)
                                st.warning("Could not read saved CSV for preview.")
                        else:
                            st.info("No saved CSV found for this record.")

                        for img_name, caption in (
                            ("bar.png", "Distribution Bar Chart"),
                            ("pie.png", "Distribution Pie Chart"),
                            ("box.png", "Feature Boxplots"),
                        ):
                            img_path = Path(rec.get("path", "")) / img_name
                            if img_path.exists():
                                _, col2, _ = st.columns([1, 4, 1])
                                with col2:
                                    st.image(str(img_path), caption=caption, use_container_width=True)
            else:
                st.info("Select one or more batch records above to preview/export.")

    themed_divider()
    st.info("Tip: If history seems out-of-sync, try reloading the page or restarting the app. The history file is stored at `dataset/history.json`.")
