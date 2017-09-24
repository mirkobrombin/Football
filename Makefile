all: dependecies install uninstall

dependecies:
	sudo apt install libgtk-3-dev
	sudo apt install libgranite-dev
	sudo apt install python3

install:
	sudo cp src/main.py /bin/com.github.mirkobrombin.football
	sudo cp data/com.github.mirkobrombin.football.desktop /usr/share/applications/
	sudo cp data/com.github.mirkobrombin.football.svg /usr/share/icons/hicolor/128x128/apps
	sudo cp data/com.github.mirkobrombin.football.xml /usr/share/metainfo

uninstall:
	sudo rm /bin/com.github.mirkobrombin.football
	sudo rm /usr/share/applications/com.github.mirkobrombin.football.desktop
	sudo rm /usr/share/icons/hicolor/128x128/apps/com.github.mirkobrombin.football.svg
	sudo rm /usr/share/metainfo/com.github.mirkobrombin.football.xml
