all: check check-cppyy

lib:
	$(CXX) -Wall -Wextra -pedantic -Wshadow -O3 -march=native -mtune=native unity_build.cpp -shared -fPIC -o libMocosHelper.so
check:
	$(CXX) -fsyntax-only -Wall -Wextra -pedantic -Wshadow unity_build.cpp
check-cppyy:
	$(CXX) -fsyntax-only -DMOCOS_CPPYY -Wall -Wextra -pedantic -Wshadow unity_build.cpp
