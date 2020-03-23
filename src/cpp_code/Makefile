all:
	$(CC) -fsyntax-only -Wall -Wextra -pedantic -Wshadow unity_build.cpp
lib:
	$(CC) -Wall -Wextra -pedantic -Wshadow -O3 -march=native -mtune=native unity_build.cpp -shared -fPIC -o libMocosHelper.so
