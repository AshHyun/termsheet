from copy import copy
import random
import streamlit as st
import pandas as pd

def dfs_must(chart, remain, solved):
    
    if False in solved:
        for i, issolved in enumerate(solved):
            if issolved:
                continue
            else:
                who, which = must[i]
                for num, term in enumerate(chart):
                    if not term[who]:
                        for spec in which:
                            if remain[num][spec] == 0:
                                continue
                        
                            temp_chart = copy(chart)
                            temp_solved = copy(solved)
                            temp_remain = copy(remain)

                            temp_chart[num][who] = spec
                            temp_solved[i] = True
                            temp_remain[num][spec] -= 1

                            success, c, r = dfs_must(temp_chart, temp_remain, temp_solved)
                            if success:
                                return success, c, r


    else:
        print("Done")
        return True, chart, remain

def lucky(chart, remain):
    print(chart)
    print(remain)
    chances = []
    for spec, qty in enumerate(remain):
        for i in range(qty):
            chances.append(spec)
    random.shuffle(chances)
    cnt = 0
    for i, spec in enumerate(chart):
        if spec == None:
            chart[i] = chances[cnt]
            cnt += 1
    return chart

submit_must = False
st.title("근무표")
with st.form(key='form1'):
    specs = st.text_area("근무 과")
    submit_specs = st.form_submit_button(label='완료')

specs = specs.strip().split('\n')
spec2idx = {spec : i for i, spec in enumerate(specs)}
with st.form(key='form2'):
    pos = {}
    if specs:
        for i, spec in enumerate(specs):
            need = st.slider(f"{spec}의 필수 인원", min_value=1, max_value=10, key=i)
            pos[i] = need
    pos = list(pos.values())
    columns = []
    for s, p in zip(specs, pos):
        for i in range(p):
            if p > 1:
                columns.append(s + f'-{i+1}')
            else:
                columns.append(s)

    names = st.text_area("이름").split()
    submit_pos = st.form_submit_button(label='완료')



st.write('필수조건의 수를 입력하고, 그 조건을 체크해주세요')
must = []

for i, person in enumerate(names):
    num = st.text_input(f'{person}의 필수 조건 수', key=i)
    if num == '0':
        continue
    elif num != '':
        dic = {}
        for j in range(int(num)):
            mult = st.multiselect("필수 과", options=specs, key=f'{person}_{j}')
            temp = []
            if len(mult) == 0:
                continue
            for m in mult:
                temp.append(spec2idx[m])
            dic[j] = temp
        # print(list(dic.items()))
        must += list(dic.items())
print(must)
button = st.button("근무표 확인")
if button:
# pos = [2,1,1,1,1]
    remain = [copy(pos) for i in range(7)]
    doctors = len(names)
    # must = [[0, [0,1]], [1, [1]], [4, [0]], [5, [0]]]
    solved = [False for i in range(len(must))]
    entry = [[None for i in range(doctors)] for j in range(7)]

    success, c, r = dfs_must(entry, remain, solved)
    result = []
    print(c, r)
    for i in range(7):
        result.append(lucky(c[i], r[i]))
    total = []
    for r in result:
        people = [i[0] for i in sorted(enumerate(r), key=lambda x:x[1])]
        people2name = []
        for p in people:
            people2name.append(names[p])
        total.append(people2name)
    index = [f'{i+1}텀' for i in range(7)]
    df = pd.DataFrame(total, columns=columns, index=index)
    st.dataframe(df)
    st.balloons()