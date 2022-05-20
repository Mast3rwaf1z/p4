#g++ -o c_impl/main $(pkg-config --cflags --libs opencv4) -g c_impl/main.cpp
g++ c_impl/test.cpp -I /usr/include/Halide/ -L /lib/libHalide.so -lHalide $(libpng-config --cflags --ldflags) -ljpeg -ldl -o c_impl/main
./c_impl/main