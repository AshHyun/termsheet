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
def check_duplicate(before, cur):
    count = 0
    for i,j in zip(before, cur):
        if i == j:
            count += 1
    return count
def lucky(before_chart, chart, remain):
    chances = []
    for spec, qty in enumerate(remain):
        for i in range(qty):
            chances.append(spec)

    if not before_chart:
        random.shuffle(chances)
        cnt = 0
        for i, spec in enumerate(chart):
            if spec == None:
                chart[i] = chances[cnt]
                cnt += 1
        return chart
    else:
        best = 10000
        best_chart = None
        for r in range(100):
            chart_temp = copy(chart)
            random.shuffle(chances)
            cnt = 0
            for i, spec in enumerate(chart_temp):
                if spec == None:
                    chart_temp[i] = chances[cnt]
                    cnt += 1
            loss = check_duplicate(before_chart, chart_temp)
            if loss < best:
                best = loss
                best_chart = chart_temp
        return best_chart


if 'step' not in st.session_state:
    st.session_state.step = 0

st.title("Term Planner")
st.caption("made by JH")

if st.session_state.step == 0:
    with st.form(key='form1'):
        specs = st.text_area("??? ????????? ??? ?????? ????????? ??????????????????.")
        submit_specs = st.form_submit_button(label='??????')
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
                need = st.slider(f"{spec} ?????????", min_value=1, max_value=5, key=i)
                pos[i] = need
        pos = list(pos.values())
        columns = []
        for s, p in zip(specs, pos):
            for i in range(p):
                if p > 1:
                    columns.append(s + f'-{i+1}')
                else:
                    columns.append(s)
        names = st.text_area("?????? ?????? (????????? ????????? ??????????????????)").split()
        submit_pos = st.form_submit_button(label='??????')
    if submit_pos:
        if sum(pos) != len(names):
            st.error("???????????? ?????? ?????? ???????????? ????????????. ???????????? ??? ???????????? ?????????.")
        else:
            st.success(f"?????? ????????? ?????? ??? {sum(pos)}???, ????????? {len(names)}???")
        st.session_state.pos = pos
        st.session_state.step = 2
        st.session_state.names = names
        st.session_state.specs = specs
        st.session_state.spec2idx = spec2idx
        st.session_state.columns = columns


if st.session_state.step == 2:
    st.write('??????????????? ?????? ????????????, ??? ????????? ??????????????????')
    must = []
    names = st.session_state.names
    specs = st.session_state.specs
    spec2idx = st.session_state.spec2idx
    pos = st.session_state.pos
    columns = st.session_state.columns

    for i, person in enumerate(names):
        num = st.number_input(f'{person}??? ?????? ?????? ???', key=i, min_value=0, value=0, max_value=7, step=1)
        if num == 0:
            continue
        dic = {}
        for j in range(num):
            mult = st.multiselect("?????? ???", options=specs, key=f'{person}_{j}')
            temp = []
            if len(mult) == 0:
                continue
            for m in mult:
                temp.append(spec2idx[m])
            dic[i] = temp
        # print(list(dic.items()))
        must += list(dic.items())

    button = st.button("????????? ??????")

    if button:
    # pos = [2,1,1,1,1]
        remain = [copy(pos) for i in range(7)]
        doctors = len(names)
        # must = [[0, [0,1]], [1, [1]], [4, [0]], [5, [0]]]
        solved = [False for i in range(len(must))]
        entry = [[None for i in range(doctors)] for j in range(7)]

        # print(entry, remain, must)
        success, c, r = dfs_must(entry, remain, solved)
        if not success:
            st.error("??????????????????. ?????????????????????")
        else:
            st.success("?????? ??????")
            result = []
            for i in range(7):
                if i == 0:
                    result.append(lucky(None, c[i], r[i]))
                    continue
                result.append(lucky(result[i-1], c[i], r[i]))

            total = []
            for r in result:
                people = [i[0] for i in sorted(enumerate(r), key=lambda x:x[1])]
                people2name = []
                for p in people:
                    people2name.append(names[p])
                total.append(people2name)
            index = [f'{i+1}???' for i in range(7)]
            df = pd.DataFrame(total, columns=columns, index=index)
            csv = df.to_csv()
            st.table(df)
            st.download_button(
                label="CSV ????????????",
                data=csv,
                file_name='term.csv',
                mime='text/csv',
            )
            print(csv)