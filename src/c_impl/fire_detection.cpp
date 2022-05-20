#include <iostream>
#include <Halide/Halide.h>
using namespace Halide::Tools;
using namespace std;

typedef Halide::Buffer<uint8_t> buffer;
typedef tuple<int, int> coordinate;
typedef vector<coordinate> cluster;

/*  Fire Detection Algorithm for RGB    */
vector<coordinate> fire_detection_algorithm(buffer image){
    vector<coordinate> result;
    int matrix[image.width()][image.height()][3];
    int image_size =(image.width()*image.height())*3;
    int channel_size = image_size/image.channels();
    int red_start = 0;
    for(int i = 0; i < image.height(); i++){
        for(int j = 0; j < image.width(); j++){
            matrix[i][j][2] = (int) *(image.begin()+((i*image.width())+j));
            matrix[i][j][1] = (int) *(image.begin()+((i*image.width())+j)+channel_size);
            matrix[i][j][0] = (int) *(image.begin()+((i*image.width())+j)+(channel_size*2));
        }
    }
    
    for(int i = 0; i < image.height(); i++){
        for(int j = 0; j < image.width(); j++){
            matrix[i][j][2] > 165 && matrix[i][j][1] < 100 && matrix[i][j][0] < 100 ? result.push_back(coordinate(i, j)) : void();
        }
    }
    return result;
}