package java_impl;

import java.util.ArrayList;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;

public class subsystem {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
        String filename = args.length > 0 ? args[0] : "images/smallfire.jpg";
        String type = args.length == 2 ? args[1] : "parallel";
        System.out.println("Analysing image:            " + filename);
        System.out.println("Execution type:             " + type);
        Mat image =  Imgcodecs.imread(filename);
        System.out.print("Detecting fire...           ");
        long detect_pre = System.currentTimeMillis();
        int[][] result = new int[image.rows()][image.cols()];
        if(type.equalsIgnoreCase("parallel")){
            result = parallel_fire_detection_algorithm(image);
        }
        else if(type.equalsIgnoreCase("sequential")){
            result = fire_detection_algorithm(image);
        }
        long detect_post = System.currentTimeMillis();
        System.out.println(detect_post-detect_pre + "ms");
        int red_detected = 0;
        int all_pixels = 0;
        int red_pixels = 0;
        for(int[] row : result){
            for(int element : row){
                red_pixels += element != 0 ? 1 : 0;
                red_detected += element;
            }
            all_pixels += row.length;
        }
        int percentage = red_pixels * 100 / all_pixels;
        
        System.out.println("Number of pixels:           " + all_pixels);
        System.out.println("Number of red pixels:       " + red_pixels);
        System.out.println("Percentage of red pixels:   " + percentage);
        if(red_detected > 0 && percentage < 1){
            System.out.println("Potential fire detected");
            System.out.print("Identifying fires...        ");
            long ident_pre = System.currentTimeMillis();
            ArrayList<cluster> coords = fire_identification_algorithm(result);
            long ident_post = System.currentTimeMillis();
            System.out.println((ident_post-ident_pre) + "ms");

            System.out.println("Number of fires:            " + coords.size());
            if(args.length > 2 && args[2].equalsIgnoreCase("-v")){

                System.out.print("Size of fires:              ");
                for(cluster Cluster : coords){
                    System.out.print(Cluster.size() + "px");
                    System.out.print(" ");
                }
                System.out.println();
                System.out.print("Coordinates of fires:       ");
                for(cluster Cluster : coords){
                    System.out.print("(" + Cluster.get(0)[0] + ", " + Cluster.get(0)[1] + ")");
                }
                System.out.println();
            }
        }

        else{
            System.out.println("No fire detected");
        }
    }
    private static int[][] fire_detection_algorithm(Mat image){
        int[][] result = new int[image.rows()][image.cols()];
        for (int i = 0; i < image.rows(); i++) {
            for (int j = 0; j < image.cols(); j++) {
                result[i][j] = image.get(i, j)[2] > 175 && image.get(i, j)[1] < 60 && image.get(i, j)[0] < 60 ? 255 : 0;
            }
        }
        return result;
    }
    private static int[] parallel_row(Mat image, int index){ 
        int[] row = new int[image.cols()];
        for(int i = 0; i < image.cols(); i++){
            row[i] = image.get(index, i)[2] > 175 && image.get(index, i)[1] < 60 && image.get(index, i)[0] < 60 ? 255: 0;
        }
        return row;
    }
    private static int[][] parallel_fire_detection_algorithm(Mat image) throws InterruptedException, ExecutionException{
        int[][] result = new int[image.rows()][image.cols()];
        ExecutorService executor = Executors.newFixedThreadPool(4);
        ArrayList<Future<int[]>> processes = new ArrayList<Future<int[]>>();
        for(int i = 0; i < image.rows(); i++){
            final int index = i;
            processes.add(executor.submit(() -> parallel_row(image, index)));
        }
        for(int i = 0; i < processes.size(); i++){
            result[i] = processes.get(i).get();
        }
        executor.shutdown();
        return result;
    }
    private static ArrayList<cluster> fire_identification_algorithm(int[][] matrix){
        ArrayList<cluster> coords = new ArrayList<cluster>();
        for (int y = 0; y < matrix.length; y++) {
            for (int x = 0; x < matrix[y].length; x++) {
                if(matrix[y][x] != 0){
                    if(x == 0 || y == 0){
                        coords.add(new cluster(new int[]{x, y}));
                        continue;
                    }
                    int upper = matrix[y-1][x];
                    int left = matrix[y][x-1];
                    int upperleft = matrix[y-1][x-1];
                    if(upper == 0 && left == 0 && upperleft == 0){
                        coords.add(new cluster(new int[]{x, y}));
                    }
                    else if(upper != 0 && left != 0){
                        ArrayList<int[]> upper_cluster = get_cluster(coords, x, y-1);
                        ArrayList<int[]> left_cluster = get_cluster(coords, x-1, y);
                        if(left_cluster == upper_cluster){
                            upper_cluster.add(new int[]{x, y});
                        }
                        else{
                            upper_cluster.addAll(left_cluster);
                            coords.remove(left_cluster);
                            upper_cluster.add(new int[]{x, y});
                        }
                    }
                    else if(upper != 0){
                        get_cluster(coords, x, y-1).add(new int[]{x, y});
                    }
                    else if(left != 0){
                        get_cluster(coords, x-1, y).add(new int[]{x, y});
                    }
                    else if(upperleft != 0){
                        get_cluster(coords, x-1, y-1).add(new int[]{x, y});
                    }
                }
            }
        }
        return coords;
    }
    private static cluster get_cluster(ArrayList<cluster> coords, int x, int y) {
        int[] Element = {x, y};
        for (cluster Cluster : coords) {
            for(int[] element : Cluster){
                if(element[0] == Element[0] && element[1] == Element[1]){
                    return Cluster;
                }
            }
            
        }
        return null;
    }
}