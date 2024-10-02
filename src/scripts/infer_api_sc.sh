set -ex
MODEL_NAME_OR_PATH="claude-3-5-sonnet-20240620"

DATA_NAME="amc"     # choose required dataset option:    amc/aime/odyssey/ob
SPLIT="test"
PROMPT_TYPE="sbsc"    # choose required prompt option:    cot/pal/tora/l2m_pal/sbsc
NUM_TEST_SAMPLE=-1

# Set the API key as an environment variable
export API_KEY="your_api_key_here"  # Make sure to replace with your actual API key/

python -um infer.inference_api_sc \
    --model_name_or_path $MODEL_NAME_OR_PATH \
    --output_dir ../src/outputs/ \
    --data_name $DATA_NAME \
    --split $SPLIT \
    --prompt_type $PROMPT_TYPE \
    --num_test_sample $NUM_TEST_SAMPLE \
    --seed 0 \
    --temperature 0.7 \
    --n_sampling 1 \
    --top_p 0.9 \
    --start 0\
    --end 8000\
    --num_chains 7\
