"""Main script for generating output.csv."""

from pandas import *


def subjectFilter(Split):
	# used to return the data selected by 'Split'
	data = DataFrame.from_csv('C:/Users/Jiadong Chen/Desktop/interview/python_hiring_test/python_hiring_test/data/raw/pitchdata.csv')
	if Split == 'vs LHH':
		return data[(data['HitterSide'] =='L')]
	if Split == 'vs RHH':
		return data[(data['HitterSide'] =='R')]
	if Split == 'vs LHP':
		return data[(data['PitcherSide'] =='L')]
	else:
		return data[(data['PitcherSide'] =='R')]	


def dataAnalysis():
	f = open('C:/Users/Jiadong Chen/Desktop/interview/python_hiring_test/python_hiring_test/data/reference/combinations.txt','r')
	lines = f.readlines()
	finalRes = []
	for i in lines[1::]:
		Stat, Subject, Split = i.split(',')
		Split = Split[0:6]
		dataSelected = subjectFilter(Split)
		dataSelected = dataSelected.groupby([Subject]).sum()
		# group the data by 'Subject'
		dataPA = dataSelected[dataSelected['PA'] >= 25]	
		SubjectId = list(dataPA.transpose())
		if Stat == 'AVG':
			dataPA['value'] = dataPA.apply(lambda dataPA: float("{0:.3f}".format(dataPA.H / dataPA.AB)), axis = 1)
			
		if Stat == 'OBP':
			dataPA['value'] =  dataPA.apply(lambda dataPA: float("{0:.3f}".format((dataPA.H + dataPA.BB + dataPA.HBP) / (dataPA.AB + dataPA.BB + dataPA.HBP + dataPA.SF))), axis = 1)
			#print(value)
		if Stat == 'SLG':
			dataPA['value'] =  dataPA.apply(lambda dataPA: float("{0:.3f}".format(dataPA.TB / dataPA.AB)), axis = 1)
		if Stat == 'OPS':
			dataPA['value'] =  dataPA.apply(lambda dataPA: float("{0:.3f}".format((dataPA.TB / dataPA.AB) + ((dataPA.H + dataPA.BB + dataPA.HBP) / (dataPA.AB + dataPA.BB + dataPA.HBP + dataPA.SF)))), axis = 1)

		resData = {'SubjectId': SubjectId, 'Stat': Stat, 'Split': Split, 'Subject': Subject, 'Value': dataPA['value']}
		res = DataFrame(resData)
		finalRes.append(res)
	result = concat(finalRes).sort_values(by = ['SubjectId', 'Stat', 'Split', "Subject"])
	result = result[['SubjectId', "Stat", "Split", "Subject", "Value"]]
	result.to_csv('C:/Users/Jiadong Chen/Desktop/interview/python_hiring_test/python_hiring_test/data/processed/output.csv', index = False)
def main():
    # add basic program logic here
    print('start calculating ...')
    dataAnalysis()
    print('output finished')
    
if __name__ == '__main__':
    main()
