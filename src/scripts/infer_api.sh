set -ex
MODEL_NAME_OR_PATH="claude-3-5-sonnet-20240620"
DATA_NAME="aime"     # choose required dataset option:    amc/aime/odyssey/olympiadbench
SPLIT="test"
PROMPT_TYPE="l2m_pal"    # choose required prompt option:    cot/pal/tora/sbsc/l2m_pal
NUM_TEST_SAMPLE=-1

# Set the API key as an environment variable
export API_KEY="your_api_key_here"  # Make sure to replace with your actual API key

python -um infer.inference_api \
    --model_name_or_path $MODEL_NAME_OR_PATH \
    --output_dir ../src/outputs/ \
    --data_name $DATA_NAME \
    --split $SPLIT \
    --prompt_type $PROMPT_TYPE \
    --num_test_sample $NUM_TEST_SAMPLE \
    --seed 0 \
    --temperature 0 \
    --n_sampling 1 \
    --top_p 1 \
    --start 0\
    --end 8000\

