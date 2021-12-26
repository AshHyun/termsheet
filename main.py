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


if 'step' not in st.session_state:
    st.session_state.step = 0

st.title("Term Planner")
st.caption("made by JH")
print(st.session_state.step)
if st.session_state.step == 0:
    with st.form(key='form1'):
        specs = st.text_area("과 종류를 한 줄에 하나씩 입력해주세요.")
        submit_specs = st.form_submit_button(label='다음')
    if submit_specs:
        st.session_state.step = 1
        st.session_state.specs = specs

if st.session_state.step == 1:
    specs = st.session_state.specs
    specs = specs.strip().split('\n')
    spec2idx = {spec : i for i, spec in enumerate(specs)}
    with st.form(key='form2'):
        pos = {}
        if specs:
            for i, spec in enumerate(specs):
                need = st.slider(f"{spec} 인원수", min_value=1, max_value=5, key=i)
                pos[i] = need
        pos = list(pos.values())
        columns = []
        for s, p in zip(specs, pos):
            for i in range(p):
                if p > 1:
                    columns.append(s + f'-{i+1}')
                else:
                    columns.append(s)
        names = st.text_area("이름 입력 (한줄에 한명씩 입력해주세요)").split()
        submit_pos = st.form_submit_button(label='다음')
    if submit_pos:
        if sum(pos) != len(names):
            st.error("인원수와 자리 수가 일치하지 않습니다. 새로고침 후 재시도해 주세요.")
        else:
            st.success(f"배정 가능한 자리 수 {sum(pos)}개, 인원수 {len(names)}명")
        st.session_state.pos = pos
        st.session_state.step = 2
        st.session_state.names = names
        st.session_state.specs = specs
        st.session_state.spec2idx = spec2idx
        st.session_state.columns = columns


if st.session_state.step == 2:
    st.write('필수조건의 수를 입력하고, 그 조건을 체크해주세요')
    must = []
    names = st.session_state.names
    specs = st.session_state.specs
    spec2idx = st.session_state.spec2idx
    pos = st.session_state.pos
    columns = st.session_state.columns

    for i, person in enumerate(names):
        num = st.number_input(f'{person}의 필수 조건 수', key=i, min_value=0, value=0, max_value=7, step=1)
        if num == 0:
            continue
        dic = {}
        for j in range(num):
            mult = st.multiselect("필수 과", options=specs, key=f'{person}_{j}')
            temp = []
            if len(mult) == 0:
                continue
            for m in mult:
                temp.append(spec2idx[m])
            dic[j] = temp
        # print(list(dic.items()))
        must += list(dic.items())

    button = st.button("근무표 확인")

    if button:
    # pos = [2,1,1,1,1]
        remain = [copy(pos) for i in range(7)]
        doctors = len(names)
        # must = [[0, [0,1]], [1, [1]], [4, [0]], [5, [0]]]
        solved = [False for i in range(len(must))]
        entry = [[None for i in range(doctors)] for j in range(7)]

        success, c, r = dfs_must(entry, remain, solved)
        if not success:
            st.error("불가능합니다. 재시도해주세요")
        else:
            st.success("처리 완료")
            result = []
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
            csv = df.to_csv().encode('utf-8')
            st.dataframe(df)
            st.download_button(
                label="CSV 다운로드",
                data=csv,
                file_name='term.csv',
                mime='text/csv',
            )