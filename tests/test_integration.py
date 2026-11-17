import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

from benchmarks.scripts.benchmark import run_benchmark


class InferenceHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        payload = json.loads(self.rfile.read(length))

        assert self.path == "/v1/completions"

        response = json.dumps({
            "usage": {
                "prompt_tokens": 512,
                "completion_tokens": payload["max_tokens"]
            }
        }).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)


def test_http_integration():
    server = HTTPServer(("127.0.0.1", 0), InferenceHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    try:
        result = run_benchmark(
            f"http://127.0.0.1:{server.server_port}",
            "simulated-model",
            "Integration test",
            256, 2, 4
        )

        assert result["requests"] == 4
        assert result["total_output_tokens"] == 1024
        assert result["output_tokens_per_second"] > 0

    finally:
        server.shutdown()
        thread.join()
        server.server_close()
