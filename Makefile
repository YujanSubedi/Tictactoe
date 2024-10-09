build:
	c++ ./minimaxbot.cpp -o bot.so -shared -fPIC

remove:
	rm ./bot.so

run:
	python ./Main.py
