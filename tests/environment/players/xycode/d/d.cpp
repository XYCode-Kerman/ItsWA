// 必定编译失败，非法代码
#include <bits/stdc++.h>
#include </dev/null>
#include <con>
using namespace std;

int main() {
    string s;cin>>s;  // 错误解，只能过第一个测试点
    // string s;getline(cin,s);  // 正解，可过第二个测试点
    cout<<s<<' '<<s;

    return 0;
}