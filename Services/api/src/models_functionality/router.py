import json
from io import BytesIO

import pandas as pd
from fastapi import APIRouter, Query, Response, UploadFile
from models_functionality.inference import predict_texts_and_return_dict
from models_functionality.scrapers import parse_links

router = APIRouter(prefix="/model", tags=["Model"])


@router.post("/predict_by_link", description="Get prediction by link to the news")
async def predict_by_link(url: str = Query(min_length=1)) -> Response:
    """
    Get prediction by one link to the news.

    :param url: url of the news
    :type url: str

    :rtype: Response
    :return json: .json file with prediction to the news
    """
    # Read link passed
    links = pd.DataFrame({"Url": url}, index=[0])
    # Parse link and get text
    texts = parse_links(links)
    # Predict and transform to json
    response_json = json.dumps(predict_texts_and_return_dict(texts))

    return Response(content=response_json, media_type="application/json")


@router.post("/predict_by_links_batch", description="Get prediction by batch of links")
async def predict_by_links_batch(file: UploadFile) -> Response:
    """
    Get prediction by batch of links to the news.

    :param file: .csv file with links to the news
    :type file: UploadFile

    :rtype: Response
    :return json: .json file with predictions to the news
    """
    # Read .csv file with links
    links = pd.read_csv(BytesIO(file.file.read()))
    # Parse links and get texts
    texts = parse_links(links)
    # Predict and transform to json
    response_json = json.dumps(predict_texts_and_return_dict(texts))

    return Response(content=response_json, media_type="application/json")


@router.post("/predict_by_text", description="Get prediction by news text")
async def predict_by_text(text: str = Query(min_length=1)) -> Response:
    """
    Get prediction by one text of the news.

    :param text: text of the news
    :type text: str

    :rtype: Response
    :return json: .json file with prediction to the news
    """
    # Read text passed
    texts = pd.DataFrame({"Text": text}, index=[0])
    # Predict and transform to json
    response_json = json.dumps(predict_texts_and_return_dict(texts))

    return Response(content=response_json, media_type="application/json")


@router.post(
    "/predict_by_texts_batch",
    description="Get prediction by batch of texts; Input: .csv; Output: .json",
)
async def predict_by_texts_batch(file: UploadFile) -> Response:
    """
    Get prediction by batch of texts of the news.

    :param file: .csv file with texts of the news
    :type file: UploadFile

    :rtype: Response
    :return json: .json file with predictions to the news
    """
    # Read .csv file with texts
    texts = pd.read_csv(BytesIO(file.file.read()))
    # Predict and transform to json
    response_json = json.dumps(predict_texts_and_return_dict(texts))

    return Response(content=response_json, media_type="application/json")
