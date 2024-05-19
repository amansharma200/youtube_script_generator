import streamlit as st
import pandas as pd
from groq import Groq
import os

# Load the dataset
df = pd.read_csv('data.csv')

# Extract examples from the dataset
examples = df.head(2).to_dict(orient='records')

# Create a prompt template with options for video format and topic
prompt_template = """
Generate a {video_format} YouTube script on the topic: {topic} based on the following format:
Title: {title}
Introduction: {introduction}
Content: {content}
Conclusion: {conclusion}

Examples:
{examples}
"""

def generate_prompt(video_format, topic):
    example_texts = "\n\n".join([
        f"Title: {ex['Hook']}\nIntroduction: {ex['Build Up']}\nContent: {ex['Body']}\nConclusion: {ex['CTA']}"
        for ex in examples
    ])
    return prompt_template.format(
        video_format=video_format,
        topic=topic,
        title="Example Title",
        introduction="Example Introduction",
        content="Example Content",
        conclusion="Example Conclusion",
        examples=example_texts
    )

# Initialize Groq client
client = Groq(api_key="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")

def generate_script(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

# Streamlit app
st.title("YouTube Script Generator")

video_format = st.selectbox("Choose the video format", ["short format", "long format"])
topic = st.text_input("Enter the topic of the script")

if st.button("Generate Script", type="primary"):
    if topic:
        final_prompt = generate_prompt(video_format, topic)
        script = generate_script(final_prompt)
        st.subheader("Generated Script:")
        st.write(script)
    else:
        st.error("Please enter a topic.")
