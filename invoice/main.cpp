#include <fstream>
#include <iostream>
#include <iomanip>

int main(int argc, const char* argv[]) {
	std::string filename = "worklog.csv";
	if (argc > 1) {
		filename = argv[1];
	}
	std::ifstream worklog(filename);

	// Ignore the first line containing the field names:
	// date,start,end,payrate,hours,subtotal
	worklog.ignore(1024, '\n');

	std::string value;
	std::string date;
	std::string start;
	std::string end;
	double payrate;
	double hours;
	double subtotal;
	double total;

	std::cout << std::fixed << std::setprecision(2);
	while (!worklog.eof()) {
		getline(worklog, date, ',');
		getline(worklog, start, ',');
		getline(worklog, end, ',');
		getline(worklog, value, ',');
		payrate = stod(value);
		getline(worklog, value, ',');
		hours = stod(value);
		getline(worklog, value);
		subtotal = stod(value);
		std::cout << date << " from " << start << " to " << end << ": $" << payrate << "/hr for " << hours << " hours, subtotal $" << subtotal << std::endl;
		total += subtotal;
		std::cout << "Current total: $" << total << std::endl;
		// Don't attempt to process a trailing newline
		worklog.ignore(1, '\n');
	}

	return 0;
}
