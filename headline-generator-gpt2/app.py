import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import gradio as gr

# Load the model and tokenizer
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Generation history
history = []

# Generation function with logging
def generate_and_log(prompt, max_length=100, temperature=0.7, top_k=50):
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=max_length,
            do_sample=True,
            top_k=top_k,
            temperature=temperature,
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id
        )
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    result = generated_text.strip()
    
    # Log this output
    history.append(f"📝 **Prompt**: `{prompt}`\n🎯 **Output**: {result}")
    return result, "\n\n---\n\n".join(reversed(history[-10:]))  # Limit to last 10 logs

# Clear fields and history
def clear_fields():
    history.clear()
    return "", ""

# UI components
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 📰 Headline Generator (GPT-2)\nEnter a prompt and get a creative headline.")
    
    with gr.Row():
        preset = gr.Dropdown(
            label="Preset Prompts",
            choices=[
                "AI cannot beat humans in",
                "The future of space travel is",
                "India's biggest tech achievement is",
                "Breaking news about climate change",
                "The secret behind productivity is"
            ],
            value=None,
            interactive=True
        )

        prompt_input = gr.Textbox(
            label="Or type your own prompt",
            placeholder="e.g., AI cannot beat humans in...",
            lines=1
        )


    with gr.Row():
        generate_btn = gr.Button("🔮 Generate")
        clear_btn = gr.Button("🧹 Clear")

    with gr.Row():
        output = gr.Textbox(label="Generated Headline", lines=2)
        log_output = gr.Markdown(label="📜 Generation Log")

    # Button click events
    preset.change(fn=fill_prompt, inputs=preset, outputs=prompt_input)
    generate_btn.click(fn=generate_and_log, inputs=prompt_input, outputs=[output, log_output])
    prompt_input.submit(fn=generate_and_log, inputs=prompt_input, outputs=[output, log_output])  # On Enter key
    clear_btn.click(fn=clear_fields, outputs=[prompt_input, log_output])

# Launch the app
demo.launch()
