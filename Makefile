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
	  else echo PYTHON=/usr/bin/python >> ${CONF_FILE}; fi
	@@mkdir ${INSTALL_DIR}
	@@cp -r images template.html daemon.py webextract.py ${INSTALL_DIR}
	@@chmod +x ${INSTALL_DIR}/webextract.py ${INIT_SCRIPT}
	@@update-rc.d webextract defaults
	@@${INIT_SCRIPT} start
	@@echo "Installation complete."

uninstall:
	@@echo "Uninstalling WebExtract ..."
	@@if [ -f ${PID_FILE} ]; then ${INIT_SCRIPT} stop; fi
	@@update-rc.d -f webextract remove
	@@rm -rf ${INSTALL_DIR} ${PID_FILE} ${CONF_FILE} ${INIT_SCRIPT}
	@@echo "Done."