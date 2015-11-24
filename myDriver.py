from glob import glob
import csv

def read_and_parse(filename):
    import csv
    csvfile = open(filename, 'rb')
    lines = csv.reader(csvfile, delimiter = '|')
    newlines = []
    for row in lines:
        try:
            newlines.append(row)
        except:
            pass
    return {csvfile.name[2:-4] : newlines}
        

userfile = glob('u_*.csv')
userdata = read_and_parse(userfile[0])
#print userdata

followerfiles = glob('f_*.csv')
followerdata = []
for filename in followerfiles:
    followerdata.append(read_and_parse(filename))
print followerdata[4:7]

