#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <array>
#include <algorithm>
using namespace std;

class Sport
{
public:
	Sport(string KingOfSport, double WorldRecord, const array<int, 3>& temp);
	Sport();
	~Sport();
	void PrintWorldRecord(vector<Sport>& list, string KingOfSport);
	void PrintRecordInData(vector<Sport>& list, int currentData);
	void SortByKingOfSport(vector<Sport>& list);
	string getInfo();
private:
	string KingOfSport;
	double WorldRecord;
	array<int, 3> DataRecord;
};

Sport::Sport()
{
	KingOfSport = "";
	WorldRecord = 0;
	DataRecord = {};
}

Sport::Sport(string KingOfSport, double WorldRecord, const array<int, 3>& temp)
{
	this->KingOfSport = KingOfSport;
	this->WorldRecord = WorldRecord;
	this->DataRecord = temp;
}

void Sport::PrintWorldRecord(vector<Sport>& list, string KingOfSport)
{
	for (vector<Sport>::iterator i = list.begin(); i != list.end(); ++i)
	{
		if (i->KingOfSport == KingOfSport)
		{
			cout << "In " << KingOfSport << " will be worls record: ";
			cout << i->WorldRecord << endl;
		}
		else
		{
			cout << "Data not find" << endl;
			return;
		}
	}
}

void Sport::PrintRecordInData(vector<Sport>& list, int currentData)
{
	for (vector<Sport>::iterator i = list.begin(); i != list.end(); ++i)
	{
		if (i->DataRecord.at(1) == currentData)
		{
			cout << "In " << currentData << " month will be world record: ";
			cout << i->WorldRecord << endl;
		}
		else
		{
			cout << "Data not find" << endl;
			return;
		}
	}
}

void Sport::SortByKingOfSport(vector<Sport>& list)
{
	sort(list.begin(), list.end(), [](Sport& e1, Sport& e2) {
	return e1.KingOfSport < e2.KingOfSport;	});
}

string Sport::getInfo()
{
	string temp_str;
	for (const auto& i : DataRecord)
	{
		temp_str = to_string(i) + " ";
	}
	return KingOfSport + " " + to_string(WorldRecord) + " " + temp_str;
}

Sport::~Sport()
{
}

int main()
{
	setlocale(LC_ALL, "ru");

	string path = "C:\\Users\\Никита\\Desktop\\1.txt";
	vector <Sport> list;

	string bufKingOfSport;
	double bufWorldRecord;
	int dd, mm, yy;
	array<int, 3> temp;

	fstream DataFile;
	DataFile.open(path, fstream::in | fstream::out | fstream::app);
	if (DataFile.is_open())
	{
		while (!DataFile.eof())
		{
			DataFile >> bufKingOfSport;
			DataFile >> bufWorldRecord;
			DataFile >> dd;
			DataFile >> mm;
			DataFile >> yy;
			temp = { dd, mm, yy };
			list.push_back(Sport(bufKingOfSport, bufWorldRecord, temp));
		}
	}
	
	// Разблокировать, чтобы выполнить сортировку (SortByKingOfSport) по названию вида спорта 
	/*
	Sport sport = Sport();
	cout << "\nUnsorted" << endl;
	for (auto &i: list)
	{
		cout << i.getInfo() << endl;
	}

	sport.SortByKingOfSport(list);

	cout << "\nSorted" << endl;
	for (auto& i : list)
	{
		cout << i.getInfo() << endl;
	}*/

	// Разблокировать конструктор без параметров, чтобы исполнить методы PrintRecordInData и PrintWorldRecord
	/*
	Sport sport = Sport();
	sport.PrintRecordInData(list, 2);
	sport.PrintWorldRecord(list, "Atlet");
	*/
	
	// Разблокировать, чтобы выполнить удаление n-го элемента списка
	/*
	int n;
	cout << "Enter index of list, to remove n element :";
	cin >> n;
	list.erase(list.begin() + n);
	*/

	// Разблокировать, чтобы выполнить добавление элемента в список
	/*
	string tempKingOfSport;
	double tempWorldRecord;
	int temp_dd, temp_mm, temp_yy;
	array<int, 3> temp_arr;

	cout << "Enter data in the form: sport << record << record date" << endl;
	cout << "Enter sport: ";
	cin >> tempKingOfSport;
	cout << "Enter record: ";
	cin >> tempWorldRecord;
	cout << "Enter record date dd: ";
	cin >> temp_dd;
	cout << "Enter record date mm: ";
	cin >> temp_mm;
	cout << "Enter record date yy: ";
	cin >> temp_yy;
	temp_arr = { temp_dd, temp_mm, temp_yy };
	list.push_back(Sport(tempKingOfSport, bufWorldRecord, temp_arr));
	*/
	
	// Разблокировать, чтобы выполнить изменение n-го элемента в списке
	/*
	string tempKingOfSport;
	double tempWorldRecord;
	int new_data_index;
	int temp_dd, temp_mm, temp_yy;
	array<int, 3> temp_arr;

	cout << "Enter new data in the form: new_data_index << sport << record << record date" << endl;
	cout << "Enter new_data_index: ";
	cin >> new_data_index;
	cout << "Enter new sport: ";
	cin >> tempKingOfSport;
	cout << "Enter new record: ";
	cin >> tempWorldRecord;
	cout << "Enter new record date dd: ";
	cin >> temp_dd;
	cout << "Enter new record date mm: ";
	cin >> temp_mm;
	cout << "Enter new record date yy: ";
	cin >> temp_yy;
	temp_arr = { temp_dd, temp_mm, temp_yy };
	list.at(new_data_index) = Sport(tempKingOfSport, bufWorldRecord, temp_arr);
	*/

	return 0;
}