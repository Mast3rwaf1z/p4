#include <iostream>
#include <opencv4/opencv2/opencv.hpp>
using namespace std;
using namespace cv;

class coordinate{
    public:
    int x;
    int y;
    coordinate(int x, int y){
        this->x = x;
        this->y = y;
    }

    bool operator== (const coordinate& c) const {
        if(x == c.x && y == c.y){
            return true;
        }
        return false;
    }
};

list<coordinate> new_coordinate_list(int x, int y){
    list<coordinate> l;
    l.push_back(coordinate(x, y));
    return l;
}

list<coordinate> get_fire(list<list<coordinate>> coords, int x, int y){
    for(list<coordinate> fire : coords){
        for(coordinate coordinate : fire){
            if(coordinate.x == x && coordinate.y == y){
                return fire;
            }
        }
    }
    cout << "FAILURE!" << endl;
    throw exception();
}

int** fire_detection_algorithm(Mat image){
    int** result = new int*[image.rows];
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

list<list<coordinate>> fire_identification_algorithm(int** matrix, int N, int M){
    list<list<coordinate>> coords;
    for(int y = 0; y < M; y++){
        for(int x = 0; x < N; x++){
            if(matrix[y][x] != 0){
                if(x == 0 && y == 0){
                    coords.push_back(new_coordinate_list(x, y));
                    continue;
                }
                int upper = matrix[y-1][x];
                int left = matrix[y][x-1];
                int upperleft = matrix[y-1][x-1];
                if(upper == 0 && left == 0 && upperleft == 0){
                    coords.push_back(new_coordinate_list(x, y)); //this line bad
                }
                else if(upper != 0 && left != 0){
                    list<coordinate> upper_fire = get_fire(coords, x, y-1);
                    list<coordinate> left_fire = get_fire(coords, x-1, y);
                    if(left_fire == upper_fire){
                        upper_fire.push_back(coordinate(x, y));
                    }
                    else{
                        upper_fire.insert(upper_fire.end(), left_fire.begin(), left_fire.end());
                        coords.remove(left_fire);
                        upper_fire.push_back(coordinate(x, y));
                    }
                }
                else if(upper != 0){
                    get_fire(coords, x, y-1).push_back(coordinate(x, y));
                }
                else if(left != 0){
                    get_fire(coords, x-1, y).push_back(coordinate(x, y));
                }
                else if(upperleft != 0){
                    get_fire(coords, x-1, y-1).push_back(coordinate(x, y));
                }
            }
        }
    }
    return coords;
}

int main(int argc, char* argv[]){
    String filename = argc > 1 ? argv[1] : "images/smallfire.jpg";
    cout << "Analysing image:           " << filename << endl;
    Mat image = imread(filename);
    cout << "Detecting fire...          ";
    time_t detect_pre = time(NULL);
    int** processed_image = fire_detection_algorithm(image);
    time_t detect_post = time(NULL);
    cout << detect_post-detect_pre << "ms" << endl;
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
        list<list<coordinate>> coords = fire_identification_algorithm(processed_image, image.cols, image.rows);
        time_t ident_post = time(NULL);
        cout << ident_post-ident_pre << "sec" << endl;
        cout << "Number of fires:           " << coords.size() << endl;
        cout << "Size of fires:             ";
        for(list<coordinate> fire : coords){
            cout << fire.size() << "px ";
        }
        cout << endl;
        cout << "Coordinates of fires:      ";
        for (list<coordinate> fire : coords){
            cout  << "(" << fire.front().x << ", " << fire.front().y << ")";
        }
        cout << endl;

    }
    else{
        cout << "No fire detected" << endl;
    }

    return 0;
}