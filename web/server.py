#!/usr/bin/env python3
"""
Simple HTTP server with CORS and webhook proxy for Survey Cleaner MVP
"""

import http.server
import socketserver
import urllib.request
import urllib.parse
import json
import os
from urllib.error import URLError

class ProxyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == '/webhook':
            self.proxy_to_n8n()
        else:
            super().do_POST()

    def proxy_to_n8n(self):
        """Proxy webhook requests to n8n to avoid CORS issues"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # Forward to n8n webhook
            n8n_url = 'http://localhost:5678/webhook-test/survey-cleaner'
            
            req = urllib.request.Request(
                n8n_url,
                data=post_data,
                headers=dict(self.headers)
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                response_data = response.read()
                
                self.send_response(response.status)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(response_data)
                
        except URLError as e:
            print(f"Error proxying to n8n: {e}")
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = json.dumps({
                'error': 'Failed to connect to n8n webhook',
                'details': str(e)
            }).encode()
            self.wfile.write(error_response)
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = json.dumps({
                'error': 'Internal server error',
                'details': str(e)
            }).encode()
            self.wfile.write(error_response)

def run_server(port=3000):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", port), ProxyHTTPRequestHandler) as httpd:
        print(f"Server running on http://localhost:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()