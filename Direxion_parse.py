import csv

def read_csv(csv_name):
	with open(csv_name, "r", encoding = "utf8") as etf_file:
		reader = csv.reader(etf_file)
		reader = list(reader)
		etf_dict = {}
		for i in range(1, len(reader)):
			if reader[i][1] not in etf_dict.keys() and len(reader[i][2]) > 0:
				etf_dict[reader[i][1]] = [reader[i][2]]
			elif reader[i][1] in etf_dict.keys() and len(reader[i][2]) > 0:
				etf_dict[reader[i][1]].append(reader[i][2])
		etf_file.close()
	return etf_dict


def get_ticker(etf_ticker):
	etfs = read_csv("Direxion-ETFs-Daily-Holdings-File.csv")
	if etf_ticker in etfs.keys():
		return etfs[etf_ticker]
	return []
stocks = get_ticker("VSPY")
print(stocks)