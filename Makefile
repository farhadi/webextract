INSTALL_DIR = /usr/share/webextract
PID_FILE = /var/run/webextract.pid
CONF_FILE = /etc/webextract.conf
INIT_SCRIPT = /etc/init.d/webextract

install:
	@@echo "Installing WebExtract ..."
	@@cp webextract /etc/init.d/webextract
	@@cp webextract.conf ${CONF_FILE}
	@@if [ -f /usr/local/bin/python ]; then \
		echo PYTHON=/usr/local/bin/python >> ${CONF_FILE}; \
	  else echo PYTHON=`which python --skip-alias` >> ${CONF_FILE}; fi
	@@mkdir ${INSTALL_DIR}
	@@cp -r images template.html daemon.py webextract.py ${INSTALL_DIR}
	@@chmod +x ${INSTALL_DIR}/webextract.py ${INIT_SCRIPT}
	@@if which update-rc.d &> /dev/null; then \
		update-rc.d webextract defaults 90 10; \
	  else chkconfig --add webextract; fi
	@@${INIT_SCRIPT} start
	@@echo "Installation complete."

uninstall:
	@@echo "Uninstalling WebExtract ..."
	@@if [ -f ${PID_FILE} ]; then ${INIT_SCRIPT} stop; fi
	@@if which update-rc.d &> /dev/null; then \
		update-rc.d -f webextract remove; \
	  else chkconfig --del webextract; fi
	@@rm -rf ${INSTALL_DIR} ${PID_FILE} ${CONF_FILE} ${INIT_SCRIPT}
	@@echo "Done."