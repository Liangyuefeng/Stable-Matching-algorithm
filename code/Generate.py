import random
import pandas as pd

st_id = []
# st = input('Please enter students number:')
st = 2500
st_num = int(st)
for i in range(st_num):
    st_id.append(i)

school_id = []
# sc = input('Please enter schools number:')
sc = 50
sc_num = int(sc)
for i in range(sc_num):
    school_id.append(i)

print(st_id)
print(school_id)
print('-------------------------------------')

st_pref = []
list1 = []
for i in range(0, len(st_id)):
    all_num = sc_num
    num = sc_num
    result = random.sample(range(0, all_num), num)
    st_pref.append(result)

st = pd.DataFrame(data=st_pref)   #columns=name,
print(st)
st.to_csv('F:/Python_Code/Comp702/data/full_preferencelist/50/Students-Preference1.csv', mode='w')


print('----------------------------')

sc_pref = []
list1 = []
for i in range(0, len(school_id)):
    all_num = st_num
    num = st_num
    result = random.sample(range(0, all_num), num)
    sc_pref.append(result)

sc = pd.DataFrame(data=sc_pref)  #columns=name,
print(sc)
sc.to_csv('F:/Python_Code/Comp702/data/full_preferencelist/50/Schools-Preference1.csv', mode='w')

print("end")
