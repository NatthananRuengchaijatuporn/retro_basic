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
		return "error goto"
	ret = bc_type['GOTO'] + " " + line[1] + " "
	return ret

def iff(line) :
	ret = bc_type['IF'] + " 0 "
	if not isLineNum(line[4]) or len(line) != 5 or not isTerm(line[1]) or not isTerm(line[3]) or not(line[2] in ['<','=']) :
		return "error if"
	ret += getTerm(line[1]) + getOp(line[2]) + getTerm(line[3]) + goto(["GOTO"]+[line[4]])
	return ret

def printt(line) :
	if len(line) != 2 or not (isId(line[1])) :
		return "error printt"
	ret = bc_type['PRINT'] + " 0 "
	ret += getId(line[1])
	return ret
def asgmnt(line) :
	ret = ""
	if (len(line) != 5 and len(line) != 3) or line[1] != '=' or not isTerm(line[2]):
		return "error asgmnt3,5"
	ret += getId(line[0]) + getOp(line[1]) +getTerm(line[2])
	if len(line) == 5 :
		if not line[3] in ['+','-'] or not isTerm(line[4]) :
			return "error asgmnt5"
		else :
			ret += getOp(line[3]) + getTerm(line[4])
	return ret

#----------------main of compiler-------------#
print(len(sys.argv))
if (len(sys.argv) <=1) :
	print("""ERROR: format is wrong. To use this compiler please use the following command.$python compiler.py [input_path] [output_path]. If you don't pass output_path, the output_path will be output.txt""")
	exit(1)
iname = sys.argv[1]
oname = "output.txt"
if(len(sys.argv) == 3) :
	oname = sys.argv[2]
print("Starting compiling your basic program.")
print("....")
result = ""
file = open(iname,"r")
error = 0
#error1 : don't have line num
#error2 : only line num?
#error3 : 
#eof = 0
line_count = 0
for line in file :
	out = ""
	line1 = line.strip().split()
	print(line1)
	idx = 0
	if(len(line1)==0) :
		#eof = 1
		break
	if not isLineNum(line1[idx]) :
		error = 1
		break
	if len(line1) <= 1 :
		error = 2
		break
	out += getLineNum(line1[idx])
	idx += 1

	if line1[idx] == "IF" :
		tmp = iff(line1[idx:])
	elif line1[idx] == "GOTO" :
		tmp = goto(line1[idx:])
	elif line1[idx] == "PRINT" :
		tmp = printt(line1[idx:])
	elif line1[idx] == "STOP" :
		tmp = bc_type['STOP'] + " 0"
	elif isId(line1[idx]) :
		tmp = asgmnt(line1[idx:])
	else :
		tmp = "error 1"
		error = int(tmp[6])
	if tmp[:5] == "error" :
		error = tmp[6:]
		break
	tmp = tmp.strip()
	out += tmp
	out += "\n"
	result += out




if(error!=0) : 
	print("ERROR : at line "+ str(line_count)+" unexpected syntax. Error case : "+str(error))
	exit(1)


result += "0"
file.close()

output_file = open(oname,"w")
output_file.write(result.strip())
output_file.close()
print("Done!!!")
print("Your B-code is in " + oname)
