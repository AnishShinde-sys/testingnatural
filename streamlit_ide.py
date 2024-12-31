import streamlit as st
import io
import contextlib

# For the GPT-based code generation:
from openai import OpenAI

########################################
# 1) Setup your OpenAI client
########################################
client = OpenAI(
    api_key="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"
)

def nl_to_python(nl_command: str) -> str:
    """
    Convert natural language instructions into Python code using the openai>=1.0.0 approach.
    """
    prompt = f"""
You are a Python code generation assistant.
Only produce valid Python code. Do not include explanations.

Instruction:
{nl_command}

Answer:
"""
    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful Python coding assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        code = resp.choices[0].message.content
        return code.strip()
    except Exception as e:
        return f"# Error calling OpenAI API: {e}"

def run_python_code(code: str) -> str:
    """
    Capture stdout from exec-ed code and return it as a string.
    """
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        try:
            exec(code, {})
        except Exception as e:
            print(f"Error: {e}")
    return buffer.getvalue()

########################################
# 2) Streamlit app
########################################
def main():
    st.set_page_config(page_title="VS Code–like NLP IDE", layout="wide")

    # Inject your custom CSS:
    st.markdown("""
    <style>
    /* --- Begin your VSCode-inspired CSS --- */
    :root {
        --bg-primary: #1e1e1e;
        --bg-secondary: #252526;
        --bg-tertiary: #2d2d2d;
        --text-primary: #d4d4d4;
        --text-secondary: #858585;
        --accent: #007acc;
        --border: #404040;
        --success: #28a745;
        --error: #ff5555;
        --warning: #f1fa8c;
    }

    body {
        background: var(--bg-primary);
        color: var(--text-primary);
    }

    .top-nav {
        height: 48px;
        background: var(--bg-secondary);
        border-bottom: 1px solid var(--border);
        display: flex;
        align-items: center;
        padding: 0 16px;
        justify-content: space-between;
        flex-shrink: 0;
    }

    /* Basic text color overrides for Streamlit's default elements */
    .stTextInput>div>div>input, .stTextArea textarea, .stMarkdown, .stCodeBlock, .stText, .stButton>button, .stSelectbox>div>div>span {
        color: var(--text-primary) !important;
        background-color: var(--bg-secondary) !important;
        border-color: var(--border) !important;
    }
    .stCodeBlock code {
        color: var(--text-primary);
        background: var(--bg-tertiary);
    }

    /* Buttons */
    .stButton>button {
        background: var(--accent) !important;
        color: white !important;
        border: none !important;
        padding: 6px 16px !important;
    }
    .stButton>button:hover {
        opacity: 0.9 !important;
    }
    /* Hide default boxes */
    .block-container, .main, .reportview-container {
        background: var(--bg-primary) !important;
    }

    /* Scrollbars */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--bg-tertiary);
        border-radius: 6px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-secondary);
    }
    /* --- End your custom CSS --- */
    </style>
    """, unsafe_allow_html=True)

    # Top nav simulation (We'll do a horizontal container)
    st.markdown(
        """
        <div class="top-nav">
            <div class="nav-left">
                <span style="color:var(--accent); font-weight:bold;">Natural Py IDE</span>
            </div>
            <div class="nav-right">
                <span style="color:var(--text-secondary);">VSCode-like UI</span>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

    # Mode toggling (NLP or Python)
    st.write("### Mode Switch")
    mode = st.radio(
        "Select Input Mode:",
        options=["NLP", "Python"],
        horizontal=True
    )

    # Code input area
    st.write("### Editor Area")
    instructions = st.text_area(
        "Type your code or natural language instructions here:",
        height=200,
    )

    # "Run" button
    if st.button("Run"):
        # If in NLP mode, convert line by line
        lines = instructions.split("\n")
        final_lines = []
        for line in lines:
            text = line.strip()
            if text:
                if mode == "NLP":
                    py_code = nl_to_python(text)
                    final_lines.append(py_code)
                else:
                    final_lines.append(line)
            else:
                final_lines.append("")  # preserve blank lines

        final_script = "\n".join(final_lines)

        # Show user the final code
        st.write("#### Generated Python Code")
        st.code(final_script, language="python")

        # Attempt to run it
        st.write("#### Output")
        output = run_python_code(final_script)
        if output.strip():
            st.text(output)
        else:
            st.text("(No output)")
    else:
        st.info("Click 'Run' to execute your input.")

if __name__ == "__main__":
    main()