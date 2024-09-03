import pytest
from fasthtml.common import FastHTML, Title
from starlette.testclient import TestClient

from ft_gt import gt2fasthtml


@pytest.fixture
def simple_app(gtbl):
    @gt2fasthtml(id="gt")
    def get_tbl():
        return gtbl

    app = FastHTML()

    @app.get("/")
    def homepage():
        div_comp = get_tbl()
        return Title("FastHTML-GT testing app"), div_comp

    yield app


@pytest.fixture
def client(simple_app):
    yield TestClient(simple_app)


def test_simple_app(client):
    resp = client.get("/")
    resp_text = resp.text

    assert "FastHTML-GT testing app" in resp_text
    assert '<div id="gt">' in resp_text
