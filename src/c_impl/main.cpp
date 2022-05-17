#include <opencv4/opencv2/opencv.hpp>
#include <iostream>
#include "fire_detection.cpp"
#include "fire_clustering.cpp"
#include <vector>
#include <tuple>
using namespace cv;
using namespace std;

int main(int argc, char* argv[]){
    String filename = argc > 1 ? argv[1] : "images/smallfire.jpg";
    cout << "Analysing image:           " << filename << endl;
    Mat image = imread(filename);
    cout << "Detecting fire...          ";
    time_t detect_pre = time(NULL);
    matrix processed_image = fire_detection_algorithm(image);
    time_t detect_post = time(NULL);
    cout << detect_post-detect_pre << "sec" << endl;
    int all_pixels = 0;
    int red_pixels = 0;
    for(int i = 0; i < image.cols; i++){
        for(int j = 0; j < image.rows; j++){
            all_pixels += 1;
            red_pixels += processed_image[i][j] != 0 ? 1 : 0;
        }
    }
    float percentage = red_pixels * 100 / all_pixels;
    cout << "Number of pixels:          " << all_pixels << endl;
    cout << "Number of red pixels:      " << red_pixels << endl;
    cout << "Percentage of red pixels:  " << percentage << endl;
    if(red_pixels > 0 && percentage < 1){
        cout << "Potential fire detected" << endl;
        cout << "Identifying fire...        ";
        time_t ident_pre = time(NULL);
        list<cluster> coords = fire_clustering_algorithm(processed_image, image.cols, image.rows);
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