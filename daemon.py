#!/usr/bin/env python
##
# Daemon
# A generic daemon base class.
#
# @copyright   Copyright 2010, Ali Farhadi (http://farhadi.ir/)
# @license     GNU General Public License 3.0 (http://www.gnu.org/licenses/gpl.html)
#

import sys, os, time, atexit
from signal import SIGTERM 

class Daemon:
	"""
	A generic daemon class.
	
	Usage: subclass the Daemon class and override the run() method
	"""
	def __init__(self, name, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		self.name = name
		self.pidfile = '/var/run/' + name + '.pid'
	
	def daemonize(self):
		"""
		Deamonize class. UNIX double fork mechanism.
		"""
		try: 
			pid = os.fork() 
			if pid > 0:
				# exit first parent
				sys.exit(0) 
		except OSError, e: 
			sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
			sys.exit(1)
	
		# decouple from parent environment
		os.chdir("/") 
		os.setsid() 
		os.umask(0) 
	
		# do second fork
		try: 
			pid = os.fork() 
			if pid > 0:
				# exit from second parent
				sys.exit(0) 
		except OSError, e: 
			sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
			sys.exit(1) 
	
		# redirect standard file descriptors
		sys.stdout.flush()
		sys.stderr.flush()
		si = file(self.stdin, 'r')
		so = file(self.stdout, 'a+')
		se = file(self.stderr, 'a+', 0)
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())
	
		# write pidfile
		atexit.register(self.delpid)
		pid = str(os.getpid())
		file(self.pidfile,'w+').write("%s\n" % pid)
	
	def delpid(self):
		os.remove(self.pidfile)

	def start(self):
		"""
		Start the daemon
		"""
		# Check for a pidfile to see if the daemon already runs
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
	
		if pid:
			try:
				os.kill(pid, 0)
				running = True
			except:
				running = False

			if running:
				message = "%s (pid %s) is already running\n"
				sys.stderr.write(message % (self.name, pid))
				sys.exit(1)

		# Start the daemon
		self.daemonize()
		self.run()

	def stop(self):
		"""
		Stop the daemon
		"""
		# Get the pid from the pidfile
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
	
		if not pid:
			message =  "%s isn't already running\n"
			sys.stderr.write(message % self.name)
			sys.exit(1)

		# Try killing the daemon process	
		try:
			while 1:
				os.kill(pid, SIGTERM)
				time.sleep(0.1)
		except OSError, err:
			err = str(err)
			if err.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print str(err)
				sys.exit(1)
	def status(self):
		"""
		Show daemon status
		"""
		try:
			pf = file(self.pidfile,'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None

		if pid:
			try:
				os.kill(pid, 0)
				running = True
			except:
				running = False

			if running:
				message = "%s (pid %s) is already running"
				print message % (self.name, pid)
			else:
				message = "%s dead but pid file exists"
				print message % self.name
		else:
			print "%s is stopped" % self.name

	def run(self):
		"""
		You should override this method when you subclass Daemon.
		It will be called after the process has been daemonized by start().
		"""