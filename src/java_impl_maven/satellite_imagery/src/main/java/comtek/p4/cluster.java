package comtek.p4;

import java.util.ArrayList;

public class cluster extends ArrayList<int[]> {
    cluster(int[] element){
        this.add(element);
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
    
    public static ArrayList<cluster> clustering_algorithm(ArrayList<int[]> coordinates){
        ArrayList<cluster> result = new ArrayList<cluster>();
        result.add(new cluster(coordinates.get(0)));
        coordinates.remove(0);
        for(int[] c1 : coordinates){
            inner_clustering_algorithm(c1, result);
        }
        return result; 
    }
}
