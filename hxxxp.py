#coding=utf-8
#
import http.server
import socketserver

PORT = 8080

class ServerHandler(http.server.BaseHTTPRequestHandler):
	#def __init__(self):
	#	print("newline")

	def do_GET(self):
		body = None
		content = "nihao,xiaomaotongxue"
		body = content.encode('UTF-8', 'replace')

		message = "aaaaaaaaaaa\r\n"
		self.send_response(200)
		self.end_headers()
		self.wfile.write(body)

server = socketserver.TCPServer(("", PORT), ServerHandler)
server.serve_forever()