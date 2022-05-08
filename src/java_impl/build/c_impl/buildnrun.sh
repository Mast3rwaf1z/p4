g++ -o c_impl/subsystem c_impl/subsystem.cpp $(pkg-config --libs opencv4)
./c_impl/subsystem