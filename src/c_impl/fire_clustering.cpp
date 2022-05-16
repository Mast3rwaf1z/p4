#include <iostream>
#include <vector>
#include <tuple>
using namespace std;

/*  Fire Clustering Algorithm   */
typedef tuple<int, int> coordinate;
typedef vector<coordinate> cluster;
typedef vector<cluster> cluster_list;

cluster create_cluster(int x, int y){
    cluster Cluster = cluster();
    Cluster.push_back(coordinate(x, y));
    return Cluster;
}

cluster get_cluster(cluster_list Cluster_list, coordinate element){
    for(cluster Cluster : Cluster_list){
        for(coordinate Coordinate : Cluster){
            if(element == Coordinate){
                return Cluster;
            }
        }
    }
}

cluster_list fire_clustering_algorithm(int** matrix, int N, int M){
    cluster_list coords = cluster_list();
    for(int y = 0; y < M; y++){
        for(int x = 0; x < N; x++){
            if(matrix[y][x] != 0){
                int upper = matrix[y-1][x];
                int left = matrix[y][x-1];
                int upperleft = matrix[y-1][x-1];
                if(upper == 0 && left == 0 && upperleft == 0){
                    coords.push_back(create_cluster(x, y));
                    cout << "here" << endl;
                }
                else if(upper != 0 && left != 0){
                    cluster upper_cluster = get_cluster(coords, coordinate(x, y-1));
                    cluster left_cluster = get_cluster(coords, coordinate(x-1, y));
                    if(upper_cluster == left_cluster){
                        upper_cluster.push_back(coordinate(x, y));
                    }
                    else{
                        upper_cluster.insert(upper_cluster.end(), left_cluster.begin(), left_cluster.end());
                        coords.pop_back();
                        upper_cluster.push_back(coordinate(x, y));
                    }
                }
                else if(upper != 0){
                    get_cluster(coords, coordinate(x, y-1)).push_back(coordinate(x, y));
                }
                else if(left != 0){
                    get_cluster(coords, coordinate(x-1, y)).push_back(coordinate(x, y));
                }
                else if(upperleft != 0){
                    get_cluster(coords, coordinate(x-1, y-1)).push_back(coordinate(x, y));
                }
            }
        }
    }
    return coords;
}