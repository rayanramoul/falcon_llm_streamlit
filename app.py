#!/usr/bin/python
import os

import streamlit as st
import openai

st.set_page_config(page_title="Falcon LLM")
message_history = []

potential_models = ['falcon7b-instruct.ggmlv3.q4_0.bin']

def run_comparison_chatgpt(original_prompt:str, prompt1:str, prompt2:str, agent_tone:str):
    """
    Runs the comparison between the two responses using ChatGPT
    """
    chatgpt_prompt = f"Between the two responses (for the prompt {original_prompt}), which one is more {agent_tone.lower()}? \n\n Response 1: {prompt1} \n\n Response 2: {prompt2}\n Justify your answer."
    response= openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": f"{chatgpt_prompt}"},
    ]
    )
    response_message = response["choices"][0]["message"]
    print("Response from GPT:", response_message)
    return response_message['content']



def generate_response_llama(prompt:str, agent_tone:str):
    """
    Generates a response from the LLaMa LLM
    """
    print(f"\n\n\nNEW PROMPT LLAMA {prompt}\n\n\n")
    prompt = prompt + f"\n Answer this question with a {agent_tone} tone."
    args = ("llama.cpp/main", "-t", "8", "-ngl", "100", "-b", "1", "-m", "/home/rayanramoul/models/llama_ggml/LLaMa-7B-GGML/llama-7b.ggmlv3.q4_0.bin ", "-p",f'"{prompt}"')
    # popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    # popen.wait()
    # output = popen.stdout.read()
    cmd = ' '.join(args)
    output = os.popen(cmd).read()
    print(f"\n\n\nOUTPUT {output}\n\n\n")
    output = output.replace(prompt, '')
    output = output.replace('<|endoftext|>', '')
    return str(output)
    
def generate_response_falcon(prompt:str, agent_tone:str):
    """
    Generates a response from the Falcon LLM
    """
    print(f"\n\n\nNEW PROMPT FALCON {prompt}\n\n\n")
    prompt = prompt + f"\n Answer this question with a {agent_tone} tone."
    args = ("ggllm.cpp/build/bin/falcon_main", "-t", "8", "-ngl", "100", "-b", "1", "-m", "/home/rayanramoul/models/falcon7b-instruct.ggmlv3.q4_0.bin", "-p",f'"{prompt}"')
    # popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    # popen.wait()
    # output = popen.stdout.read()
    cmd = ' '.join(args)
    output = os.popen(cmd).read()
    print(f"\n\n\nOUTPUT {output}\n\n\n")
    output = output.replace(prompt, '')
    output = output.replace('<|endoftext|>', '')
    return str(output)



st.title("Role Interpretation Comparison between LLMs")
agent_tone = st.selectbox('Agent Tone', ['Friendly', 'Hostile', 'Introvert', 'Extrovert'])
first_model = st.selectbox('First Model', potential_models)
second_model = st.selectbox('Second Model', ["LLaMa-7B-GGML/llama-7b.ggmlv3.q4_0.bin"])
prompt = st.text_input('Prompt', value='Girafatron is obsessed with giraffes, the most glorious animal on the face of this Earth. Giraftron believes all other animals are irrelevant when compared to the glorious majesty of the giraffe.\nDaniel: Hello, Girafatron!\nGirafatron:')
if st.button('Generate'):
    result_falcon = generate_response_falcon(prompt, agent_tone)
    result_llama = generate_response_llama(prompt, agent_tone)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Response from {first_model}")
        st.write(result_falcon)
    with col2:
        st.subheader(f"Response from {second_model}")
        st.write(result_llama)

    output = run_comparison_chatgpt(prompt, result_falcon, result_llama, agent_tone)
    st.header("Comparison by ChatGPT")
    st.write(output)
    
st.write('Made with ❤️ by Rayan Samy Ramoul')