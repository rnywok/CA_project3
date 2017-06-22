#!/usr/bin/python
import sys


def main(argv):
    input_name = argv[1]
    output_name = argv[2]
    result=[]
    num_sn=""	
    num_sn2=1
    try:
        with open(input_name) as inFile:
            for line in inFile:
                stripped = line.strip()
                if len(stripped) < 1 or not stripped[0].isdigit():
                    #blank line or not debug message
                    continue

                tokens = line.split()
                tick = int(tokens[0][:-1])
                debug_flag = tokens[1][:-1]
                message = " ".join(tokens[2:])
		tokens2=message.split()
                if debug_flag == 'system.cpu.fetch':
                        if 'Instruction is:' in message:
                                k=message.strip()
                                instruction = k[24:].strip()
                                mem = dict()
                                mem['inst']=instruction
                                result.append(mem)  
                if debug_flag == 'system.cpu.iew':
                        if 'Issue: Adding PC' in message:
                                temp=tokens2[5]
				length=len(temp)
				num_sn=temp[4:length-1]
				num_sn2=int(num_sn)
           		        number = tick/500
                                result[num_sn2-1]['issue']= number
                                result[num_sn2-1]['sn']=num_sn2
                        if 'Execute: Processing PC' in message:
				temp=tokens2[5]
				length=len(temp)-1
				num_sn=temp[4:length-1]
				num_sn2=int(num_sn)
                                number = tick/500
                                result[num_sn2-1]['execute']= number
                if debug_flag == 'system.cpu':
                        if 'Removing instruction' in message:
                                temp=tokens2[3]
				length=len(temp)
				num_sn=temp[4:length-1]
				num_sn2=int(num_sn)
        	                number = tick/500
                                result[num_sn2-1]['commit']= number
               
		 #your code here

    except IOError as e:
        print "error opening file to read: {}".format(input_name)
        exit(1)

    try:
        with open(output_name, "w") as outFile:
            table="#sn,inst,issued,execution_completed,committed\n"
 	    outFile.write(table)
            for i in result:
                if 'execute' in i and 'commit' in i:
                   outFile.write(str(i['sn'])+"\t"+i['inst']+"\t"+str(i['issue'])+"\t"+str(i['execute'])+"\t"+str(i['commit'])+"\n")  

		 #your code here
            pass

    except IOError as e:
        print "error opening file to write: {}".format(
            output_name)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: exe_order.py <input file name> <output file name>"
        exit(1)
    main(sys.argv)
