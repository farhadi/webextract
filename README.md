WebExtract v1.0
===============

What is WebExtract?
-------------------
WebExtract is a web-based utility to extract archive files for unix systems.
After installing each of unix users can access WebExtract remotely using a web browser
and browse their own files and folders on the server and extract archive files remotely.

One of WebExtract usages is when you don't want to give shell access to your users but
you want your users to be able to extract their own archive files themselves.

Acctually I wrote it for our shared hosting services so that our customers can extract
their files themselves. Because we are using Parallel's Plesk Control Panel which lacks this feature.


Under which license WebExtract is released?
-------------------------------------------
GNU General Public License 3.0 (http://www.gnu.org/licenses/gpl.html)


Which linux distributions does WebExtract support?
--------------------------------------------------
Its supposed to work on all redhat and debian based distros.
However I only tested it on CentOS, Ubuntu and Debian.


What are installation requirements?
-----------------------------------
The only requirement is Python2.5 or higher.


How to install WebExtract?
--------------------------
1. Install Python2.5 or higher if it's not already installed:

		wget http://www.python.org/ftp/python/2.7/Python-2.7.tgz
		tar xvfz Python-2.7.tgz
		cd Python-2.7
		./configure
		make
		make install

2. Download latest WebExtract package from [here](http://github.com/downloads/farhadi/webextract/webextract-latest.tar.gz) :

		wget http://github.com/downloads/farhadi/webextract/webextract-latest.tar.gz

3. Unpack it and go to its folder:

		tar xvfz webextract-latest.tar.gz
		cd webextract-*

4. Install it as root:

        make install

5. Make sure port 2121 is open on your server's firewall.

6. Its ready. Go to http://yourserver:2121/ and enjoy it.


How to uninstall WebExtract?
----------------------------
1. Repeat first two steps of Installation.
2. Run the following command as root:

		make uninstall


Which archive formats does WebExtract support?
----------------------------------------------
For now .tar, .tar.gz, .tgz, .zip and .rar formats are supported.


Why when I try to extract a file I see the error "sorry, you must have a tty to run sudo"?
--------------------------------------------------------------------------------------------------
You need to comment out `#Default requiretty` using `visudo`.
If requiretty is set, sudo will only run when the user is logged in to a real tty
which causes WebExtract to not work properly.


How can I change default WebExtract port?
-----------------------------------------
You can change the port in `/etc/webextract.conf`.
And don't forget to restart WebExtract for the changes to take effect.


How can I stop/start WebExtract service?
----------------------------------------
Use `/etc/init.d/webextract stop` to stop the service.
Use `/etc/init.d/webextract start` to start the service.
Use `/etc/init.d/webextract restart` to restart the service.
And use `/etc/init.d/webextract status` to see the service status.


Where can I report bugs, suggestions and feature requests?
----------------------------------------------------------
Either you can send your reports using [WebExtract's issue tracker](http://github.com/farhadi/webextract/issues)
or contact me directly using email at <a.farhadi@gmail.com>.