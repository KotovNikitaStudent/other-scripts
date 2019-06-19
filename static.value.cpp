#include <iostream>
#include <cmath>
using namespace std;
double root_mean_square(double* arr,int size);
double arithmetic(double* arr, int size);
double average(double* arr, int size);
double root_mean_square(double* arr, int size)//������������������ �����������
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
double arithmetic(double* arr, int size)//�������������������� �����������
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
double average(double* arr, int size)//������� ��������
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
		cout << "������� ����� ���������: ";
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
			cout << i << " ��������� - " << x[i] << endl;
		}
		cout << "������� ��������: " << average(x, n) << endl;
		cout << "�������������������� �����������: " << arithmetic(x, n) << endl;
		cout << "������������������ �����������: " << root_mean_square(x, n) << endl;
		double alfa;
		cout << "������� ����������� ��������� ��� �������� ��������� = 0,95 (� ����������� �� ����� ���������): ";
		cin >> alfa;
		double delt_x = (root_mean_square(x, n) * alfa) / sqrt(n);
		cout << "���������� ������: " << average(x, n) << " +- " << delt_x << endl;
		delete[] x;
	system("pause");
	return 0;
}

