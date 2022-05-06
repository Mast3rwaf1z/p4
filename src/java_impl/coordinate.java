package java_impl;

import java.util.ArrayList;

public class coordinate {
    int x = 0;
    int y = 0;
    coordinate(int x, int y){
        this.x = x;
        this.y = y;
    }
    public static ArrayList<coordinate> new_coordinate_list(int x, int y){
        ArrayList<coordinate> list = new ArrayList<coordinate>();
        list.add(new coordinate(x, y));
        return list;
    }
}
