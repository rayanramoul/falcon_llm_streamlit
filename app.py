#!/usr/bin/python

import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

import openai
# import subprocess
import os

import torch
from transformers import LlamaTokenizer, LlamaForCausalLM

message_history = []

st.set_page_config(page_title="Falcon LLM")

llama_model_path = 'openlm-research/open_llama_3b'
potential_models = ['falcon7b-instruct.ggmlv3.q4_0.bin']
llama_tokenizer = LlamaTokenizer.from_pretrained(llama_model_path,
                                                 device_map={'': 0})
llama_model = LlamaForCausalLM.from_pretrained(
    llama_model_path, torch_dtype=torch.float16, device_map={'': 0},
)

def run_comparison_chatgpt(prompt1:str, prompt2:str, agent_tone:str):
    chatgpt_prompt = f"Between the two responses, which one is more {agent_tone.lower()}? \n\n Response 1: {prompt1} \n\n Response 2: {prompt2}\n Justify your answer."
    response= openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": f"{chatgpt_prompt}"},
    ]
    )
    response_message = response["choices"][0]["message"]
    print("Response from GPT:", response_message)
    return response_message



def generate_response_llama(prompt, agent_tone):
    print(f"\n\n\nLLAMA NEW PROMPT {prompt}\n\n\n")
    prompt = prompt + f"\n Answer this question with a {agent_tone} tone."
    input_ids = llama_tokenizer(prompt, return_tensors="pt").input_ids
    generation_output = llama_model.generate(
        input_ids=input_ids, max_new_tokens=32
    )
    output = llama_tokenizer.decode(generation_output[0])
    print(f"\n\n\nLLAMA OUTPUT {output}\n\n\n")
    return output

def generate_response_falcon(prompt, agent_tone):
    print(f"\n\n\nNEW PROMPT {prompt}\n\n\n")
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
second_model = st.selectbox('Second Model', [llama_model_path])
prompt = st.text_input('Prompt', value='Girafatron is obsessed with giraffes, the most glorious animal on the face of this Earth. Giraftron believes all other animals are irrelevant when compared to the glorious majesty of the giraffe.\nDaniel: Hello, Girafatron!\nGirafatron:')
if st.button('Generate'):
    result_falcon = generate_response_falcon(prompt, agent_tone)
    result_llama = generate_response_llama(prompt, agent_tone)
    col1, col2 = st.columns(2)
    with col1:
        st.header(f"Response from {first_model}")
        st.write(result_falcon)
    with col2:
        st.header(f"Response from {second_model}")
        st.write(result_llama)

    output = run_comparison_chatgpt(result_falcon, result_llama, agent_tone)
    st.header("Comparison by ChatGPT")
    st.write(output)
    
st.write('Made with ❤️ by Rayan Samy Ramoul')