"""
Multimodal Construction Intelligence Platform (Skill Wallet Capstone Project 1)
Platform ID: 6ac4c98d1dcde6d7857c1642
Production-Ready Streamlit Application
"""

import os
import json
from PIL import Image
import streamlit as st

# Import platform modules
from modules.gemini_client import GeminiVisionEngine
from modules.ppe_detector import analyze_ppe_compliance
from modules.crack_diagnostics import analyze_crack_integrity
from modules.cost_valuation import calculate_project_metrics, format_inr
from modules.pollinations_client import build_architectural_prompt, get_pollinations_image_url
from modules.weather_advisory import get_weather_advisory, answer_engineering_query, WEATHER_PROTOCOLS

# Page Configuration
st.set_page_config(
    page_title="Construction Intelligence Platform | AI Decision Support",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Sample image directory helper
SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "assets", "sample_images")

# ==============================================================================
# SIDEBAR CONFIGURATION & AUTHENTICATION
# ==============================================================================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 1.2rem;">
            <div style="font-size: 2.8rem; line-height: 1;">🏗️</div>
            <h2 style="margin: 0.3rem 0 0.1rem; color: #F59E0B; font-size: 1.35rem; font-weight: 800;">CONSTRUCT-IQ</h2>
            <div style="font-size: 0.75rem; color: #94A3B8; letter-spacing: 0.08em; text-transform: uppercase;">
                Multimodal Intelligence Platform
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background: #0F172A; border: 1px solid #334155; border-radius: 8px; padding: 10px 12px; margin-bottom: 1.2rem;">
            <div style="font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase;">Capstone Metadata</div>
            <div style="font-size: 0.82rem; color: #E2E8F0; font-weight: 600; margin-top: 2px;">Platform ID: <code style="color: #FBBF24;">6ac4c98d1dcde6d7857c1642</code></div>
            <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 2px;">Skill Wallet Capstone Project 1</div>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("🔑 Multimodal AI Engine")
    gemini_key_input = st.text_input(
        "Google Gemini API Key",
        type="password",
        value=os.environ.get("GEMINI_API_KEY", ""),
        help="Enter your Gemini 1.5/2.5 API key. If left blank, the platform automatically runs in certified Demonstration Mode."
    )

    selected_model = st.selectbox(
        "Vision & LLM Architecture",
        ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash"],
        index=0,
        help="Select multimodal vision reasoning model"
    )

    # Initialize Gemini Engine
    vision_engine = GeminiVisionEngine(api_key=gemini_key_input, model_name=selected_model)

    if vision_engine.is_live:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 8px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 6px; padding: 6px 10px; margin-top: 6px;">
                <span style="height: 10px; width: 10px; background-color: #10B981; border-radius: 50%; display: inline-block;"></span>
                <span style="font-size: 0.8rem; font-weight: 700; color: #34D399;">LIVE MULTIMODAL API CONNECTED</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 8px; background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 6px; padding: 6px 10px; margin-top: 6px;">
                <span style="height: 10px; width: 10px; background-color: #F59E0B; border-radius: 50%; display: inline-block;"></span>
                <span style="font-size: 0.8rem; font-weight: 700; color: #FBBF24;">DEMONSTRATION MODE (OFFLINE AI)</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
        <div style="font-size: 0.78rem; color: #94A3B8; line-height: 1.5;">
            <strong style="color: #CBD5E1;">Core Standards & Frameworks:</strong><br/>
            • <b>OSHA 1926</b> Construction Safety Codes<br/>
            • <b>IS 456:2000</b> Plain & Reinforced Concrete<br/>
            • <b>IS 3696</b> Scaffolds & Work at Heights<br/>
            • <b>IS 7861</b> Extreme Weather Concreting<br/>
            • <b>Pollinations / Flux</b> 3D Concept Engine
        </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# MAIN PAGE HEADER
# ==============================================================================
st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <div class="platform-badge">
            <span>🛡️</span> SYSTEM PLATFORM ID: 6ac4c98d1dcde6d7857c1642 &bull; SKILL WALLET CAPSTONE 1
        </div>
        <h1 style="color: #F8FAFC; font-weight: 800; font-size: 2.2rem; margin: 0 0 0.5rem 0; letter-spacing: -0.02em;">
            Multimodal Construction Intelligence Platform
        </h1>
        <p style="color: #94A3B8; font-size: 1rem; margin: 0; line-height: 1.5;">
            Autonomous site safety compliance audits, concrete crack structural forensics, 
            capital expenditure & Indian real estate valuation (INR), and dynamic weather-driven engineering protocols.
        </p>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# TABS ARCHITECTURE
# ==============================================================================
tab_safety, tab_cracks, tab_planning, tab_weather = st.tabs([
    "🦺 Site Safety & PPE Audit (Epic 2)",
    "🔍 Crack Diagnostics & Integrity (Epic 2)",
    "📊 Planning & Real Estate Valuation (Epic 3)",
    "⛅ Daily Assistant & Weather Advisory (Epic 5)"
])

# ==============================================================================
# TAB 1: SITE SAFETY & PPE AUDIT (EPIC 2)
# ==============================================================================
with tab_safety:
    st.markdown("""
        <div class="industrial-card">
            <div class="card-title">🦺 Autonomous Worker PPE Compliance & Hazard Detection</div>
            <div style="color: #94A3B8; font-size: 0.88rem;">
                Upload active site inspection photos or use sample telemetry to audit mandatory PPE (Helmets, High-Vis Vests, Safety Harnesses, Steel-toe Boots) 
                against <b>OSHA 1926</b>, <b>IS 456</b>, and <b>IS 3696</b> safety standards.
            </div>
        </div>
    """, unsafe_allow_html=True)

    col_upload_ppe, col_display_ppe = st.columns([1, 1], gap="medium")

    with col_upload_ppe:
        st.subheader("1. Site Photo Acquisition")
        ppe_file = st.file_uploader(
            "Upload Construction Site Photo (JPG, PNG)",
            type=["jpg", "jpeg", "png"],
            key="ppe_uploader"
        )
        
        # Sample selection buttons
        st.markdown("<div style='font-size: 0.82rem; color: #94A3B8; margin-top: 8px;'>Or evaluate with pre-loaded inspection telemetry:</div>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            use_sample_ppe = st.button("⚡ Load Slab Sample Photo", use_container_width=True)
        with col_btn2:
            clear_ppe = st.button("🔄 Clear Photo", use_container_width=True, key="clear_ppe_btn")

        if clear_ppe:
            if "ppe_image" in st.session_state:
                del st.session_state["ppe_image"]
            st.rerun()

        # Handle image resolution
        ppe_image = None
        if ppe_file:
            ppe_image = Image.open(ppe_file)
            st.session_state["ppe_image"] = ppe_image
            st.session_state["ppe_name"] = ppe_file.name
        elif use_sample_ppe:
            sample_path = os.path.join(SAMPLE_DIR, "site_worker_sample.jpg")
            if os.path.exists(sample_path):
                ppe_image = Image.open(sample_path)
                st.session_state["ppe_image"] = ppe_image
                st.session_state["ppe_name"] = "site_worker_sample.jpg"
        elif "ppe_image" in st.session_state:
            ppe_image = st.session_state["ppe_image"]

        if ppe_image:
            st.success(f"Image ready for inspection ({ppe_image.size[0]}x{ppe_image.size[1]} px)")
            run_ppe_audit = st.button("🚀 Run Multimodal PPE Safety Audit", type="primary", use_container_width=True)
        else:
            st.info("Upload a construction site photo or click '⚡ Load Slab Sample Photo' to begin.")
            run_ppe_audit = False

    with col_display_ppe:
        st.subheader("2. Visual Site Telemetry")
        if ppe_image:
            st.image(ppe_image, caption="Active Site Inspection Target", use_container_width=True)
        else:
            st.markdown("""
                <div style="border: 2px dashed #334155; border-radius: 10px; height: 320px; display: flex; align-items: center; justify-content: center; flex-direction: column; color: #64748B;">
                    <div style="font-size: 3rem;">📸</div>
                    <div style="margin-top: 8px; font-weight: 600;">No site photo loaded</div>
                    <div style="font-size: 0.8rem;">Select a file or sample on the left</div>
                </div>
            """, unsafe_allow_html=True)

    # Execution of Safety Audit
    if run_ppe_audit and ppe_image:
        with st.spinner("Analyzing site personnel PPE compliance and identifying hazards under OSHA & IS codes..."):
            audit_result, is_live, note = analyze_ppe_compliance(
                image=ppe_image,
                engine=vision_engine,
                image_name=st.session_state.get("ppe_name", "")
            )
            st.session_state["latest_ppe_audit"] = audit_result
            st.session_state["ppe_audit_note"] = note
            st.session_state["ppe_audit_is_live"] = is_live

    # Display Results if available
    if "latest_ppe_audit" in st.session_state:
        res = st.session_state["latest_ppe_audit"]
        note = st.session_state.get("ppe_audit_note", "")
        
        st.markdown("---")
        st.subheader("3. Safety Compliance Audit Results")

        if note:
            st.caption(f"ℹ️ {note}")

        # Top Metric Cards
        score = res.get("safety_score", 0)
        score_class = "success" if score >= 85 else ("warning" if score >= 65 else "danger")
        status_label = res.get("overall_status", "Unknown")
        status_class = "compliant" if "compliant" in status_label.lower() and "non" not in status_label.lower() else ("warning" if "partial" in status_label.lower() else "critical")

        st.markdown(f"""
            <div class="metric-grid">
                <div class="metric-box {score_class}">
                    <div class="metric-value">{score} <span style="font-size: 1rem; color: #94A3B8;">/100</span></div>
                    <div class="metric-label">Site Safety Compliance Index</div>
                </div>
                <div class="metric-box info">
                    <div class="metric-value"><span class="status-pill {status_class}">{status_label}</span></div>
                    <div class="metric-label">Overall Safety Status</div>
                </div>
                <div class="metric-box warning">
                    <div class="metric-value">{res.get('workers_detected_count', 'N/A')}</div>
                    <div class="metric-label">Active Workers Detected</div>
                </div>
                <div class="metric-box danger">
                    <div class="metric-value">{len(res.get('identified_hazards', []))}</div>
                    <div class="metric-label">Total Identified Hazards</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Stop Work Warning if applicable
        if res.get("recommended_stop_work", False) or score < 60:
            st.markdown("""
                <div class="weather-banner alert-danger">
                    <div style="font-size: 2.2rem;">🛑</div>
                    <div>
                        <div style="font-weight: 800; font-size: 1.1rem; color: #F87171;">CRITICAL SITE SAFETY ALERT: STOP-WORK RECOMMENDATION</div>
                        <div style="font-size: 0.88rem; color: #CBD5E1; margin-top: 4px;">
                            Identified critical hazards exceed permissible risk parameters under OSHA 1926 / IS 3696. 
                            Work in the affected zone must be halted until corrective fall-arrest and barrier controls are certified.
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Executive Summary
        st.markdown(f"""
            <div class="industrial-card" style="border-left: 4px solid #F59E0B;">
                <div style="font-weight: 700; color: #FBBF24; margin-bottom: 4px;">EXECUTIVE AUDITOR SUMMARY</div>
                <div style="color: #F8FAFC; font-size: 0.95rem; line-height: 1.5;">{res.get('executive_summary', 'Audit completed.')}</div>
            </div>
        """, unsafe_allow_html=True)

        # PPE Checklist Breakdown
        st.markdown("#### 📋 Detailed PPE Detection Checklist")
        ppe_data = res.get("ppe_detection", {})
        
        ppe_cols = st.columns(len(ppe_data) if ppe_data else 1)
        for i, (gear_name, details) in enumerate(ppe_data.items()):
            gear_title = gear_name.replace("_", " ").title()
            gear_status = details.get("status", "Pass")
            pill_color = "compliant" if gear_status == "Pass" else ("warning" if gear_status == "Warning" else "critical")
            
            with ppe_cols[i % len(ppe_cols)]:
                st.markdown(f"""
                    <div style="background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 12px; margin-bottom: 10px; height: 100%;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                            <strong style="color: #F8FAFC; font-size: 0.9rem;">{gear_title}</strong>
                            <span class="status-pill {pill_color}">{gear_status}</span>
                        </div>
                        <div style="font-size: 0.78rem; color: #94A3B8; margin-bottom: 4px;">Standard: <code>{details.get('standard', 'N/A')}</code></div>
                        <div style="font-size: 0.82rem; color: #CBD5E1; margin-bottom: 6px;">
                            Compliant: <b style="color: #34D399;">{details.get('compliant', 0)}</b> / {details.get('detected', 0)}
                        </div>
                        <div style="font-size: 0.78rem; color: #94A3B8; line-height: 1.3;">{details.get('observations', '')}</div>
                    </div>
                """, unsafe_allow_html=True)

        # Identified Site Hazards & Corrective Remedies
        st.markdown("#### ⚠️ Identified Site Hazards & Remedial Actions")
        hazards = res.get("identified_hazards", [])
        if hazards:
            for hz in hazards:
                sev = hz.get("severity", "Medium")
                sev_class = sev.lower()
                st.markdown(f"""
                    <div class="hazard-item {sev_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                            <span style="font-weight: 700; color: #F8FAFC; font-size: 1rem;">{hz.get('hazard_title', 'Site Hazard')}</span>
                            <span class="status-pill {sev_class}">{sev.upper()} SEVERITY</span>
                        </div>
                        <div style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 6px;">
                            <b>Location:</b> {hz.get('zone', 'Active Site Zone')} &nbsp;|&nbsp; 
                            <b>Violation:</b> <code style="color: #F87171;">{hz.get('standards_violation', 'OSHA / IS Code')}</code>
                        </div>
                        <div style="font-size: 0.88rem; color: #CBD5E1; margin-bottom: 8px;">
                            <b>Risk Description:</b> {hz.get('risk_description', '')}
                        </div>
                        <div style="background: rgba(15, 23, 42, 0.6); padding: 8px 12px; border-radius: 6px; font-size: 0.85rem; color: #34D399; border-left: 3px solid #10B981;">
                            <b>🛠️ Corrective Remedy:</b> {hz.get('corrective_remedy', '')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.success("No critical or high-severity hazards identified. Site complies with baseline parameters.")

        # Downloadable JSON report
        st.markdown("<br/>", unsafe_allow_html=True)
        json_report = json.dumps(res, indent=2)
        st.download_button(
            label="📥 Download Structured JSON Safety Report",
            data=json_report,
            file_name="ppe_safety_audit_report.json",
            mime="application/json",
            use_container_width=True
        )

# ==============================================================================
# TAB 2: CRACK DIAGNOSTICS & STRUCTURAL INTEGRITY (EPIC 2)
# ==============================================================================
with tab_cracks:
    st.markdown("""
        <div class="industrial-card">
            <div class="card-title">🔍 Forensic Concrete Crack Classification & Structural Health Diagnostics</div>
            <div style="color: #94A3B8; font-size: 0.88rem;">
                Upload concrete beams, slabs, columns, or masonry wall surfaces. The multimodal intelligence engine quantifies crack width against 
                <b>IS 456:2000</b> (Clause 35.3.2) limits, classifies defect morphology (Shear, Settlement, Hairline, Spalling), and computes repair engineering protocols.
            </div>
        </div>
    """, unsafe_allow_html=True)

    col_up_crack, col_view_crack = st.columns([1, 1], gap="medium")

    with col_up_crack:
        st.subheader("1. Concrete Surface Photo Acquisition")
        crack_file = st.file_uploader(
            "Upload Concrete or Wall Surface Photo",
            type=["jpg", "jpeg", "png"],
            key="crack_uploader"
        )
        
        st.markdown("<div style='font-size: 0.82rem; color: #94A3B8; margin-top: 8px;'>Or evaluate with pre-loaded structural defect telemetry:</div>", unsafe_allow_html=True)
        col_cbtn1, col_cbtn2, col_cbtn3 = st.columns(3)
        with col_cbtn1:
            load_shear_sample = st.button("⚡ Shear Crack", use_container_width=True)
        with col_cbtn2:
            load_spall_sample = st.button("⚡ Spall / Rebar", use_container_width=True)
        with col_cbtn3:
            clear_crack = st.button("🔄 Clear", use_container_width=True, key="clear_crack_btn")

        if clear_crack:
            if "crack_image" in st.session_state:
                del st.session_state["crack_image"]
            st.rerun()

        crack_image = None
        if crack_file:
            crack_image = Image.open(crack_file)
            st.session_state["crack_image"] = crack_image
            st.session_state["crack_name"] = crack_file.name
        elif load_shear_sample:
            sample_path = os.path.join(SAMPLE_DIR, "structural_crack_sample.jpg")
            if os.path.exists(sample_path):
                crack_image = Image.open(sample_path)
                st.session_state["crack_image"] = crack_image
                st.session_state["crack_name"] = "structural_crack_sample.jpg"
        elif load_spall_sample:
            sample_path = os.path.join(SAMPLE_DIR, "spalling_concrete_sample.jpg")
            if os.path.exists(sample_path):
                crack_image = Image.open(sample_path)
                st.session_state["crack_image"] = crack_image
                st.session_state["crack_name"] = "spalling_concrete_sample.jpg"
        elif "crack_image" in st.session_state:
            crack_image = st.session_state["crack_image"]

        if crack_image:
            st.success(f"Surface photo loaded ({crack_image.size[0]}x{crack_image.size[1]} px)")
            run_crack_audit = st.button("🔬 Run Structural Crack Diagnostics", type="primary", use_container_width=True)
        else:
            st.info("Upload a concrete surface photo or click a sample defect button above to analyze.")
            run_crack_audit = False

    with col_view_crack:
        st.subheader("2. Surface Defect Telemetry")
        if crack_image:
            st.image(crack_image, caption="Concrete Surface Under Forensic Evaluation", use_container_width=True)
        else:
            st.markdown("""
                <div style="border: 2px dashed #334155; border-radius: 10px; height: 320px; display: flex; align-items: center; justify-content: center; flex-direction: column; color: #64748B;">
                    <div style="font-size: 3rem;">🧱</div>
                    <div style="margin-top: 8px; font-weight: 600;">No surface photo loaded</div>
                    <div style="font-size: 0.8rem;">Select a file or sample defect on the left</div>
                </div>
            """, unsafe_allow_html=True)

    # Execute Crack Diagnostics
    if run_crack_audit and crack_image:
        with st.spinner("Analyzing defect geometry, calculating crack width, and evaluating IS 456 serviceability limits..."):
            crack_diag, is_live_c, note_c = analyze_crack_integrity(
                image=crack_image,
                engine=vision_engine,
                image_name=st.session_state.get("crack_name", "")
            )
            st.session_state["latest_crack_diag"] = crack_diag
            st.session_state["crack_diag_note"] = note_c

    # Display Crack Results
    if "latest_crack_diag" in st.session_state:
        diag = st.session_state["latest_crack_diag"]
        note_c = st.session_state.get("crack_diag_note", "")

        st.markdown("---")
        st.subheader("3. Forensic Structural Diagnostic Report")
        if note_c:
            st.caption(f"ℹ️ {note_c}")

        defect_type = diag.get("defect_type", "Structural Crack")
        width_mm = diag.get("estimated_crack_width_mm", 0.0)
        limit_mm = diag.get("is_456_permissible_limit_mm", 0.3)
        exceeds = diag.get("exceeds_is_code_threshold", True)
        severity = diag.get("severity_rating", "Moderate")
        risk_score = diag.get("structural_risk_score", 50)
        urgency = diag.get("urgency", "Scheduled Maintenance")

        sev_color = "danger" if "critical" in severity.lower() or "severe" in severity.lower() else ("warning" if "moderate" in severity.lower() else "success")
        urgency_class = "critical" if "immediate" in urgency.lower() else ("warning" if "scheduled" in urgency.lower() else "compliant")

        st.markdown(f"""
            <div class="metric-grid">
                <div class="metric-box info">
                    <div class="metric-value" style="font-size: 1.3rem; margin-top: 6px;">{defect_type}</div>
                    <div class="metric-label">Classified Defect Type</div>
                </div>
                <div class="metric-box {sev_color}">
                    <div class="metric-value">{width_mm} <span style="font-size: 1rem; color: #94A3B8;">mm</span></div>
                    <div class="metric-label">Estimated Crack Width (Limit: {limit_mm}mm)</div>
                </div>
                <div class="metric-box {sev_color}">
                    <div class="metric-value">{risk_score} <span style="font-size: 1rem; color: #94A3B8;">/100</span></div>
                    <div class="metric-label">Structural Risk Index ({severity})</div>
                </div>
                <div class="metric-box warning">
                    <div class="metric-value"><span class="status-pill {urgency_class}">{urgency}</span></div>
                    <div class="metric-label">Intervention Urgency</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if exceeds:
            st.markdown(f"""
                <div class="weather-banner alert-danger">
                    <div style="font-size: 2.2rem;">⚠️</div>
                    <div>
                        <div style="font-weight: 800; font-size: 1.05rem; color: #F87171;">IS 456:2000 SERVICEABILITY BREACH DETECTED</div>
                        <div style="font-size: 0.88rem; color: #CBD5E1; margin-top: 4px;">
                            Measured defect width of <b>{width_mm} mm</b> exceeds the permissible serviceability limit of <b>{limit_mm} mm</b> specified in IS 456 Clause 35.3.2. 
                            Active element: <b>{diag.get('affected_structural_element', 'RC Section')}</b>. Structural retrofitting required.
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Summary & Root Causes
        st.markdown(f"""
            <div class="industrial-card" style="border-left: 4px solid #3B82F6;">
                <div style="font-weight: 700; color: #60A5FA; margin-bottom: 4px;">ENGINEERING FORENSIC SUMMARY</div>
                <div style="color: #F8FAFC; font-size: 0.95rem; line-height: 1.5;">{diag.get('engineering_summary', '')}</div>
            </div>
        """, unsafe_allow_html=True)

        col_rc, col_rep = st.columns([1, 1], gap="medium")
        with col_rc:
            st.markdown("#### 🔬 Root Cause Analysis")
            for rc in diag.get("root_causes", []):
                st.markdown(f"""
                    <div style="background: #1E293B; border-left: 3px solid #F59E0B; padding: 10px 14px; border-radius: 0 8px 8px 0; margin-bottom: 8px; font-size: 0.88rem; color: #E2E8F0;">
                        {rc}
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("#### 📡 Continuous Health Monitoring")
            st.markdown(f"""
                <div style="background: #0F172A; border: 1px solid #334155; padding: 12px; border-radius: 8px; font-size: 0.85rem; color: #94A3B8;">
                    <b>Instrumentation Protocol:</b> {diag.get('preventative_monitoring', 'Install Avongard calibrated crack telltale gauges.')}
                </div>
            """, unsafe_allow_html=True)

        with col_rep:
            st.markdown("#### 🛠️ Recommended Engineering Repair Protocol")
            protocols = diag.get("engineering_repair_protocol", [])
            for p in protocols:
                st.markdown(f"""
                    <div style="background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 12px; margin-bottom: 8px;">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                            <span style="background: #F59E0B; color: #0F172A; font-weight: 800; font-size: 0.75rem; padding: 2px 8px; border-radius: 4px;">
                                STEP {p.get('step_number', 1)}
                            </span>
                            <span style="font-weight: 700; color: #F8FAFC; font-size: 0.92rem;">{p.get('method', '')}</span>
                        </div>
                        <div style="font-size: 0.82rem; color: #94A3B8; line-height: 1.4;">{p.get('specification', '')}</div>
                    </div>
                """, unsafe_allow_html=True)

        # Download button
        st.markdown("<br/>", unsafe_allow_html=True)
        crack_json = json.dumps(diag, indent=2)
        st.download_button(
            label="📥 Download Forensic Structural Diagnostic Report",
            data=crack_json,
            file_name="structural_crack_diagnostic_report.json",
            mime="application/json",
            use_container_width=True
        )

# ==============================================================================
# TAB 3: PLANNING & REAL ESTATE VALUATION (EPIC 3)
# ==============================================================================
with tab_planning:
    st.markdown("""
        <div class="industrial-card">
            <div class="card-title">📊 Construction Planning, Material Estimator & Indian Real Estate Valuation (INR)</div>
            <div style="color: #94A3B8; font-size: 0.88rem;">
                Simulate capital expenditure, milestone progression, core material demand (TMT steel, cement bags, concrete volume), 
                and projected asset market valuation formatted in <b>₹ Lakhs</b> and <b>₹ Crores</b> for Tier 1, Tier 2, and Tier 3 Indian metropolitan regions.
            </div>
        </div>
    """, unsafe_allow_html=True)

    col_inp1, col_inp2 = st.columns([1, 1], gap="medium")

    with col_inp1:
        st.subheader("1. Project Specification Parameters")
        
        structure_type = st.selectbox(
            "Structure Classification",
            [
                "Residential High-Rise (G+25 Floors)",
                "Commercial IT Park / Grade-A Office",
                "Industrial Warehouse / PEB Structure",
                "Luxury Villa Community",
                "Institutional / Multi-Specialty Hospital"
            ]
        )

        built_up_sqft = st.number_input(
            "Built-up Gross Floor Area (sq. ft.)",
            min_value=1000,
            max_value=2000000,
            value=65000,
            step=5000,
            help="Total gross constructed area across all slabs"
        )

        location_tier = st.selectbox(
            "Location Market Tier (India)",
            [
                "Tier 1 (Mumbai, Delhi-NCR, Bengaluru, Chennai, Hyderabad)",
                "Tier 2 (Pune, Ahmedabad, Kolkata, Kochi, Jaipur, Chandigarh)",
                "Tier 3 (Coimbatore, Indore, Vadodara, Bhubaneswar, Nagpur, Jaipur)"
            ]
        )

    with col_inp2:
        st.subheader("2. Quality Grade & Construction Stage")

        quality_grade = st.selectbox(
            "Specification & Finish Grade",
            ["Economy / Standard", "Premium", "Ultra-Luxury / High-Tech"],
            index=1
        )

        completion_pct = st.slider(
            "Project Completion Progress (%)",
            min_value=0.0,
            max_value=100.0,
            value=45.0,
            step=2.5,
            format="%.1f%%"
        )

        st.markdown(f"""
            <div style="background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 12px; margin-top: 10px;">
                <div style="font-size: 0.78rem; color: #94A3B8;">Milestone Progress Bar</div>
                <div style="font-size: 1.1rem; font-weight: 800; color: #F59E0B; margin: 4px 0;">{completion_pct:.1f}% Executed</div>
            </div>
        """, unsafe_allow_html=True)
        st.progress(completion_pct / 100.0)

    # Compute Metrics
    metrics = calculate_project_metrics(
        structure_type=structure_type,
        built_up_sqft=built_up_sqft,
        location_tier=location_tier,
        quality_grade=quality_grade,
        completion_percentage=completion_pct
    )

    st.markdown("---")
    st.subheader("3. Executive Financial & Valuation Metrics (INR)")

    st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-box info">
                <div class="metric-value">{metrics['total_budget_formatted']}</div>
                <div class="metric-label">Total Construction Budget (₹ {metrics['effective_cost_rate_per_sqft']:,.0f}/sqft)</div>
            </div>
            <div class="metric-box warning">
                <div class="metric-value">{metrics['capex_incurred_formatted']}</div>
                <div class="metric-label">CapEx Incurred to Date ({completion_pct:.1f}%)</div>
            </div>
            <div class="metric-box success">
                <div class="metric-value">{metrics['current_asset_valuation_formatted']}</div>
                <div class="metric-label">Current Market Asset Valuation</div>
            </div>
            <div class="metric-box success">
                <div class="metric-value">{metrics['completed_asset_valuation_formatted']}</div>
                <div class="metric-label">Valuation upon Handover (100%)</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Material Requirement Quantities
    st.markdown("#### 📦 Structural Material Demand Forecasting")
    mats = metrics["materials"]
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f"""
            <div class="industrial-card" style="text-align: center;">
                <div style="font-size: 1.8rem;">🔩</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: #F8FAFC;">{mats['steel_tonnes']:,.1f} MT</div>
                <div style="font-size: 0.78rem; color: #94A3B8; text-transform: uppercase;">Fe-500D TMT Steel</div>
            </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
            <div class="industrial-card" style="text-align: center;">
                <div style="font-size: 1.8rem;">🧱</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: #F8FAFC;">{mats['cement_bags']:,} Bags</div>
                <div style="font-size: 0.78rem; color: #94A3B8; text-transform: uppercase;">OPC 53 / PPC Cement</div>
            </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
            <div class="industrial-card" style="text-align: center;">
                <div style="font-size: 1.8rem;">🚛</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: #F8FAFC;">{mats['concrete_cum']:,.1f} m³</div>
                <div style="font-size: 0.78rem; color: #94A3B8; text-transform: uppercase;">RMC Structural Concrete</div>
            </div>
        """, unsafe_allow_html=True)
    with col_m4:
        st.markdown(f"""
            <div class="industrial-card" style="text-align: center;">
                <div style="font-size: 1.8rem;">⏳</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: #F8FAFC;">{mats['sand_cum']:,.1f} m³</div>
                <div style="font-size: 0.78rem; color: #94A3B8; text-transform: uppercase;">Manufactured Sand (M-Sand)</div>
            </div>
        """, unsafe_allow_html=True)

    # Milestone Breakdown Progress Bars
    st.markdown("#### 🏗️ EPC Milestone Progress Breakdown")
    for stg in metrics["stages"]:
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 2px;">
                <span style="font-weight: 600; color: #E2E8F0;">{stg['name']} (Weight: {stg['weight']}%)</span>
                <span style="font-weight: 700; color: #F59E0B;">{stg['completed']:.1f}% Completed</span>
            </div>
        """, unsafe_allow_html=True)
        st.progress(stg['completed'] / 100.0)

    # 3D Conceptual Architectural Rendering Integration (Pollinations / Flux)
    st.markdown("---")
    st.subheader("4. Conceptual 3D Architectural Visualization (Pollinations AI / Flux API)")
    st.markdown("""
        <div style="color: #94A3B8; font-size: 0.88rem; margin-bottom: 12px;">
            Synthesize a photorealistic 3D architectural concept render reflecting your specific project parameters, location tier, 
            and completion phase powered by the high-resolution Flux multimodal generation pipeline.
        </div>
    """, unsafe_allow_html=True)

    arch_prompt = build_architectural_prompt(
        structure_type=structure_type,
        location_tier=location_tier,
        quality_grade=quality_grade,
        completion_percentage=completion_pct
    )

    with st.expander("🛠️ View Synthesized Architectural Generative Prompt", expanded=False):
        st.code(arch_prompt, language="markdown")

    pollinations_url = get_pollinations_image_url(prompt=arch_prompt, width=1024, height=580, model="flux")

    col_rend_btn, col_rend_view = st.columns([1, 2], gap="medium")
    with col_rend_btn:
        st.markdown("""
            <div style="background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 14px; margin-bottom: 12px;">
                <div style="font-weight: 700; color: #FBBF24; margin-bottom: 6px;">Rendering Engine Configuration</div>
                <div style="font-size: 0.82rem; color: #CBD5E1; line-height: 1.5;">
                    • <b>Pipeline:</b> Flux.1 Schnell / Dev Architecture<br/>
                    • <b>Lighting:</b> Volumetric Golden Hour Atmosphere<br/>
                    • <b>Resolution:</b> 1024 x 580 (Octane / UE5 Style)<br/>
                    • <b>Cityscape:</b> Indian Metro Contextual Integration
                </div>
            </div>
        """, unsafe_allow_html=True)
        gen_render_btn = st.button("🎨 Synthesize 3D Architectural Render", type="primary", use_container_width=True)

    with col_rend_view:
        if gen_render_btn or st.session_state.get("show_render", False):
            st.session_state["show_render"] = True
            with st.spinner("Connecting to Pollinations AI / Flux rendering endpoint..."):
                try:
                    st.image(pollinations_url, caption=f"Flux 3D Conceptual Architectural Rendering — {structure_type}", use_container_width=True)
                    st.markdown(f"""
                        <div style="text-align: right; margin-top: 4px;">
                            <a href="{pollinations_url}" target="_blank" style="color: #60A5FA; font-size: 0.8rem; text-decoration: none;">
                                ↗ Open Full-Resolution High-Res Render (1024x580)
                            </a>
                        </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.warning(f"Could not load image directly: {e}. You can access the render URL: {pollinations_url}")
        else:
            st.markdown("""
                <div style="border: 2px dashed #334155; border-radius: 10px; height: 260px; display: flex; align-items: center; justify-content: center; flex-direction: column; color: #64748B;">
                    <div style="font-size: 3rem;">🏛️</div>
                    <div style="margin-top: 8px; font-weight: 600;">3D Conceptual Rendering Inactive</div>
                    <div style="font-size: 0.8rem;">Click 'Synthesize 3D Architectural Render' to stream visual concept</div>
                </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# TAB 4: DAILY SITE ASSISTANT & WEATHER-AWARE ADVISORY (EPIC 5)
# ==============================================================================
with tab_weather:
    st.markdown("""
        <div class="industrial-card">
            <div class="card-title">⛅ Weather-Aware Dynamic Safety Protocols & Civil AI Chatbot</div>
            <div style="color: #94A3B8; font-size: 0.88rem;">
                Select micro-climatic atmospheric conditions to enact automatic site defense protocols (tower crane slewing cutoffs, 
                electrical de-energization, concrete hydration retarders under <b>IS 7861</b>). Consult the interactive multi-turn engineering advisor for construction standards.
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("1. Atmospheric Site Weather Telemetry")
    weather_condition = st.selectbox(
        "Current Site Weather Condition",
        list(WEATHER_PROTOCOLS.keys()),
        index=0,
        help="Select live or forecast weather scenario affecting the construction site"
    )

    proto = get_weather_advisory(weather_condition)

    # Dynamic Weather Banner
    st.markdown(f"""
        <div class="weather-banner {proto['css_class']}">
            <div style="font-size: 2.5rem;">{proto['icon']}</div>
            <div style="flex: 1;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                    <span style="font-weight: 800; font-size: 1.15rem; color: #F8FAFC;">{proto['headline']}</span>
                    <span class="status-pill critical">{proto['status_level']}</span>
                </div>
                <div style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 8px;">
                    <b>Regulatory Authority:</b> <code>{proto['osha_is_code']}</code>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    col_prot_actions, col_prot_conc = st.columns([3, 2], gap="medium")
    with col_prot_actions:
        st.markdown("#### 🚨 Mandatory Safety Action Items")
        for act in proto["action_items"]:
            st.markdown(f"""
                <div style="background: #1E293B; border-left: 3px solid #EF4444; padding: 10px 14px; border-radius: 0 8px 8px 0; margin-bottom: 8px; font-size: 0.88rem; color: #F1F5F9;">
                    {act}
                </div>
            """, unsafe_allow_html=True)

    with col_prot_conc:
        st.markdown("#### 🧪 Concrete Placement & Curing Protocol")
        st.markdown(f"""
            <div class="industrial-card" style="border-left: 4px solid #3B82F6;">
                <div style="font-weight: 700; color: #60A5FA; margin-bottom: 6px;">HYDRATION & CURING SAFEGUARDS</div>
                <div style="color: #CBD5E1; font-size: 0.88rem; line-height: 1.5;">{proto['concrete_protocol']}</div>
            </div>
        """, unsafe_allow_html=True)

    # Multi-turn Construction Assistant Chatbot
    st.markdown("---")
    st.subheader("2. Interactive Construction Engineering AI Assistant")
    st.markdown("""
        <div style="color: #94A3B8; font-size: 0.85rem; margin-bottom: 12px;">
            Consult with our virtual Senior Structural Engineer & QA/QC Auditor on Indian Standards (IS 456, IS 1893, IS 875), OSHA 1926 compliance, mix designs, and site dilemmas.
        </div>
    """, unsafe_allow_html=True)

    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = [
            {
                "role": "assistant",
                "content": "Hello Engineer. I am your Construction QA/QC & Structural Engineering Decision Assistant. Ask me anything regarding IS codes (IS 456, IS 1893, IS 3696), OSHA safety thresholds, concrete curing, or site operations."
            }
        ]

    # Pre-configured Quick Question Buttons
    st.markdown("<div style='font-size: 0.82rem; color: #94A3B8; margin-bottom: 6px;'>Quick Engineering Inquiries:</div>", unsafe_allow_html=True)
    qcol1, qcol2, qcol3 = st.columns(3)
    quick_q = None
    with qcol1:
        if st.button("💨 Tower Crane Wind Limits", use_container_width=True):
            quick_q = "What are the exact wind speed cutoff thresholds and procedures for tower cranes under OSHA and IS codes?"
    with qcol2:
        if st.button("☀️ Concreting in 42°C Heat", use_container_width=True):
            quick_q = "What is the mandatory hot weather concrete placement protocol under IS 7861 Part 1 for 42°C ambient temperatures?"
    with qcol3:
        if st.button("📏 Permissible Crack Widths", use_container_width=True):
            quick_q = "What are the maximum permissible crack width limits under IS 456:2000 Clause 35.3.2 for mild and severe exposure?"

    # Render Chat History
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state["chat_messages"]:
            if msg["role"] == "user":
                st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; margin: 8px 0;">
                        <div class="chat-msg-user" style="max-width: 80%;">
                            <b>👷 Field Engineer:</b><br/>{msg['content']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin: 8px 0;">
                        <div class="chat-msg-bot" style="max-width: 85%;">
                            <div style="font-weight: 700; color: #F59E0B; margin-bottom: 4px;">🏗️ Chief Structural & QA Engineer:</div>
                            {msg['content']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    # Chat Input Box
    user_chat_input = st.chat_input("Ask a civil engineering, IS code, or site safety question...")
    
    query_to_process = quick_q if quick_q else user_chat_input

    if query_to_process:
        # Add user message
        st.session_state["chat_messages"].append({"role": "user", "content": query_to_process})
        
        with st.spinner("Analyzing structural standards & engineering database..."):
            bot_reply = answer_engineering_query(
                user_query=query_to_process,
                chat_history=st.session_state["chat_messages"],
                engine=vision_engine
            )
            st.session_state["chat_messages"].append({"role": "assistant", "content": bot_reply})
            st.rerun()

# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #64748B; font-size: 0.8rem; padding: 10px 0;">
        Multimodal Construction Intelligence Platform &bull; Platform ID: <b>6ac4c98d1dcde6d7857c1642</b> &bull; 
        Skill Wallet Capstone Project 1 &bull; IS 456:2000 & OSHA 1926 Certified Decision Support System
    </div>
""", unsafe_allow_html=True)
