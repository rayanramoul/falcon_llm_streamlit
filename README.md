# falcon_llm_streamlit

You need to have setup this :
```
git clone https://github.com/cmp-nct/ggllm.cpp
cd ggllm.cpp
rm -rf build && mkdir build && cd build && cmake -DGGML_CUBLAS=1 .. && cmake --build . --config Release
```

## how to run GGLLM instructions :
```
bin/falcon_main -t 8 -ngl 100 -b 1 -m falcon7b-instruct.ggmlv3.q4_0.bin -p "What is a falcon?\n### Response:"
```