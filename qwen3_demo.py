import subprocess
import shutil
import gradio as gr

# Look up the ollama command at import time. The value is cached but the helper
# will re-check if it's missing to allow users to install ollama after starting
# the program.
OLLAMA_CMD = shutil.which("ollama")


def _run_ollama(prompt: str) -> str:
    """Run the ollama command and return the response or an error message."""
    global OLLAMA_CMD

    # Re-check for the command each call in case it was installed after the
    # module was imported.
    cmd = OLLAMA_CMD or shutil.which("ollama")
    if not cmd:
        return "Error: ollama command not found. Please install ollama."

    # Cache the command path so subsequent calls don't need to search again.
    OLLAMA_CMD = cmd

    try:
        result = subprocess.run(
            [cmd, "run", "qwen3:8b"],
            input=prompt,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        return f"Error running ollama: {exc.stderr.strip()}"
    return result.stdout


def reasoning_qwen3(prompt: str, mode: str) -> str:
    prompt_with_mode = f"{prompt} /{mode}"
    return _run_ollama(prompt_with_mode)


def multilingual_qwen3(prompt: str, lang: str) -> str:
    if lang != "English":
        prompt = f"Translate to {lang}: {prompt}"
    return _run_ollama(prompt)


reasoning_ui = gr.Interface(
    fn=reasoning_qwen3,
    inputs=[
        gr.Textbox(label="Enter your prompt"),
        gr.Radio(["think", "no_think"], label="Reasoning Mode", value="think"),
    ],
    outputs="text",
    title="Qwen3 Reasoning Mode Demo",
    description="Switch between /think and /no_think to control response depth.",
)

multilingual_ui = gr.Interface(
    fn=multilingual_qwen3,
    inputs=[
        gr.Textbox(label="Enter your prompt"),
        gr.Dropdown([
            "English",
            "French",
            "Hindi",
            "Chinese",
        ], label="Target Language", value="English"),
    ],
    outputs="text",
    title="Qwen3 Multilingual Translator",
    description="Use Qwen3 locally to translate prompts to different languages.",
)

demo = gr.TabbedInterface(
    [reasoning_ui, multilingual_ui],
    tab_names=["Reasoning Mode", "Multilingual"],
)

if __name__ == "__main__":
    demo.launch(debug=True)
