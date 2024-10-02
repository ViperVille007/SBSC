set -ex

python -m eval.evaluate \
    --data_name "math" \
    --prompt_type "tora" \
    --file_path "" \ #provide output jsonl path
    --execute
