import base64
import datetime
import http.server
import joblib
import json
import numpy
import os
import sentence_transformers
import socketserver
import sys
import threading
import time
import torch


class Handler(http.server.BaseHTTPRequestHandler):
    def __init__(self, embedder, classifier, device, *args):
        self.embedder = embedder
        self.classifier = classifier
        self.device = device
        super(http.server.BaseHTTPRequestHandler, self).__init__(*args)


    def classify(self, text):
        try:
            embeddings = self.embedder.encode(["passage: {}".format(text)], normalize_embeddings=True)
            prediction = self.classifier.predict(embeddings)
            return { "result": True if prediction[0] else False }
        except:
            return None

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        print(length)
        content = self.rfile.read(length).decode('utf-8')
        print(content)
        post_data = json.loads(content)
        result = self.classify(post_data['text'])
        if result is None:
            self.send_response(500)
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))


def watchdog(httpd):
    start_day = int(time.time()) // (60 * 60 * 24)
    while True:
        time.sleep(1)
        ts = int(time.time())
        day = ts // (60 * 60 * 24)
        hour = ts // (60 * 60) % 24
        if day != start_day and hour == 7:
            httpd.shutdown()
            return


def main():
    device = torch.device('cpu')
    embedder = sentence_transformers.SentenceTransformer('intfloat/multilingual-e5-large')
    classifier = joblib.load("svm_model.joblib")
    print('Running server')
    with socketserver.TCPServer(("", 8013), lambda *args: Handler(embedder, classifier, device, *args)) as httpd:
        watchdog_thread = threading.Thread(target = lambda: watchdog(httpd))
        watchdog_thread.start()
        httpd.serve_forever()


if __name__ == "__main__":
    main()

