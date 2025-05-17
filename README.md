# Qwen3 Ollama Demo

This repository contains a simple demonstration of using the `ollama` command
line tool to interact with the Qwen3 model. Two small Gradio apps are provided:

* **Reasoning Demo** – toggles between `/think` and `/no_think` modes.
* **Multilingual Demo** – translates prompts into different languages.

A standalone Python script `qwen3_demo.py` replicates the notebook logic and
includes basic error handling to ensure the `ollama` command is available.
Run it with:

```bash
python qwen3_demo.py
```

The notebook `qwen3_demo.ipynb` shows the same code in an interactive format.

