import uuid

from multiprocessing import Process
from flask import Flask, jsonify
from typing import Callable, Iterable, Dict


class MockitServer:
    def __init__(self, port: int = 5000):
        super().__init__()
        self.port = port
        self.app = Flask(__name__)
        self.url = f"http://localhost:{self.port}"
        self.process = Process(target=self.run)

    def add_callback_response(
        self, url: str, callback: Callable, methods: Iterable = ("GET",)
    ):
        callback.__name__ = str(
            uuid.uuid4().hex
        )  # change name of method to mitigate flask exception
        self.app.add_url_rule(rule=url, view_func=callback, methods=methods)

    def add_json_response(
        self, url: str, serializable: Dict, methods: Iterable = ("GET",)
    ):
        def callback():
            return jsonify(serializable)

        self.add_callback_response(url=url, callback=callback, methods=methods)

    def add_string_response(
        self, url: str, response: str, methods: Iterable = ("GET",)
    ):
        def callback():
            return response

        self.add_callback_response(url=url, callback=callback, methods=methods)

    def run(self):
        self.app.run(port=self.port)

    def start(self):
        self.process.start()

    def terminate(self):
        self.process.terminate()
