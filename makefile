install:
	python3 -m venv .venv; \
	source .venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements.txt; \

run: 
	source .venv/bin/activate; \
	streamlit run app.py; \