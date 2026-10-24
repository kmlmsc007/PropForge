import streamlit as st
import subprocess
import sys
import os
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="PropForge: AI Quantum Testing",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom modern CSS for a premium quantum dark theme
st.markdown(
    """
    <style>
        /* Base typography & palette */
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Outfit:wght@300;500;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }

        code, pre {
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* Hero header */
        .hero-container {
            background: linear-gradient(135deg, rgba(17, 24, 39, 0.8) 0%, rgba(30, 41, 59, 0.9) 100%);
            border: 1px solid rgba(99, 102, 241, 0.25);
            border-radius: 16px;
            padding: 24px 32px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(99, 102, 241, 0.1);
        }

        .hero-title {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(90deg, #60a5fa, #a855f7, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
        }

        .hero-subtitle {
            color: #94a3b8;
            font-size: 1.05rem;
            margin: 0;
        }

        /* Glass Cards */
        .glass-card {
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid rgba(148, 163, 184, 0.12);
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 20px;
            backdrop-filter: blur(12px);
        }

        .section-header {
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 700;
            font-size: 1.25rem;
            color: #e2e8f0;
            margin-bottom: 14px;
            border-bottom: 1px solid rgba(148, 163, 184, 0.15);
            padding-bottom: 8px;
        }

        /* Badges */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
        }

        .status-success {
            background: rgba(34, 197, 94, 0.15);
            border: 1px solid rgba(34, 197, 94, 0.4);
            color: #4ade80;
        }

        .status-error {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.4);
            color: #f87171;
        }

        /* Terminal box */
        .terminal-box {
            background: #090d16;
            border: 1px solid #1e293b;
            border-radius: 10px;
            padding: 16px;
            color: #38bdf8;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            line-height: 1.5;
            max-height: 380px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Section
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">⚛️ PropForge: AI Quantum Testing</div>
        <p class="hero-subtitle">
            Autonomous Property-Based Testing for Qiskit Circuits powered by Gemini & QuCheck
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Current directory paths
BASE_DIR = Path(__file__).resolve().parent
CIRCUIT_FILE = BASE_DIR / "my_circuit.py"
PROPFORGE_FILE = BASE_DIR / "propforge.py"
GENERATED_TEST_FILE = BASE_DIR / "generated_test.py"
PYTHON_EXE = BASE_DIR / "venv" / "Scripts" / "python.exe"
if not PYTHON_EXE.exists():
    PYTHON_EXE = sys.executable

# Two columns layout
col_left, col_right = st.columns([1, 1], gap="large")

# Left Column: Circuit Code Viewer
with col_left:
    st.markdown('<div class="section-header">📄 Quantum Circuit (my_circuit.py)</div>', unsafe_allow_html=True)
    
    if CIRCUIT_FILE.exists():
        with open(CIRCUIT_FILE, "r", encoding="utf-8") as f:
            circuit_code = f.read()
        st.code(circuit_code, language="python", line_numbers=True)
    else:
        st.warning("`my_circuit.py` not found in current directory.")

    # Circuit diagram preview button/expander
    with st.expander("🔍 Preview Circuit ASCII Diagram", expanded=True):
        if st.button("Render Circuit Diagram"):
            try:
                result = subprocess.run(
                    [str(PYTHON_EXE), str(CIRCUIT_FILE)],
                    cwd=str(BASE_DIR),
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                )
                if result.stdout:
                    st.code(result.stdout, language="text")
                if result.stderr:
                    st.caption("Runtime info:")
                    st.code(result.stderr, language="text")
            except Exception as e:
                st.error(f"Error rendering circuit: {e}")

# Right Column: Test Generation & Execution
with col_right:
    st.markdown('<div class="section-header">⚡ QuCheck Autonomous Verification</div>', unsafe_allow_html=True)
    st.write("Synthesize formal quantum property tests with Gemini 1.5/3.8 Flash, then run property-based statistical verification.")

    run_btn = st.button("🚀 Generate & Run Tests", type="primary", use_container_width=True)

    if run_btn:
        # Step 1: Run propforge.py to generate tests
        with st.status("🧠 Step 1: Synthesizing QuCheck Properties via Gemini...", expanded=True) as status_step:
            try:
                gen_proc = subprocess.run(
                    [str(PYTHON_EXE), str(PROPFORGE_FILE)],
                    cwd=str(BASE_DIR),
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                )
                if gen_proc.returncode != 0:
                    status_step.update(label="❌ Failed generating QuCheck properties", state="error", expanded=True)
                    st.error("Error during property generation:")
                    st.code(gen_proc.stderr or gen_proc.stdout)
                    st.stop()
                else:
                    status_step.update(label="✅ Tests Generated successfully!", state="complete", expanded=False)
                    st.toast("QuCheck test script generated!", icon="✨")
            except Exception as ex:
                status_step.update(label=f"❌ Error: {ex}", state="error")
                st.error(f"Execution failed: {ex}")
                st.stop()

        # Step 2: Run generated_test.py
        with st.status("🔬 Step 2: Executing QuCheck Statistical Test Suite...", expanded=True) as run_step:
            try:
                test_proc = subprocess.run(
                    [str(PYTHON_EXE), str(GENERATED_TEST_FILE)],
                    cwd=str(BASE_DIR),
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                )
                full_output = (test_proc.stdout or "") + ("\n" + test_proc.stderr if test_proc.stderr else "")
                
                # Check for unittest OK indicator
                is_ok = "OK" in (test_proc.stderr or "") or "OK" in (test_proc.stdout or "") or test_proc.returncode == 0

                if is_ok:
                    run_step.update(label="✅ All Property-Based Tests Passed [OK]", state="complete", expanded=False)
                    st.markdown(
                        """
                        <div class="status-badge status-success" style="margin-bottom: 12px;">
                            <span>✔</span> <span>All Quantum Properties Verified & Passed (OK)</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    run_step.update(label="❌ Test Assertions Failed", state="error", expanded=False)
                    st.markdown(
                        """
                        <div class="status-badge status-error" style="margin-bottom: 12px;">
                            <span>✖</span> <span>Some Quantum Property Assertions Failed</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                # Visual Terminal Output Box
                st.markdown("**🖥️ Captured Terminal Output:**")
                st.markdown(f'<div class="terminal-box">{full_output.strip()}</div>', unsafe_allow_html=True)

            except Exception as ex:
                run_step.update(label=f"❌ Execution error: {ex}", state="error")
                st.error(f"Failed to execute tests: {ex}")

    # Inspect Generated Test Code
    if GENERATED_TEST_FILE.exists():
        with st.expander("📜 View Current `generated_test.py`", expanded=False):
            with open(GENERATED_TEST_FILE, "r", encoding="utf-8") as f:
                test_code = f.read()
            st.code(test_code, language="python", line_numbers=True)
