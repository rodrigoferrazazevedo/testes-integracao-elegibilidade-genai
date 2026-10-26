import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


class ServicoFalso:
    """Stub HTTP local do serviço de elegibilidade; cada teste programa a resposta."""

    def __init__(self):
        self.status, self.corpo, self.atraso, self.recebidas = 200, b"{}", 0.0, []

    def responder(self, status=200, corpo=None, bruto=None, atraso=0.0):
        self.status, self.atraso = status, atraso
        self.corpo = bruto if bruto is not None else json.dumps(corpo or {}).encode()


@pytest.fixture
def servico():
    estado = ServicoFalso()

    class Manipulador(BaseHTTPRequestHandler):
        def do_POST(self):
            tamanho = int(self.headers.get("Content-Length", 0))
            estado.recebidas.append({"caminho": self.path, "headers": dict(self.headers), "corpo": json.loads(self.rfile.read(tamanho))})
            time.sleep(estado.atraso)
            self.send_response(estado.status)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(estado.corpo)

        def log_message(self, *args):
            pass

    servidor = ThreadingHTTPServer(("127.0.0.1", 0), Manipulador)
    threading.Thread(target=servidor.serve_forever, kwargs={"poll_interval": 0.02}, daemon=True).start()
    estado.url = f"http://127.0.0.1:{servidor.server_address[1]}"
    yield estado
    servidor.shutdown()
    servidor.server_close()
