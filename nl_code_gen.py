#!/usr/bin/env python3

import sys
import re
import os
from openai import OpenAI

###########################################
# 1) Create an OpenAI client with your API key
#    (Read from an environment variable, not hard-coded)
###########################################
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")  # Use environment variable here
)

###########################################
# 2) NLP to Python function with a more specific prompt
###########################################
def nl_to_python(nl_command: str) -> str:
    """
    Convert natural language instructions into Python code using GPT-3.5 or GPT-4.
    Adds extra prompt logic to ensure a function name if user wants a function.
    """

    # Basic detection: if user says "make a function" but no name is found, we nudge GPT
    # to be extra explicit about function names.
    want_function = bool(re.search(r"(make a function|create a function)", nl_command, re.IGNORECASE))
    has_name = bool(re.search(r"\bcalled\b|\bnamed\b|\bfunction\s+\w+", nl_command, re.IGNORECASE))

    extra_instructions = ""
    if want_function and not has_name:
        extra_instructions = (
            "The user asked to make a function but did not provide a name. "
            "Politely enforce that a function name must exist. If none is provided, choose a short, descriptive name.\n"
        )

    prompt = f"""
You are a Python code generation assistant.
Only produce valid Python code. Do not include explanations.

{extra_instructions}

Instruction:
{nl_command}

Answer:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful Python coding assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        code = response.choices[0].message.content
        return code.strip()
    except Exception as e:
        return f"# Error calling the OpenAI API: {e}"

###########################################
# 3) Main interactive loop
###########################################
def main():
    current_mode = "python"  # "python" or "nlp"

    print("Welcome to Kids' Python IDE with Natural Language Mode!")
    print("Type `:mode nlp` or `:mode python` to switch modes.")
    print("Type `:quit` or Ctrl+C to exit.\n")

    while True:
        try:
            user_input = input(f"[{current_mode.upper()} mode] >>> ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting IDE. Goodbye!")
            sys.exit(0)

        # Handle special commands
        if user_input.strip().lower() == ":quit":
            print("Exiting IDE. Goodbye!")
            sys.exit(0)
        elif user_input.strip().lower() == ":mode nlp":
            current_mode = "nlp"
            print("Switched to NLP mode.\n")
            continue
        elif user_input.strip().lower() == ":mode python":
            current_mode = "python"
            print("Switched to Python mode.\n")
            continue

        # Generate code
        if current_mode == "python":
            python_code = user_input
        else:
            python_code = nl_to_python(user_input)

        # Print code
        print(f"\nGenerated code (mode: {current_mode}):")
        print(python_code)
        print()

        # Optionally auto-run the generated code:
        """
        try:
            exec(python_code, {})
        except Exception as e:
            print("Error executing code:", e)
        """

if __name__ == "__main__":
    main()