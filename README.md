export HF_TOKEN=
export OPENAI_API_KEY=

# RGB data
python rag_test.py --data data/rgb_nobel.json
python lag_test.py --data data/rgb_nobel.json

# CoSQA+ data (works directly)
python lag_test.py --data CoSQAPlus_verified_public.json

# Construct openclaw data
export OPENAI_API_KEY=
python label_openclaw_data.py --data data/openclaw_29106.json --workers 5 --batch-size 100
python rag_test.py --data data/openclaw_29106.json