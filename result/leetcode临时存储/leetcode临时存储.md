原文链接：http://www.cnblogs.com/codingbigdog/archive/2022/08/31/16643326.html
提交日期：Wed, 31 Aug 2022 07:39:00 GMT
博文内容：
```

class Solution {
public:
    int binarySearch(vector<int>& nums, int target, bool lower) {
        int left = 0, right = (int)nums.size() - 1, ans = (int)nums.size();
        while (left <= right) { 
            int mid = (left + right) / 2; // 中间偏左的数，所以mid在某一时刻会落在left上
            if (nums[mid] > target || (lower && nums[mid] >= target)) {
                right = mid - 1;
                ans = mid; 
            } else {
                left = mid + 1;
            }
        }
        return ans;
    }

    int search(vector<int>& nums, int target) {
        int leftIdx = binarySearch(nums, target, true); // 找第一个大于等于target 的下标
        int rightIdx = binarySearch(nums, target, false) - 1; // 第一个大于target 的位置减一
        if (leftIdx <= rightIdx){   //&& rightIdx < nums.size() && nums[leftIdx] == target && nums[rightIdx] == target) {
            return rightIdx - leftIdx + 1;
        }
        return 0;
    }
};
```

1.binarySearch函数中的nums[mid] >= target与nums[mid] > target的区别？
答：首先明白两点：
- 使用二分法不断地移动左右两边，ans每次都是查找范围的最右边+1。
- 当lower为true时，nums[mid] > target || (lower && nums[mid] >= target)等价于nums[mid] >= target
当lower为false时，nums[mid] > target || (lower && nums[mid] >= target)等价于nums[mid] > target

则：
如果nums中有target，那么肯定会有left和right之间全都是target的时刻，此时nums[mid] > target和nums[mid] >= target的区别就显现出来了，前者是left向右移，后者是right向左移。


2.search中的rightIdx < nums.size() && nums[leftIdx] == target && nums[rightIdx] == target可以没有吗？
答：可以。如果nums中没有target，那么binarySearch(nums, target, false)将会等于binarySearch(nums, target, true)，也就是说leftIdx=rightIdx+1，即leftIdx>rightIdx。


3.nums中没有target，那么ans会落在哪里？
答：不管nums中有没有target，最后的结果一定是left=right+1，即ans=left。

4.nums中没有target，那么ans会大于还是小于target？
答：不一定，情况很复杂。

二分法不会用，可以参考：[链接](https://www.cnblogs.com/zhaozhibo/p/14983880.html)。博文中对二分法查找目标值和二分法查找目标值的左右边界进行了介绍，这两种情况的不同在于遇到了target以后，是否继续收缩查找区间，而不同的收缩方向决定了查找的是左边界还是右边界。
博文的查找边界的代码，最终会使得left=right，此时如果是查找右边界，则右边界为right-1（left-1）；此时如果是查找左边界，则左边界为right（left）。
上面提到的leetcode答案只是将博文中的代码进行了整合。两者都有下面情况：
- 查找左边界代码：如果nums为空，会返回0。
查找右边界代码：如果nums为空，会返回-1。
- 没有target时，查找左边界代码和查找右边界代码返回相同的数。



我对leetcode答案的修改：
```
class Solution {
public:
    int binarySearch(vector<int>& nums, int target, bool lower) {
        int left = 0, right = (int)nums.size() - 1, ans = (int)nums.size();
        while (left <= right) { 
            int mid = (left + right) / 2; // 中间偏左的数，所以mid在某一时刻会落在
            if (nums[mid] > target || (lower && nums[mid] >= target)) {
                right = mid - 1;
                ans = mid; 
            } else {
                left = mid + 1;
            }
        }
        return ans;
    }

    int search(vector<int>& nums, int target) {
        int leftIdx = binarySearch(nums, target, true); // 找第一个大于等于target 的下标
        
        // 如果target很多的时候，这种方法的效率就会低很多。
        int n = 0;
        if( leftIdx< nums.size() && nums[leftIdx] == target){  // leftIdx不会低于零，所以不用写判断语句
            for(;leftIdx<nums.size() && nums[leftIdx]==target; ++leftIdx)  ++n;
        }

        return n;
    }
};
```
