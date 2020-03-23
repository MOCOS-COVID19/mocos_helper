all:
	$(CC) -fsyntax-only -Wall -Wextra -pedantic -Wshadow *.cpp
lib:
	$(CC) -Wall -Wextra -pedantic -Wshadow -O3 -march=native -mtune=native *.cpp -shared -fPIC -o libMocosHelper.so
