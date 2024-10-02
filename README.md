# Step-By-Step-Coding

We build on top of ToRA   
We recommend using Conda to manage your environment. We use vLLM (0.1.4) to accelerate inference.    
Run the following commands to setup your environment, clone this git repo and do the following :

```
cd Step-By-Step-Coding/src
conda create -n tora python=3.10
conda activate tora
pip install packaging==22.0
pip install torch==2.0.1 --index-url https://download.pytorch.org/whl/cu118 # CUDA 11.8 for example
pip install -r requirements.txt
```

Once done, you can run inference using the given script.   
Simply config the MODEL_NAME_OR_PATH, PROMPT_TYPE (to either cot/pal/tora/sbsc/l2m_pal as required) and DATA in src/scripts/infer_api.sh.   
In the file src/infer/inference_api.py, remember to change max_func_call value to 15 in case of sbsc.   
With prompt_type l2m_pal change max_func_call value to 2 for single generation of breakdown and solution.
Increasing the value of max_func_call gives more steps for resolving errors in l2m_pal prompt_type  

   
Finally, run the following command:
    
```
bash scripts/infer_api.sh
```
or for Self-Consistency, run the following command:
    
```
bash scripts/infer_api_sc.sh
```
