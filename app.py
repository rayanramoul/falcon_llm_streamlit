#!/usr/bin/python

import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

# import subprocess
import os


message_history = []

st.set_page_config(page_title="Falcon LLM")
potential_models = ['falcon7b-instruct.ggmlv3.q4_0.bin']

def generate_response(prompt):
    print(f"\n\n\nNEW PROMPT {prompt}\n\n\n")
    args = ("ggllm.cpp/build/bin/falcon_main", "-t", "8", "-ngl", "100", "-b", "1", "-m", "/home/rayanramoul/models/falcon7b-instruct.ggmlv3.q4_0.bin", "-p",f'"{prompt}"')
    # popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    # popen.wait()
    # output = popen.stdout.read()
    cmd = ' '.join(args)
    output = os.popen(cmd).read()
    print(f"\n\n\nOUTPUT {output}\n\n\n")
    return str(output)

agent_tone = st.selectbox('Agent Tone', ['Friendly', 'Neutral', 'Hostile', 'Introvert', 'Extrovert'])
first_model = st.selectbox()
prompt = st.text_input('Prompt', value='Girafatron is obsessed with giraffes, the most glorious animal on the face of this Earth. Giraftron believes all other animals are irrelevant when compared to the glorious majesty of the giraffe.\nDaniel: Hello, Girafatron!\nGirafatron:')
if st.button('Generate'):
    result = generate_response(prompt)
    st.write(result)


st.write('Made with ❤️ by Rayan Samy Ramoul')