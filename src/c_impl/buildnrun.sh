g++ -o c_impl/main $(pkg-config --libs opencv4) -g c_impl/main.cpp
./c_impl/main