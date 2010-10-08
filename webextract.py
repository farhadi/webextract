#!/usr/bin/env python
##
# WebExtract v1.0
# A web-based utility to extract archive files for unix systems.
#
# @link        http://github.com/farhadi/webextract
# @copyright   Copyright 2010, Ali Farhadi (http://farhadi.ir/)
# @license     GNU General Public License 3.0 (http://www.gnu.org/licenses/gpl.html)
#

import time, re, subprocess, urllib, os, crypt, pwd, spwd, base64, sys
from daemon import Daemon
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class WebExtractHandler(BaseHTTPRequestHandler):

	def render(self, **data):
		data = dict({
			'status': 200,
			'title': '',
			'user': '',
			'content': '',
			'image': False
		}, **data)
		self.send_response(data['status'])
		if data['image']:
			self.send_header('Content-type', 'image/png')
			self.send_header('Expires', time.strftime(
				'%a, %d %b %Y %H:%M:%S GMT',
				time.gmtime(time.time() + 315360000)
			))
			self.send_header('Cache-Control', 'max-age=315360000')
			self.end_headers()
			f = open(os.path.dirname(sys.argv[0]) + os.sep + data['image'])
			self.wfile.write(f.read())
			f.close()
			return
		self.send_header('Content-type', 'text/html')
		if data['status'] == 401:
			self.send_header(
				'WWW-Authenticate',
				'Basic realm="Enter your FTP username and password:"'
			)
		self.end_headers()
		f = open(os.path.dirname(sys.argv[0]) + '/template.html')
		template = f.read()
		f.close()
		pattern = "|".join(['\{' + key + '\}' for key in data.keys()])
		template = re.sub(pattern, lambda m: str(data[m.group()[1:-1]]), template)
		self.wfile.write(template)

	def auth(self):
		try:
			auth = self.headers.getheader('Authorization')
			if auth.startswith('Basic '):
				auth = base64.b64decode(auth[6:])
				username, password = auth.split(':', 1)
				hashpass = spwd.getspnam(username)[1]
				if crypt.crypt(password, hashpass) == hashpass:
					return username
		except:
			pass

		self.render(
			status=401,
			title='Access Denied',
			content='Incorrect username or password. Please try again.'
		)
		return False

	def do_GET(self):
		try:
			if self.path == '/?logout':
				self.render(status=401, title='Logout', content='You are now logged out.')
				return

			if (
				re.match('/\?images/\w+\.png', self.path) and
				os.path.exists(os.path.dirname(sys.argv[0]) + os.sep + self.path[2:])
			):
				self.render(image=self.path[2:])
				return

			username = self.auth()
			if username:
				path = pwd.getpwnam(username)[5] + urllib.unquote_plus(self.path)
				data = {'user': 'Welcome <b>%s</b>! <a href="/?logout">Logout</a>' % username}

				if not os.path.exists(path):
					self.render(
						status=404,
						title='Not Found',
						content='File Not Found: %s' % urllib.unquote_plus(self.path),
						**data
					)
					return

				if os.path.isdir(path):
					if not path.endswith(os.sep):
						path += os.sep
						self.path += os.sep
					data['content'] = ''
					if self.path != os.sep:
						data['content'] += \
							'<a class="up" href="%s..">Up to higher level directory</a>' % self.path
					files = []
					dirs = []
					for file in os.listdir(path):
						try:
							mtime = time.strftime(
								'%Y/%m/%d %H:%M:%S',
								time.localtime(os.path.getmtime(path + file))
							)
						except:
							mtime = ''
						if os.path.isdir(path + file):
							dirs.append(
								('<tr><td class="name"><a class="dir" href="%s">%s</a></td>' +
								'<td></td><td class="mtime">%s</td></tr>') %
								(self.path + urllib.quote_plus(file), file, mtime)
							)
						else:
							try:
								size = os.path.getsize(path + file)
								for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
									if size < 1024.0:
										size = "%3.1f" % size
										if size.endswith('.0'):
											size = size[:-2]
										size += ' ' + x;
										break
									size /= 1024.0
							except:
								size = ''
							if file.endswith(('.zip', '.rar', '.tar', '.tar.gz', '.tgz')):
								extract = ' (<a href="%s">extract</a>)' % \
									(self.path + urllib.quote_plus(file))
								type = 'archive'
							else:
								extract = ''
								type = 'file'

							files.append(
								('<tr><td class="name"><span class="%s">%s</span>%s</td>' +
								'<td class="size">%s</td><td class="mtime">%s</td></tr>') %
								(type, file, extract, size, mtime)
							)

					files = [(x.lower(), x) for x in files]
					files.sort()
					files = [x[1] for x in files]
					dirs = [(x.lower(), x) for x in dirs]
					dirs.sort()
					dirs = [x[1] for x in dirs]
					data['content'] += \
						('<table><thead><tr><th class="name">Name</th><th class="size">Size</th>' + \
						'<th class="mtime">Last Modified</th></tr></thead><tbody>%s</tbody>' + \
						'</table>') % (''.join(dirs) + ''.join(files))
					self.render(title=urllib.unquote_plus(self.path), **data)
				elif path.endswith(('.zip', '.rar', '.tar', '.tar.gz', '.tgz')):
					if path.endswith(('.tar.gz', '.tgz')):
						cmd = ['sudo', '-u', username, 'tar', 'xvfz', path]
					elif path.endswith('.tar'):
						cmd = ['sudo', '-u', username, 'tar', 'xvf', path]
					elif path.endswith('.rar'):
						cmd = ['sudo', '-u', username, 'unrar', 'x', '-o+', path]
					elif path.endswith('.zip'):
						cmd = ['sudo', '-u', username, 'unzip', '-o', path]

					os.chdir(os.path.dirname(path))
					res = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					self.render(
						title='Extracting ' + urllib.unquote_plus(self.path),
						content=('<a class="up" href="%s">Back to parent directory</a>' +
							'<pre>%s</pre><b>Finished.</b>') %
							(os.path.dirname(self.path), res.stdout.read() + res.stderr.read()),
						**data
					)
				else:
					self.render(title='Error', content='File format not supported.', **data)

				return

		except:
			self.render(
				status=500,
				title='Internal Server Error',
				content='An internal error has occurred. Please contact your hosting provider.'
			)

class WebExtractDaemon(Daemon):
	def run(self):
		if len(sys.argv) == 3:
			port = sys.argv[2]
		else:
			port = 2121
		server = HTTPServer(('', int(port)), WebExtractHandler)
		server.serve_forever()

if __name__ == "__main__":
	daemon = WebExtractDaemon('webextract')
	if len(sys.argv) > 1:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'status' == sys.argv[1]:
			daemon.status()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop" % sys.argv[0]
		sys.exit(2)