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


class School(object):
    def __init__(self, id, prefList, capacity=1):
        self.prefList = prefList
        self.capacity = capacity
        self.held = set()
        self.id = id

    def reject(self):
        # trim the self.held set down to its capacity, returning the list of rejected students.
        if len(self.held) < self.capacity:
            return set()
        else:
            sortedStudents = sorted(list(self.held), key=lambda student: self.prefList.index(student.id))  #school排序，key:student 的prefList
            self.held = set(sortedStudents[:self.capacity])

            return set(sortedStudents[self.capacity:])

    def __repr__(self):
        return repr(self.id)


def verifyStable(students, schools, matching):
    import itertools

    def precedes(a,b,c):
        # print(a)
        if b in a:
            if a.index(b) < a.index(c):
                return True
    # precedes = lambda L, item1, item2: L.index(item1) < L.index(item2)

    def partner(student):
        a = []
        # print("student",student)
        for school in schools:
            # print("school",school)
            if student.id in matching[school.id]:
                # print("yes")
                a.append(school.id)

        # print(a)
        return a[0]
    # partner = lambda student: list(filter(lambda s: student.id in matching[s.id], schools))[0]

    def studentPrefers(student, school):
        a = student.prefList
        b = school.id
        c = partner(student)
        return precedes(a, b, c)

    def schoolPrefers(school, student1):
        list = []
        for i in matching[school.id]:
            for student in students:
                if student.id == i:
                    list.append(precedes(school.prefList, student1.id, student.id))
        return any(list)

    for value in matching.values():
        for (student, school) in itertools.product(students, schools):
            if student.id not in value:
                continue
            if student.id not in matching[school.id]:

                if studentPrefers(student, school):      #如果为真，说明匹配的学校index比随机的大

                    if schoolPrefers(school, student):    #如果为真，说明匹配的学生的index随机的大

                        return False


    return True


if __name__ == "__main__":

    data1 = pd.read_csv('F:/Python_Code/Comp702/data/full_preferencelist/10/Schools-Preference19.csv')  # read data from file
    school = data1.set_index('Unnamed: 0').T.to_dict('list')
    print("Schools's preference list:", school)

    data2 = pd.read_csv('F:/Python_Code/Comp702/data/full_preferencelist/10/Students-Preference19.csv')
    student = data2.set_index('Unnamed: 0').T.to_dict('list')
    print("Students's preference list:", student)

    students = []  # allocate keys and values in dict to Student class
    for k, v in student.items():
        students.append(Student(k, v))
    print("Students ID:", students)

    schools = []
    for k, v in school.items():
        schools.append(School(k, v, 20))
    print("Schools ID:", schools)

    fr = open("matching1.txt", 'r+')
    matching = eval(fr.read())  # 读取的str转换为字典
    print(matching)
    fr.close()

    print("Stable?: ", verifyStable(students, schools, matching))

