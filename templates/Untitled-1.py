a = int(input("Enter a number"))
b = int(input("Enter another number"))
c = int(input("Enter a third number"))
if (a<b ):
    if(a<c):
        print(a)
        print(b)
        print(c)
elif(b<a):
    if(b<c):
        print(b)
        print(a)
        print(c)
else:
    print(c)
    pritn(b)
    print(a)