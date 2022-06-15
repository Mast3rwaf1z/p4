package comtek.p4;

import java.util.ArrayList;

public class Cluster extends ArrayList<int[]> {
    Cluster(int[] element){
        this.add(element);
    }
    
    public static ArrayList<Cluster> clustering_algorithm(ArrayList<int[]> coordinates){
        ArrayList<Cluster> result = new ArrayList<Cluster>();
        result.add(new Cluster(coordinates.get(0)));
        coordinates.remove(0);
        boolean clustered = false;
        for(int[] cluster1 : coordinates){
            clustered = false;
            for(Cluster cluster : result){
                for(int[] cluster2 : cluster){
                    // check if a non-zero pixel is nearby
                    if(cluster2[0] == cluster1[0] - 1 || cluster2[1] == cluster1[1] - 1){
                        cluster.add(cluster1);
                        clustered = true;
                        break;
                    }
                }
                if(clustered){
                    break;
                }
            }
            if(!clustered){
                // no non-zero pixels were nearby, append a new list
                result.add(new Cluster(cluster1));
            }
        }
        return result; 
    }

    public static ArrayList<Cluster> old_clustering_algorithm(int[][] matrix){
        ArrayList<Cluster> coords = new ArrayList<Cluster>();
        for (int y = 0; y < matrix.length; y++) {
            for (int x = 0; x < matrix[y].length; x++) {
                if(matrix[y][x] != 0){
                    if(x == 0 || y == 0){
                        coords.add(new Cluster(new int[]{x, y}));
                        continue;
                    }
                    int upper = matrix[y-1][x];
                    int left = matrix[y][x-1];
                    int upperleft = matrix[y-1][x-1];
                    if(upper == 0 && left == 0 && upperleft == 0){
                        coords.add(new Cluster(new int[]{x, y}));
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
    private static Cluster get_cluster(ArrayList<Cluster> coords, int x, int y) {
        int[] Element = {x, y};
        for (Cluster cluster : coords) {
            for(int[] element : cluster){
                if(element[0] == Element[0] && element[1] == Element[1]){
                    return cluster;
                }
            }
            
        }
        return null;
    }
}
