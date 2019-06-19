#include <iostream>
#include <cmath>
using namespace std;
double root_mean_square(double* arr,int size);
double arithmetic(double* arr, int size);
double average(double* arr, int size);
double root_mean_square(double* arr, int size)//среднеквадратичная погрешность
{
	double sredn = average(arr, size);
	double kvdr = 0;
	for (int i = 0; i < size; i++)
	{
		//if ((arr[i] - sredn) < 0)
		//{
		//	(arr[i] - sredn)*(-1);
		//}
		kvdr += pow((arr[i] - sredn), 2);
	}
	return (sqrt(kvdr / (size - 1)));
}
double arithmetic(double* arr, int size)//среднеарифметическая погрешность
{
	double sredn = average(arr, size);
	double kvdr = 0;
	for (int i = 0; i < size; i++)
	{
		//if ((arr[i] - sredn) < 0)
		//{
		//	(arr[i] - sredn)*(-1);
		//}
 		kvdr += pow((arr[i] - sredn), 2);
	}
	return (sqrt(kvdr/(size*(size-1))));
}
double average(double* arr, int size)//средняя величина
{
	double sum = 0;
	for (int i = 0; i < size; i++)
	{
		sum += arr[i];
	}
	return (sum / size);
}

int main()
{
	setlocale(0, "Russian");
		double n;
		cout << "Введите число измерений: ";
		cin >> n;
		double *x = new double[n];
		for (int i = 0; i < n; i++)
		{
			double temp;
			cin >> temp;
			x[i] = temp;
		}
		for (int i = 0; i < n; i++)
		{
			cout << i << " измерение - " << x[i] << endl;
		}
		cout << "Средняя величина: " << average(x, n) << endl;
		cout << "Среднеарифметическая погрешность: " << arithmetic(x, n) << endl;
		cout << "Среднеквадратичная погрешность: " << root_mean_square(x, n) << endl;
		double alfa;
		cout << "Введите коэффициент Стьюдента для точности измерений = 0,95 (в зависимости от числа измерений): ";
		cin >> alfa;
		double delt_x = (root_mean_square(x, n) * alfa) / sqrt(n);
		cout << "Абсолютная ошибка: " << average(x, n) << " +- " << delt_x << endl;
		delete[] x;
	system("pause");
	return 0;
}

