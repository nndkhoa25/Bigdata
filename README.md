# Reddit trend and sentiment analysis: Docker + MinIO

## Requirements
- Docker Desktop with Docker Compose enabled

## Configure MinIO credentials
Copy `.env.example` to `.env` and replace the password with a private value. The `.env` file is ignored by Git; never commit Kaggle credentials or personal API tokens.

## Start services
From this directory, run:

```powershell
docker compose up --build
```

- JupyterLab: http://localhost:8888
- MinIO Console: http://localhost:9001
- MinIO S3 API: http://localhost:9000

Use the username and password set in `.env` to sign in to the MinIO Console. Keep these services bound to localhost; do not expose them to a public network.

## Create a bucket
In the MinIO Console, sign in and create a bucket named `reddit-data`. Upload Kaggle CSV files into that bucket. MinIO stores data in the persistent Docker volume `minio_data`, so it remains available when containers stop and restart.

## Read a CSV from MinIO in a notebook
The notebook container connects to MinIO using the service hostname `minio` (not `localhost`):

```python
import os
import boto3
import pandas as pd

s3 = boto3.client(
    "s3",
    endpoint_url=os.environ["MINIO_ENDPOINT"],
    aws_access_key_id=os.environ["MINIO_ACCESS_KEY"],
    aws_secret_access_key=os.environ["MINIO_SECRET_KEY"],
    region_name="us-east-1",
)

obj = s3.get_object(Bucket=os.environ["MINIO_BUCKET"], Key="your_file.csv")
df = pd.read_csv(obj["Body"])
df.head()
```

Stop the services with `Ctrl+C`; use `docker compose down` to stop them in the background. Data in `minio_data` persists. `docker compose down -v` permanently removes that volume.


## Interactive dashboard

The Streamlit dashboard summarizes the sentiment and V2 topic outputs without loading the full post corpus. Put these CSVs in `data/processed/` (download them from `MyDrive/RedditProject/data/processed/`):

- `sentiment_monthly.csv`
- `sentiment_by_subreddit.csv`
- `topic_monthly_counts_v2.csv`
- `topic_subreddit_counts_v2.csv`

Start the dashboard with Docker Compose:

```powershell
docker compose up --build reddit-dashboard
```

Open http://localhost:8501. The dashboard offers month and subreddit filters, monthly volume/sentiment charts, and topic summaries. Missing months remain gaps in the time chart. Topic 0 is shown as a broad mixed group, and topic 8 as a repeated-link group; treat topic shares as exploratory.

## Project notebooks
- `notebooks/01_data_audit.ipynb`: download and profile Kaggle source data.
- `notebooks/02_etl.ipynb`: clean the Reddit posts and write Parquet.
- `notebooks/03_sentiment_trends.ipynb`: VADER sentiment and time/community trends.
- `notebooks/04_topic_model.ipynb`: TF-IDF + NMF topic exploration.
- `src/dashboard.py`: interactive Streamlit dashboard.

The Kaggle API token belongs in Google Colab Secrets under `KAGGLE_API_TOKEN`, not in this repository.

## Persistent Colab data
The Colab notebooks mount Google Drive and store raw/processed files under `MyDrive/RedditProject/data/`. Run `02_etl.ipynb` again after a runtime reset if its output Parquet is missing; outputs stored on Drive persist across Colab sessions.
