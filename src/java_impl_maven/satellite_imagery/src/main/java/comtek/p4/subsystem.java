package comtek.p4;

import java.util.ArrayList;
import java.util.concurrent.ExecutionException;

import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;

public class subsystem {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        nu.pattern.OpenCV.loadLocally();
        //System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
        String filename = args.length > 0 ? args[0] : "images/smallfire.jpg";
        String type = args.length > 1 ? args[1] : "sequential";
        System.out.println("Analysing image:            " + filename);
        System.out.println("Running algorithm type:     " + type);
        Mat image = Imgcodecs.imread(filename);
        long detect_pre = System.currentTimeMillis();
        ArrayList<int[]> coordinates = new ArrayList<>();
        int[][] old_coordinates = new int[image.rows()][image.cols()];

        switch(type.toLowerCase()){
            case "sequential":
                coordinates = colorDetector.detection_algorithm(image);
                break;
            case "parallel":
                coordinates = colorDetector.parallel_detection_algorithm(image);
                break;
            case "old_sequential":
                old_coordinates = colorDetector.old_detection_algorithm(image);
                break;
            case "old_parallel":
                old_coordinates = colorDetector.parallel_old_detection_algorithm(image);
                break;
        }

        long detect_post = System.currentTimeMillis();
        int all_pixels = image.rows()*image.cols();
        int red_pixels = coordinates.size();
        int percentage = red_pixels * 100 / all_pixels;
        System.out.println("Detection time:             " + (detect_post-detect_pre) + "ms");
        System.out.println("Number of pixels:           " + all_pixels);
        System.out.println("Number of red pixels:       " + red_pixels);
        System.out.println("Percentage of red pixels:   " + percentage);
        if(coordinates.size() == 0 && !(type.equalsIgnoreCase("old_sequential") || type.equalsIgnoreCase("old_parallel"))){
            System.out.println("No fire was Detected");
            System.exit(0);
        }
        ArrayList<cluster> result = new ArrayList<cluster>();
        long cluster_pre = System.currentTimeMillis();
        if(type.equalsIgnoreCase("parallel") || type.equalsIgnoreCase("sequential")){
            result = cluster.clustering_algorithm(coordinates);
        }
        else if(type.equalsIgnoreCase("old_parallel") || type.equalsIgnoreCase("old_sequential")){
            result = cluster.old_clustering_algorithm(old_coordinates);
        }
        long cluster_post = System.currentTimeMillis();
        


        System.out.println("Clustering time:            " + (cluster_post-cluster_pre) + "ms");
        System.out.println("Number of fires:            " + result.size());
        if(args.length > 2 && args[2].equalsIgnoreCase("-v")){

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
            
        
    }
}