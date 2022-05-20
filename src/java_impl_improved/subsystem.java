package java_impl_improved;

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
        String type = args.length > 1 ? args[1] : "sequential";
        Mat image = Imgcodecs.imread(filename);
        long detect_pre = System.currentTimeMillis();
        ArrayList<int[]> coordinates = new ArrayList<>();
        if(type.equalsIgnoreCase("sequential")){
            coordinates = detection_algorithm(image);
        }
        else if(type.equalsIgnoreCase("parallel")){
            coordinates = parallel_detection_algorithm(image);
        }
        long detect_post = System.currentTimeMillis();
        long cluster_pre = System.currentTimeMillis();
        ArrayList<cluster> result = clustering_algorithm(coordinates);
        long cluster_post = System.currentTimeMillis();
        
        int all_pixels = image.rows()*image.cols();
        int red_pixels = coordinates.size();
        int percentage = red_pixels * 100 / all_pixels;


        System.out.println("Analysing image:            " + filename);
        System.out.println("Running algorithm type:     " + type);
        System.out.println("Detection time:             " + (detect_post-detect_pre) + "ms");
        System.out.println("Number of pixels:           " + all_pixels);
        System.out.println("Number of red pixels:       " + red_pixels);
        System.out.println("Percentage of red pixels:   " + percentage);
        System.out.println("Clustering time:            " + (cluster_post-cluster_pre) + "ms");
        System.out.println("Number of fires:            " + result.size());
        System.out.print  ("Size of fires:              ");
        for(cluster C : result){
            System.out.print(C.size() + "px ");
        }
        System.out.println();
        System.out.print  ("Coordinates of fires:       ");
        for(cluster C : result){
            System.out.print("(" + C.get(0)[0] + ", " + C.get(0)[1] + ")");
        }
        System.out.println();

        
    }
    private static ArrayList<int[]> detection_algorithm(Mat image){
        ArrayList<int[]> result = new ArrayList<int[]>();
        for(int i = 0; i < image.cols(); i++){
            for(int j = 0; j < image.rows(); j++){
                if(image.get(j, i)[2] > 165 && image.get(j, i)[1] < 100 && image.get(j, i)[0] < 100){
                    result.add(new int[]{j, i});
                }
            }
        }
        return result;
    }
    private static ArrayList<int[]> parallel_row(Mat image, int index){
        ArrayList<int[]> result = new ArrayList<int[]>();
        for(int i = 0; i < image.rows(); i++){
            if(image.get(i, index)[2] > 165 && image.get(i, index)[1] < 100 && image.get(i, index)[0] < 100){
                result.add(new int[]{index, i});
            }
        }
        return result;
    }
    private static ArrayList<int[]> parallel_detection_algorithm(Mat image) throws InterruptedException, ExecutionException{
        ArrayList<int[]> result = new ArrayList<int[]>();
        ExecutorService executor = Executors.newFixedThreadPool(4);
        ArrayList<Future<ArrayList<int[]>>> processes = new ArrayList<>();
        for(int i = 0; i < image.cols(); i++){
            final int index = i;
            processes.add(executor.submit(() -> parallel_row(image, index)));
        }
        for(int i = 0; i < processes.size(); i++){
            result.addAll(processes.get(i).get());
        }
        executor.shutdown();
        return result;
    }
    private static void inner_clustering_algorithm(int[] c1, ArrayList<cluster> result){
        int size1 = result.size();
        for(int i = 0; i < size1; i++){
            int size2 = result.get(i).size();
            for(int j = 0; j < size2; j++){
                int[] c2 = result.get(i).get(j);
                // check if a non-zero pixel is nearby
                if(c2[0] == c1[0] - 1 || c2[1] == c1[1] - 1){
                    result.get(i).add(c1);
                    return;
                }
            }
        }
        // no non-zero pixels were nearby, append a new list
        result.add(new cluster(c1));
    }
    private static ArrayList<cluster> clustering_algorithm(ArrayList<int[]> coordinates){
        ArrayList<cluster> result = new ArrayList<cluster>();
        result.add(new cluster(coordinates.get(0)));
        coordinates.remove(0);
        for(int[] c1 : coordinates){
            inner_clustering_algorithm(c1, result);
        }
        return result; 
    }
}