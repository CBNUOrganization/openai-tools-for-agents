from openai import OpenAI
import gradio as gr

client = OpenAI()

def generate_response(prompt):
    response=client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    return response

demo = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(placeholder="Enter your prompt here...", label="Prompt", value=""),
    outputs=gr.Textbox(label="Response"),
    title="OpenAI GPT-4o-mini",
    description="Enter a prmpt to get a response from GPT-4o-mini"
)

if __name__=="__main__":
    demo.launch()