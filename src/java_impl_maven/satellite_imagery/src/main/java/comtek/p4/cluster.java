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

    public static ArrayList<cluster> old_clustering_algorithm(int[][] matrix){
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
