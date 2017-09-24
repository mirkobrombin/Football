all: dependecies install uninstall

dependecies:
	pip install requests

install:
	cp src/main.py /bin/com.github.mirkobrombin.football
	cp data/com.github.mirkobrombin.football.desktop /usr/share/applications/
	cp data/com.github.mirkobrombin.football.svg /usr/share/icons/hicolor/128x128/apps
	cp data/com.github.mirkobrombin.football.xml /usr/share/metainfo

uninstall:
	rm /bin/com.github.mirkobrombin.football
	rm /usr/share/applications/com.github.mirkobrombin.football.desktop
	rm /usr/share/icons/hicolor/128x128/apps/com.github.mirkobrombin.football.svg
	rm /usr/share/metainfo/com.github.mirkobrombin.football.xml
