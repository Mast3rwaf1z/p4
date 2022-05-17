#include <iostream>
#include <opencv4/opencv2/opencv.hpp>
#include <list>
#include <tuple>
using namespace std;

/*  Fire Clustering Algorithm   */
typedef tuple<int, int> coordinate;
typedef list<coordinate> cluster;

cluster create_cluster(int x, int y){
    cluster Cluster = cluster();
    Cluster.push_back(coordinate(x, y));
    return Cluster;
}

cluster get_cluster(list<cluster> Cluster_list, coordinate element){
    for(cluster Cluster : Cluster_list){
        for(coordinate Coordinate : Cluster){
            if(element == Coordinate){
                return Cluster;
            }
        }
    }
    cout << "ERROR: cluster is not part of list" << endl;
    exit(0);
    return Cluster_list.back();
}

list<cluster> fire_clustering_algorithm(int** Matrix, int N, int M){
    list<cluster> coords = list<cluster>();
    for(int y = 0; y < M; y++){
        for(int x = 0; x < N; x++){
            if(Matrix[y][x] != 0){
                int upper = Matrix[y-1][x];
                int left = Matrix[y][x-1];
                int upperleft = Matrix[y-1][x-1];
                if(upper == 0 && left == 0 && upperleft == 0){
                    coords.push_back(create_cluster(x, y));
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