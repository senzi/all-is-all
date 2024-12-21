import http.server
import socketserver
import webbrowser
from pathlib import Path
import os
import sys
import logging
from urllib.parse import unquote

# 配置
PORT = 8000
HOST = "localhost"
DEFAULT_PAGE = "index.html"
DIRECTORY = Path(__file__).parent  # 服务器根目录

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # 设置默认目录
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def end_headers(self):
        # CORS和缓存控制
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'X-Requested-With, Content-Type',
            'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
        for key, value in headers.items():
            self.send_header(key, value)
        super().end_headers()

    def do_GET(self):
        try:
            # 处理路径
            path = unquote(self.path)
            if path == '/':
                self.path = f'/{DEFAULT_PAGE}'
            elif path.endswith('/'):
                self.path = f'{path}{DEFAULT_PAGE}'
            # 移除.html后缀的支持
            elif not os.path.exists(self.translate_path(self.path)) and \
                 os.path.exists(self.translate_path(f'{self.path}.html')):
                self.path = f'{self.path}.html'

            # 记录请求
            logger.info(f'Request: {self.client_address[0]} - {self.path}')
            
            return super().do_GET()
            
        except Exception as e:
            logger.error(f'Error handling request: {e}')
            self.send_error(500, f'Internal server error: {str(e)}')

    def log_message(self, format, *args):
        # 覆盖默认的日志方法，使用我们的logger
        logger.info(f'{self.client_address[0]} - {format%args}')

def start_server():
    try:
        # 检查端口是否可用
        with socketserver.TCPServer((HOST, PORT), None) as test_server:
            pass
    except OSError:
        logger.error(f'Port {PORT} is already in use')
        sys.exit(1)

    try:
        # 允许端口复用
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer((HOST, PORT), MyHTTPRequestHandler) as httpd:
            server_url = f'http://{HOST}:{PORT}/'
            logger.info(f'Server started at {server_url}')
            logger.info(f'Serving directory: {DIRECTORY}')
            logger.info('Press Ctrl+C to stop the server')

            # 自动打开浏览器
            try:
                webbrowser.open(server_url)
            except Exception as e:
                logger.error(f'Failed to open browser: {e}')

            # 运行服务器
            httpd.serve_forever()

    except KeyboardInterrupt:
        logger.info('\nServer stopped by user')
    except Exception as e:
        logger.error(f'Server error: {e}')
        sys.exit(1)

if __name__ == '__main__':
    start_server()