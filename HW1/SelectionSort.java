package ProgrammingAssignment1;

import java.util.Arrays;

public class SelectionSort {
	
	public static void sort(int [] array)	{
		for (int i = 0; i < array.length; i++)	{
			int minIndex = i;
			for (int j = i; j < array.length; j++) {
				if (array[i] > array[j])
					minIndex = j;
			}
			swap(array, i, minIndex);
		}
	}
	
	public static void swap(int [] array, int i, int j)	{
		int temp = array[i];
		array[i] = array[j];
		array[j] = temp;
	}





	Ignore this
	public static void main(String[] args) {
		int[] a = {100, 90, 80, 70, 60, 50, 40, 30, 20, 10};
		
		System.out.println(Arrays.toString(a));
		sort(a);
		System.out.println(Arrays.toString(a));
	}

}
