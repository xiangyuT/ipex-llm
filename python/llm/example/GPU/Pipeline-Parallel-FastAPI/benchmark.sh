export BATCH=$1
python benchmark.py --max_concurrent_requests $BATCH --prompt_length 1024 --max_new_tokens 512
cat $BATCH.log