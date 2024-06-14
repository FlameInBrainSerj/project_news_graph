import os
import sys
from collections.abc import Generator
from pathlib import Path
from unittest import mock

import pytest
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).parent.parent / "src"))

with mock.patch.dict(
    os.environ,
    {"SELENIUM_HOST": "localhost", "REDIS_HOST": "localhost"},
):
    from src.main import app


@pytest.fixture(scope="session", name="client")
def client_fixture() -> Generator[TestClient, None, None]:
    client = TestClient(app)
    yield client


def test_ping(client: TestClient) -> None:
    response = client.get(
        url="/ping/",
    )
    assert response.status_code == 200
    assert "I am alive!" in response.text


def test_predict_by_text(client: TestClient) -> None:
    text_3_pred = "This is the test text for model"
    text_5_pred = "Отчет сбербанка за нынешний период"

    response_3_pred = client.post(
        url=f"/model/predict_by_text/?text={text_3_pred}",
    )
    data_3_pred = response_3_pred.json()
    assert response_3_pred.status_code == 200
    assert "Global_moex" in data_3_pred["0"]
    assert "Global_rvi" in data_3_pred["0"]
    assert "Global_rubusd" in data_3_pred["0"]

    response_5_pred = client.post(
        url=f"/model/predict_by_text/?text={text_5_pred}",
    )
    data_5_pred = response_5_pred.json()
    assert response_5_pred.status_code == 200
    assert "Global_moex" in data_5_pred["0"]
    assert "Global_rvi" in data_5_pred["0"]
    assert "Global_rubusd" in data_5_pred["0"]
    assert "Company" in data_5_pred["0"]
    assert "Industry" in data_5_pred["0"]


def test_predict_by_texts_batch(client: TestClient) -> None:
    path = "tests/data/test_texts.csv"
    with open(path, "rb") as file:
        response = client.post(
            url="/model/predict_by_texts_batch/",
            files={
                "file": (
                    os.path.basename(path),
                    file,
                    "text/csv",
                ),
            },
        )
        data = response.json()

        assert response.status_code == 200
        assert "Global_moex" in data["0"]
        assert "Global_rvi" in data["0"]
        assert "Global_rubusd" in data["0"]
        assert "Global_moex" in data["1"]
        assert "Global_rvi" in data["1"]
        assert "Global_rubusd" in data["1"]


def test_predict_by_link(client: TestClient) -> None:
    valid_link = "https://ria.ru/20240316/gazprom_eksport-1933514645.html"
    invalid_link = "https://darova.ru/znakomi"

    valid_response = client.post(
        url=f"/model/predict_by_link/?url={valid_link}",
    )
    valid_data = valid_response.json()
    assert valid_response.status_code == 200
    assert "Global_moex" in valid_data["0"]
    assert "Global_rvi" in valid_data["0"]
    assert "Global_rubusd" in valid_data["0"]

    invalid_response = client.post(
        url=f"/model/predict_by_link/?url={invalid_link}",
    )
    assert invalid_response.status_code == 403
    assert "Sorry, but some webpages were not parsed" in invalid_response.text


def test_predict_by_links_batch(client: TestClient) -> None:
    path = "tests/data/test_links.csv"
    with open(path, "rb") as file:
        response = client.post(
            url="/model/predict_by_links_batch/",
            files={
                "file": (
                    os.path.basename(path),
                    file,
                    "text/csv",
                ),
            },
        )
        data = response.json()

        assert response.status_code == 200
        assert "Global_moex" in data["0"]
        assert "Global_rvi" in data["0"]
        assert "Global_rubusd" in data["0"]
        assert "Global_moex" in data["1"]
        assert "Global_rvi" in data["1"]
        assert "Global_rubusd" in data["1"]
