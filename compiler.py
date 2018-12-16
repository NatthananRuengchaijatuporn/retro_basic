#2110316 Programming Languages Principles
#Project Retro Basic
#Natthanan Ruengchaijatuporn 5930179921
import sys
bc_type = {'line':'10','id' :'11','const':'12','IF':'13','GOTO':'14','PRINT':'15','STOP':'16','op':'17'}
op_dict = {'+' : '1','-':'2','<':'3','=':'4'}
#--------- check ----------#
def isLineNum(i) :
	return i.isdigit() and int(i) >= 1 and int(i)<= 1000
def isId(i) :
	return len(i) ==1 and i.isalpha() and i.isupper()
def isConst(i) :
	return i.isdigit() and int(i) >= 0 and int(i)<=100
def isOp(i) :
	return i in ['+','-','<','=']
def isTerm(i) :
	return isId(i) or isConst(i)
def getLineNum(i) :
	return bc_type['line'] + " " + i+" "
def getId(i) :
	return bc_type['id'] + " " + str(ord(i.lower())-96) + " "
def getOp(i) :
	return bc_type['op'] + " " + op_dict[i] + " "
def getTerm(i) :
	if isId(i) :
		return getId(i)
	elif isConst(i) :
		return bc_type['const'] + " " + i + " "
#--------- stmt-----------#
def goto(line) :
	if len(line) != 2 or not isLineNum(line[1]):
		return "Error at parser"
	ret = bc_type['GOTO'] + " " + line[1] + " "
	return ret

def iff(line) :
	ret = bc_type['IF'] + " 0 "
	if len(line) != 5 or not isLineNum(line[4]) or not isTerm(line[1]) or not isTerm(line[3]) or not(line[2] in ['<','=']) :
		return "Error at parser"
	ret += getTerm(line[1]) + getOp(line[2]) + getTerm(line[3]) + goto(["GOTO"]+[line[4]])
	return ret

def printt(line) :
	if len(line) != 2 or not (isId(line[1])) :
		return "Error at parser"
	ret = bc_type['PRINT'] + " 0 "
	ret += getId(line[1])
	return ret
def asgmnt(line) :
	ret = ""
	if (len(line) != 5 and len(line) != 3) or line[1] != '=' or not isTerm(line[2]):
		return "Error at parser"
	ret += getId(line[0]) + getOp(line[1]) +getTerm(line[2])
	if len(line) == 5 :
		if not line[3] in ['+','-'] or not isTerm(line[4]) :
			return "Error at parser"
		else :
			ret += getOp(line[3]) + getTerm(line[4])
	return ret
#---------------- scanner --------------------#
def scanner(file) :
	check_list = ['<','=','+','-','GOTO','PRINT','STOP','IF']
	list_tkline = []
	lc = 1
	for li in file :
		line = li.strip().split()
		tmp_list = []
		if isLineNum(line[0]) :
			tmp_list.append(line[0])
		else :
			return "Error at scanner at line number in line " + str(lc) + "."
		for j in line[1:]:
			if j in check_list or isId(j) or isConst(j) or isLineNum(j):
				tmp_list.append(j)
			else :
				return "Error at scanner at line number in line " + str(lc) + "."
		list_tkline.append(tmp_list)
		lc += 1
	return list_tkline

#---------------- parser ---------------------#
def parser(tokenList) :
	result = ""
	line_count = 0
	for line1 in tokenList :
		out = ""
		print(line1)
		idx = 0
		if(len(line1)==0) :
			return "Error at parser"
		if not isLineNum(line1[idx]) :
			return "Error at parser"

		out += getLineNum(line1[idx])
		idx += 1
		if line1[idx] == "IF" :
			tmp = iff(line1[idx:])
		elif line1[idx] == "GOTO" :
			tmp = goto(line1[idx:])
		elif line1[idx] == "PRINT" :
			tmp = printt(line1[idx:])
		elif line1[idx] == "STOP" and len(line1)==2:
			tmp = bc_type['STOP'] + " 0"
		elif isId(line1[idx]) :
			tmp = asgmnt(line1[idx:])
		else :
			tmp = "Error at parser"
		if tmp[:5] == "Error" :
			return tmp
		tmp = tmp.strip()
		out += tmp
		out += "\n"
		result += out
	result += "0"
	return result
#----------------main of compiler-------------#
if (len(sys.argv) <=1) :
	print("""ERROR: format is wrong. To use this compiler please use the following command.$python compiler.py [input_path] [output_path]. If you don't pass output_path, the output_path will be output.txt""")
	exit(1)
iname = sys.argv[1]
oname = "output.txt"
if(len(sys.argv) == 3) :
	oname = sys.argv[2]
print("Starting compiling your basic program.")
print("....")
file = open(iname,"r")
error = 0

tokenList = scanner(file)
if tokenList[:5] == "Error" :
	print(tokenList,"\n")
	exit(0)
output = parser(tokenList)
if output[:5] == "Error" :
	print(output,"\n")
	exit(0)


file.close()

output_file = open(oname,"w")
output_file.write(output.strip())
output_file.close()
print("Done!!!")
print("Your B-code is in " + oname)
