#include <opencv4/opencv2/opencv.hpp>

typedef int** matrix;

/*  Fire Detection Algorithm for RGB    */
matrix fire_detection_algorithm(cv::Mat image){
    matrix result = new int*[image.rows];
    for(int i = 0; i < image.cols; i++){
        result[i] = new int[image.cols];
    }

    for(int i = 0; i < image.rows; i++){
        for(int j = 0; j < image.cols; j++){
            //cout << i << " " << j << endl;
            result[i][j] = image.ptr(i, j)[2] > 165 && image.ptr(i, j)[1] < 100 && image.ptr(i, j)[0] < 100 ? 255 : 0;
        }
    }
    return result;
}