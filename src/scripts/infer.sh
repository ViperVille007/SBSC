set -ex

MODEL_NAME_OR_PATH="llm-agents/tora-70b-v1.0"

# DATA_LIST = ['math', 'gsm8k', 'gsm-hard', 'svamp', 'tabmwp', 'asdiv', 'mawps']

DATA_NAME="aime"

SPLIT="test"
PROMPT_TYPE="cot"
NUM_TEST_SAMPLE=-1


CUDA_VISIBLE_DEVICES=1 TOKENIZERS_PARALLELISM=false \
python -um infer.inference \
--model_name_or_path ${MODEL_NAME_OR_PATH} \
--data_name ${DATA_NAME} \
--split ${SPLIT} \
--prompt_type ${PROMPT_TYPE} \
--use_train_prompt_format \
--num_test_sample ${NUM_TEST_SAMPLE} \
--seed 0 \
--temperature 0 \
--n_sampling 1 \
--top_p 1 \
--start 0 \
--end 40 \
