#include <iostream>
#include <Halide/Halide.h>
#include "Halide/halide_image_io.h"
#include "fire_detection.cpp"
#include "fire_clustering.cpp"
using namespace std;
using namespace Halide::Tools;

typedef Halide::Buffer<uint8_t> buffer;

int main(){
    string filename = "images/smallfire.jpg";
    cout << "Analysing image:           " << filename << endl;
    buffer img = load_image(filename);

    cout << "Detecting fire...          ";
    float detect_pre = time(NULL);
    vector<coordinate> coordinates = fire_detection_algorithm(img);
    float detect_post = time(NULL);
    cout << detect_post-detect_pre << " sec" << endl;

    int all_pixels = 0;
    for(int i = 0; i < img.height(); i++){
        for(int j = 0; j < img.width(); j++){
            all_pixels += 1;
        }
    }
    int red_pixels = coordinates.size();
    float percentage = red_pixels * 100 / all_pixels;
    cout << "Number of pixels:          " << all_pixels << endl;
    cout << "Number of red pixels:      " << red_pixels << endl;
    cout << "Percentage of red pixels:  " << percentage << endl;
    if(red_pixels > 0 && percentage < 1){
        cout << "Potential fire detected" << endl;
        cout << "Identifying fire...        ";
        time_t ident_pre = time(NULL);
        vector<cluster> coords = fire_clustering_algorithm(coordinates);
        time_t ident_post = time(NULL);
        cout << ident_post-ident_pre << "sec" << endl;
        cout << "Number of fires:           " << coords.size() << endl;
        cout << "Size of fires:             ";
        for(cluster Cluster : coords){
            cout << Cluster.size() << "px ";
        }
        cout << endl;
        cout << "Coordinates of fires:      ";
        for (cluster Cluster : coords){
            cout  << "(" << get<0>(Cluster.front()) << ", " << get<1>(Cluster.front()) << ")";
        }
        cout << endl;

    }
    else{
        cout << "No fire detected" << endl;
    }

    return 0;

}