package comtek.p4;

import java.util.ArrayList;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

import org.opencv.core.Mat;

public class colorDetector {
    
    public static ArrayList<int[]> detection_algorithm(Mat image){
        ArrayList<int[]> result = new ArrayList<int[]>();
        for(int i = 0; i < image.cols(); i++){
            for(int j = 0; j < image.rows(); j++){
                if(image.get(j, i)[2] > 175 && image.get(j, i)[1] < 60 && image.get(j, i)[0] < 60){
                    result.add(new int[]{j, i});
                }
            }
        }
        return result;
    }
    private static ArrayList<int[]> parallel_row(Mat image, int index){
        ArrayList<int[]> result = new ArrayList<int[]>();
        for(int i = 0; i < image.rows(); i++){
            if(image.get(i, index)[2] > 175 && image.get(i, index)[1] < 60 && image.get(i, index)[0] < 60){
                result.add(new int[]{index, i});
            }
        }
        return result;
    }
    public static ArrayList<int[]> parallel_detection_algorithm(Mat image) throws InterruptedException, ExecutionException{
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
}
