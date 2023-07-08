FROM python:3.9-slim-buster

ARG OPENAI_API_KEY


RUN apt-get update
RUN apt install -y git git-lfs cmake build-essential libssl-dev libffi-dev python3-dev wget


WORKDIR /opt
RUN git clone https://github.com/cmp-nct/ggllm.cpp 
RUN wget https://github.com/ggerganov/llama.cpp

WORKDIR /opt/ggllm.cpp
RUN rm -rf build && mkdir build && cd build && cmake -DGGML_CUBLAS=1 .. && cmake --build . --config Release

WORKDIR /opt/llama.cpp
RUN make


WORKDIR /opt/models
RUN git lfs install
RUN git clone https://huggingface.co/TheBloke/LLaMa-7B-GGML
RUN git clone https://huggingface.co/TheBloke/falcon-7b-instruct-GGML

WORKDIR /opt

# SET ENVIRONMENT VARIABLES
ENV OPENAI_API_KEY=$OPENAI_API_KEY

COPY requirements.txt /requirements.txt
COPY . /opt/app

WORKDIR /opt/app

RUN pip install -r requirements.txt

EXPOSE 8501
CMD python -m streamlit run app.py