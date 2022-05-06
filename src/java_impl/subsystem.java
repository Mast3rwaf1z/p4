package java_impl;

import java.util.ArrayList;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;

public class subsystem {
    public static void main(String[] args) {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
        String filename = args.length == 1 ? args[0] : "images/smallfire.jpg";
        System.out.println("Analysing image:            " + filename);
        Mat image =  Imgcodecs.imread(filename);
        System.out.print("Detecting fire...           ");
        long detect_pre = System.currentTimeMillis();
        fire_detection data = fire_detection_algorithm(image);
        long detect_post = System.currentTimeMillis();
        System.out.println(detect_post-detect_pre + "ms");
        System.out.println("Fire detected:              " + data.state);
        System.out.println("Number of pixels:           " + data.all_pixels);
        System.out.println("Number of red pixels:       " + data.red_pixels);
        System.out.println("Percentage of red pixels:   " + data.percentage);
        if(data.state){
            System.out.println("Potential fire detected");
            System.out.print("Identifying fires...        ");
            long ident_pre = System.currentTimeMillis();
            ArrayList<ArrayList<coordinate>> coords = fire_identification_algorithm(data.matrix);
            long ident_post = System.currentTimeMillis();
            System.out.println((ident_post-ident_pre) + "ms");

            System.out.println("Number of fires:            " + coords.size());
            System.out.print("Size of fires:              ");
            for(ArrayList<coordinate> fire : coords){
                System.out.print(fire.size() + "px");
                System.out.print(" ");
            }
            System.out.println();
            System.out.print("Coordinates of fires:       ");
            for(ArrayList<coordinate> fire : coords){
                System.out.print("(" + fire.get(0).x + ", " + fire.get(0).y + ")");
            }
            System.out.println();
        }

        else{
            System.out.println("No fire detected");
        }



    }
    public static fire_detection fire_detection_algorithm(Mat image){
        fire_detection data = new fire_detection();
        int[][] result = new int[image.rows()][image.cols()];
        for (int i = 0; i < image.rows(); i++) {
            for (int j = 0; j < image.cols(); j++) {
                result[i][j] = image.get(i, j)[2] > 165 && image.get(i, j)[1] < 100 && image.get(i, j)[0] < 100 ? 255 : 0;
            }
        }
        int red_detected = 0;
        for (int[] rows : result) {
            for (int element : rows) {
                data.all_pixels += 1;
                data.red_pixels += element != 0 ? 1 : 0;
                red_detected += element;
            }
        }
        data.percentage = data.red_pixels * 100 / data.all_pixels;

        if(red_detected > 0 && data.percentage < 1){
            data.state = true;
        }
        else{
            data.state = false;
        }
        data.matrix = result;
        return data;
    }

    public static ArrayList<ArrayList<coordinate>> fire_identification_algorithm(int[][] matrix){
        ArrayList<ArrayList<coordinate>> coords = new ArrayList<ArrayList<coordinate>>();
        for (int y = 0; y < matrix.length; y++) {
            for (int x = 0; x < matrix[y].length; x++) {
                if(matrix[y][x] != 0){
                    if(x == 0 && y == 0){
                        coords.add(coordinate.new_coordinate_list(x, y));
                        continue;
                    }
                    int upper = matrix[y-1][x];
                    int left = matrix[y][x-1];
                    int upperleft = matrix[y-1][x-1];
                    if(upper == 0 && left == 0 && upperleft == 0){
                        coords.add(coordinate.new_coordinate_list(x, y));
                    }
                    else if(upper != 0 && left != 0){
                        ArrayList<coordinate> upper_fire = get_fire(coords, x, y-1);
                        ArrayList<coordinate> left_fire = get_fire(coords, x-1, y);
                        if(left_fire == upper_fire){
                            upper_fire.add(new coordinate(x, y));
                        }
                        else{
                            upper_fire.addAll(left_fire);
                            coords.remove(left_fire);
                            upper_fire.add(new coordinate(x, y));
                        }
                    }
                    else if(upper != 0){
                        get_fire(coords, x, y-1).add(new coordinate(x, y));
                    }
                    else if(left != 0){
                        get_fire(coords, x-1, y).add(new coordinate(x, y));
                    }
                    else if(upperleft != 0){
                        get_fire(coords, x-1, y-1).add(new coordinate(x, y));
                    }
                }
            }
        }
        return coords;
    }
    private static ArrayList<coordinate> get_fire(ArrayList<ArrayList<coordinate>> coords, int x, int y) {
        for (ArrayList<coordinate> fire : coords) {
            for(coordinate coord : fire){
                if(coord.x == x && coord.y == y){
                    return fire;
                }
            }
            
        }
        return null;
    }

}