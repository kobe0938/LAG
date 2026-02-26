export HF_TOKEN=
export OPENAI_API_KEY=

# RGB data
python rag_test.py --data data/rgb_nobel.json
python lag_test.py --data data/rgb_nobel.json

# CoSQA+ data (works directly)
python lag_test.py --data CoSQAPlus_verified_public.json
