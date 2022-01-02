file1 = open('myfile.txt', 'w')
x=["file"+"000000000000"+str(x)+".jpg"+'\n' for x in list(range(7172))]
file1.writelines(x)
file1.close()