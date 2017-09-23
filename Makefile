all: dependecies install uninstall

dependecies:
	apt install libgtk-3-dev
	apt install libgranite-dev
	apt install python3

install:
	cp src/main.py /bin/com.github.mirkobrombin.Football
	cp data/com.github.mirkobrombin.Football.desktop /usr/share/applications/
	cp data/com.github.mirkobrombin.Football.svg /usr/share/icons/hicolor/128x128/apps
	cp data/com.github.mirkobrombin.Football.xml /usr/share/metainfo

uninstall:
	rm /bin/com.github.mirkobrombin.Football
	rm /usr/share/applications/com.github.mirkobrombin.Football.desktop
	rm /usr/share/icons/hicolor/128x128/apps/com.github.mirkobrombin.Football.svg
	rm /usr/share/metainfo/com.github.mirkobrombin.Football.xml
