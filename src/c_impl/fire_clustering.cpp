#include <iostream>
#include <vector>
#include <tuple>
using namespace std;

/*  Fire Clustering Algorithm   */
typedef tuple<int, int> coordinate;
typedef vector<coordinate> cluster;

cluster new_cluster(coordinate c){
    cluster Cluster;
    Cluster.push_back(c);
    return Cluster;
}

/*vector<cluster> fire_clustering_algorithm(vector<coordinate> coordinates){
    //expect an ordered vector of coordinates, element 0 has the lowest x value for pixels with the lowest y value
    vector<cluster> coords;
    coordinate c = coordinates.back();
    coordinates.pop_back();
    coords.push_back(new_cluster(c));
    for(coordinate c1 : coordinates){
        for(cluster Cluster : coords){
            for(coordinate c2 : Cluster){
                cout << coords.size() << endl;
                //left coordinate non-zero
                if(get<0>(c1) - get<0>(c2) == 1){
                    Cluster.push_back(c1);
                    coordinates.remove(c1);
                }
                //upper coordinate non-zero
                else if(get<1>(c1) - get<1>(c2) == 1){
                    Cluster.push_back(c1);
                    coordinates.remove(c1);
                }
                //upper left coordinate non-zero
                else if(get<0>(c1) - get<0>(c2) == 1 && get<1>(c1) - get<1>(c2)){
                    Cluster.push_back(c1);
                    coordinates.remove(c1);
                }
                //all coordinates are zero
                else{
                    coords.push_back(new_cluster(c1));
                    coordinates.remove(c1);
                }
            }
        }
    }
    return coords;
}*/

vector<cluster> fire_clustering_algorithm(vector<coordinate> coordinates){
    vector<cluster> coords;
    coordinate c = coordinates.back();
    coordinates.pop_back();
    coords.push_back(new_cluster(c));
    for(int c1 = 0; c1 < coordinates.size(); c1++){
        for(int C = 0; C < coords.size(); C++){
            for(int c2 = 0; c2 < coords[C].size(); c2++){
                //left coordinate non-zero
                if(get<0>(coordinates[c1]) - get<0>(coords[C][c2]) == 1){
                    cout << "here!" << endl;
                    coords[C].push_back(coordinates[c1]);
                }
                //upper coordinate non-zero
                else if(get<1>(coordinates[c1]) - get<1>(coords[C][c2]) == 1){
                    coords[C].push_back(coordinates[c1]);
                }
                //upper left coordinate non-zero
                else if(get<0>(coordinates[c1]) - get<0>(coords[C][c2]) == 1 && get<1>(coordinates[c1]) - get<1>(coords[C][c2])){
                    coords[C].push_back(coordinates[c1]);
                }
                //all coordinates are zero
                else{
                    coords.push_back(new_cluster(coordinates[c1]));
                }
            }
        }
    }
    return coords;
}