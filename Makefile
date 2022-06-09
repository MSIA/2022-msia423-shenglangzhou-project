.PHONY: image_model image_app image_test all 

clean:
	rm -rf data/artifacts/*
	rm -rf models/*

image_model:
	docker build -f dockerfiles/Dockerfile -t final-project . 

image_app:
	docker build -f dockerfiles/Dockerfile.app -t final-project-app .

image_test:
	docker build -f dockerfiles/Dockerfile.test -t final-project-tests .

.PHONY: upload_file_to_s3 download_file_from_s3

upload_file_to_s3:
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e S3_BUCKET final-project run.py upload_file_to_s3

download_file_from_s3:
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e S3_BUCKET final-project run.py download_file_from_s3

.PHONY: create_db 


create_db:
	docker run -it -e SQLALCHEMY_DATABASE_URI final-project run.py create_db


.PHONY: raw cleaned featurized model ingest_data prediction metrics


data/artifacts/cleaned.csv: 
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e S3_BUCKET final-project run.py download_file_from_s3
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run.py run_model_pipeline --step clean --config=config/config.yaml --output=data/artifacts/cleaned.csv

cleaned: data/artifacts/cleaned.csv

data/artifacts/featurized.csv: data/artifacts/cleaned.csv
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run.py run_model_pipeline --step featurize --input=data/artifacts/cleaned.csv --config=config/config.yaml --output=data/artifacts/featurized.csv

featurized: data/artifacts/featurized.csv

ingest_data:
	docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e SQLALCHEMY_DATABASE_URI final-project run.py ingest --input=data/artifacts/ingest_data.csv

models/randomforest.joblib: data/artifacts/featurized.csv
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run.py run_model_pipeline --step model --input=data/artifacts/featurized.csv --config=config/config.yaml --output=models/randomforest.joblib
	
model: models/randomforest.joblib

data/artifacts/evaluation_result.csv: models/randomforest.joblib data/sample/test.csv
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run.py run_model_pipeline --step score --config=config/config.yaml --output=data/artifacts/evaluation_result.csv

prediction: data/artifacts/evaluation_result.csv

data/artifacts/metrics_result.csv: data/artifacts/evaluation_result.csv
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run.py run_model_pipeline --step evaluate  --config=config/config.yaml --output=data/artifacts/metrics_result.csv

metrics: data/artifacts/metrics_result.csv


.PHONY: unit_test


unit_test:
	docker run final-project-tests
	

.PHONY: app

app:
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ -e SQLALCHEMY_DATABASE_URI -p 5000:5000 final-project-app

all: cleaned featurized model prediction metrics
