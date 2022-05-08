#include <iostream>
#include <list>
using namespace std;
class test{
    public:
    int var = 0;
    test(int n){
        var = n;
    }
};

int main(){
    test t3 = test(1);
    test t4 = test(2);
    list<list<test>> lst;
    list<test> lst2;
    list<test> lst3;
    for(int i = 0; i < 10; i++){
        lst2.push_back(test(i));
    }
    for(int i = 10; i < 20; i++){
        lst3.push_back(test(i));
    }
    lst.push_back(lst2);
    lst.push_back(lst3);
    cout << t3.var << endl;
    cout << t4.var << endl;
    cout << lst.front().back().var << endl;
    cout << lst.back().back().var << endl;
}