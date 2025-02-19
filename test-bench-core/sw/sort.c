// sort.c
#include <stdio.h>

void selection_sort(int arr[], int sorted_arr[], int n) {
    int i, j, min_idx, temp;
    for (i = 0; i < n-1; i++) {
        min_idx = i;
        for (j = i+1; j < n; j++) {
            if (arr[j] < arr[min_idx]) {
                min_idx = j;
            }
        }
        // Swap the found minimum element with the first element
        temp = arr[min_idx];
        arr[min_idx] = arr[i];
        arr[i] = temp;
    }
}

void call_selection_sort() {
    int arr[10] = {1,3,7,2,5,8,2,4,9,6};
    int sorted_arr[10] = {0};
    int n = 10;

    selection_sort(arr, sorted_arr, n);
    return 0;
}
