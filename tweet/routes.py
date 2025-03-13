import kagglehub
from fastapi import APIRouter
from kagglehub import KaggleDatasetAdapter

tweet_router = APIRouter()


@tweet_router.post("/ingest")
def ingest():
    df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        "thoughtvector/customer-support-on-twitter",
        "sample.csv",
        # Provide any additional arguments like
        # sql_query or pandas_kwargs. See the
        # documenation for more information:
        # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
    )

    return {"message": "Ingest successful"}
