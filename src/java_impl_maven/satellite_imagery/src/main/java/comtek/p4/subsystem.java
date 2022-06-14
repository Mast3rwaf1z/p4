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
        if(type.equalsIgnoreCase("sequential")){
            coordinates = colorDetector.detection_algorithm(image);
        }
        else if(type.equalsIgnoreCase("parallel")){
            coordinates = colorDetector.parallel_detection_algorithm(image);
        }
        long detect_post = System.currentTimeMillis();
        int all_pixels = image.rows()*image.cols();
        int red_pixels = coordinates.size();
        int percentage = red_pixels * 100 / all_pixels;
        System.out.println("Detection time:             " + (detect_post-detect_pre) + "ms");
        System.out.println("Number of pixels:           " + all_pixels);
        System.out.println("Number of red pixels:       " + red_pixels);
        System.out.println("Percentage of red pixels:   " + percentage);
        if(coordinates.size() == 0){
            System.out.println("No fire was Detected");
            System.exit(0);
        }
        long cluster_pre = System.currentTimeMillis();
        ArrayList<cluster> result = cluster.clustering_algorithm(coordinates);
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