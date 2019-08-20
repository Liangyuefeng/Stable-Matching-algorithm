IA = open("matching1.txt", 'r+')
IAmatching = eval(IA.read())  # 读取的str转换为字典
print(IAmatching)
IA.close()

DA = open("matching.txt", 'r+')
DAmatching = eval(DA.read())  # 读取的str转换为字典
print(DAmatching)
DA.close()

a=[]
for v in IAmatching.values():
    a.append(v)
print(a)

b=[]
for v in DAmatching.values():
    b.append(v)
print(b)

k=0
for i in a:
    for j in b:
        if i == j:
            k+=1

print(len(a)-k)


# 应该是配对，学生配学校。
