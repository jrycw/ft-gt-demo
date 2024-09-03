from multiprocessing import Process

import pytest
import uvicorn
from playwright.sync_api import expect, sync_playwright

from app import app  # FastHTML app is in app.py

test_schema = "http"
test_app_loc = "app:app"
test_host = "127.0.0.1"
test_port = 8741
test_url = f"{test_schema}://{test_host}:{test_port}/"


def run_server():
    uvicorn.run(test_app_loc, host=test_host, port=test_port, log_level="info")


@pytest.fixture(scope="module", autouse=True)
def start_server():
    process = Process(target=run_server, daemon=True)
    process.start()
    yield
    process.terminate()


def test_app():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(record_video_dir="videos/")
        page = context.new_page()
        page.goto(test_url)

        page.wait_for_timeout(3000)
        page.screenshot(path="screenshot.png")

        color1_value, color2_value = "#663399", "#ffa500"
        color_picker1, color_picker2 = page.locator("#color1"), page.locator("#color2")

        # test initial colors
        expect(color_picker1).to_have_value(color1_value)
        expect(color_picker2).to_have_value(color2_value)

        # change color1
        color_picker1.fill(color2_value)
        expect(color_picker1).to_have_value(color2_value)
        page.wait_for_timeout(3000)

        # change color2
        color_picker2.fill(color1_value)
        expect(color_picker2).to_have_value(color1_value)
        page.wait_for_timeout(3000)

        context.close()
        browser.close()
