# 第一选择率
import pandas as pd


class Student(object):
    def __init__(self, id, prefList):
        self.prefList = prefList
        self.rejections = 0  # num rejections is also the index of the next option
        self.id = id

    def preference(self):
        return self.prefList[self.rejections]

    def __repr__(self):
        return repr(self.id)


def Firstfive(students, matching):
    i = 0
    for student in students:
        for item in matching[student.id]:
            if item in student.prefList:
                i += 1
    return i


if __name__ == "__main__":

    data1 = pd.read_csv('F:/Python_Code/Comp702/data/full_preferencelist/10schools/10/Students-Preference.csv')
    df = data1[['0','1','2']]
    student = df.T.to_dict('list')
    students = []  # allocate keys and values in dict to Student class
    for k, v in student.items():
        students.append(Student(k, v))

    fr1 = open("F:/Python_Code/Comp702/output_matching/full_preferencelist/st_matching/10schools/10/IAmatching.txt", 'r+')
    matching1 = eval(fr1.read())  # 读取的str转换为字典
    # print(matching1)
    fr1.close()
    por1 = Firstfive(students, matching1)
    _i = (por1/len(students))*100
    # print("First choice(DA algorithm):" + str(por1) + "%")
    print(_i)

    loop = 100
    for t in range(loop):
        if t > 0:
            data2 = pd.read_csv(
                'F:/Python_Code/Comp702/data/full_preferencelist/10schools/10/Students-Preference' + str(t) + '.csv')
            df = data2[['0','1','2']]
            student1 = df.T.to_dict('list')
            students = []
            for k, v in student1.items():
                students.append(Student(k, v))

            fr1 = open(
                "F:/Python_Code/Comp702/output_matching/full_preferencelist/st_matching/10schools/10/IAmatching" + str(t) + ".txt",
                'r+')
            matching1 = eval(fr1.read())  # 读取的str转换为字典
            # print(matching1)
            fr1.close()
            por1 = Firstfive(students, matching1)
            _i = (por1 / len(students)) * 100
            # print("First choice(DA algorithm):" + str(_i) + "%")
            print(_i)

