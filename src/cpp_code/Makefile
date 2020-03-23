all: check check-cppyy

lib:
	$(CC) -Wall -Wextra -pedantic -Wshadow -O3 -march=native -mtune=native unity_build.cpp -shared -fPIC -o libMocosHelper.so
check:
	$(CC) -fsyntax-only -Wall -Wextra -pedantic -Wshadow unity_build.cpp
check-cppyy:
	$(CC) -fsyntax-only -DMOCOS_CPPYY -Wall -Wextra -pedantic -Wshadow unity_build.cpp
