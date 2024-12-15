import math
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import exergy_dashboard as ed


input_variable_info_dict = {
    'T_0': {
        'latex': r'$T_0$',
        'explaination': '환경 온도',
        'unit': '℃',
        'type': 'input',
        'default': 32.0,
        'group': 1,
    },
    'T_g': {
        'latex': r'$T_g$',
        'explaination': '토양 온도',
        'unit': '℃',
        'type': 'input',
        'default': 19.0,
        'group': 1,
    },
    'T_a_int_in': {
        'latex': r'$T_{a,int,in}$',
        'explaination': '실내기로 들어가는 공기 온도',
        'unit': '℃',
        'type': 'input',
        'default': 24.0,
        'group': 1,
    },
    'k': {
        'latex': r'$k$',
        'explaination': 'COP 보정 계수',
        'unit': '-',
        'type': 'input',
        'default': 0.4,
        'group': 2,
    },
    'E_f_int': {
        'latex': r'$E_{f,int}$',
        'explaination': '실내기 측 팬 전력',
        'unit': 'kW',
        'type': 'input',
        'default': 0.21,
        'group': 3,
    },
    'E_f_ext': {
        'latex': r'$E_{f,ext}$',
        'explaination': '실외기 측 팬 전력',
        'unit': 'kW',
        'type': 'input',
        'default': 0.29,
        'group': 3,
    },
    'Q_r_int_A': {
        'latex': r'$Q_{r,int,A}$',
        'explaination': '실내기 실내 흡열량(ASHP)',
        'unit': 'kW',
        'type': 'input',
        'default': 15.252,
        'group': 3,
    },
    'E_pmp_G': {
        'latex': r'$E_{pmp,G}$',
        'explaination': '지열교환기 펌프 전력(GSHP)',
        'unit': 'kW',
        'type': 'input',
        'default': 0.48,
        'group': 3,
    },
    'Q_r_int_G': {
        'latex': r'$Q_{r,int,G}$',
        'explaination': '실내기 실내 흡열량(GSHP)',
        'unit': 'kW',
        'type': 'input',
        'default': 15.252,
        'group': 3,
    },
    'dT_a': {
        'latex': r'$\Delta T_a$',
        'explaination': '입구 측 공기&출구 측 공기 온도차',
        'unit': '℃',
        'type': 'input',
        'default': 10.0,
        'group': 4,
    },
    'dT_r': {
        'latex': r'$\Delta T_r$',
        'explaination': '냉매&출구 측 공기 온도차',
        'unit': '℃',
        'type': 'input',
        'default': 5.0,
        'group': 4,
    }, 
}

group_names = [
    '', 
    '1. 온도 입력 조건',
    '2. COP 보정 계수',
    '4. 시스템 용량',
    '3. 온도차',
]

# Constants.
c_a = 1.005 # kJ/kgK
rho_a = 1.2 # kg/m^3

st.set_page_config(
    page_title='Exergy',
    page_icon=':fire:',
    layout='wide',
)

ml, mr = 1, 1
pad = 0.5
col_border = False
_, title_col, _ = st.columns([ml, 4 + pad + 5, mr], border=col_border)
_, title_col1, _, title_col2, _ = st.columns([ml, 4, pad, 5, mr], border=col_border)
_, col11, col12, _, col2, _ = st.columns([ml, 2, 2, pad, 5, mr], border=col_border)
_, button_col11, _, _, _, _ = st.columns([ml, 2, 2, pad, 5, mr], border=col_border)

with title_col:
    st.markdown("# Exergy Analysis Program  :fire:")

with title_col1:
    st.markdown('## Input data :dart:')

with title_col2:
    st.markdown('## Output data :chart_with_upwards_trend:')
    # st.divider()

group_name_used = [False] * len(group_names)
with col11:
    for k, v in input_variable_info_dict.items():
        if  v['group'] == 3:
            continue

        if not group_name_used[v['group']]:
            st.write('')
            st.markdown(f"##### {group_names[v['group']]}")
            group_name_used[v['group']] = True

        if v['type'] == 'input':
            input_variable_info_dict[k]['value'] = st.number_input(
                f"{v['explaination']}, {v['latex']} [{v['unit']}]",
                value=v['default'],
                step=0.1,
                format="%.1f",
                # label_visibility='collapsed',
            )

with col12:
    for k, v in input_variable_info_dict.items():
        if  v['group'] != 3:
            continue

        if not group_name_used[v['group']]:
            st.write('')
            st.markdown(f"##### {group_names[v['group']]}")
            group_name_used[v['group']] = True

        if v['type'] == 'input':
            input_variable_info_dict[k]['value'] = st.number_input(
                f"{v['explaination']}, {v['latex']} [{v['unit']}]",
                value=v['default'],
                step=0.1,
                format="%.1f",
                # label_visibility='collapsed',
            )

with button_col11:
    # TODO: Align the button to the right
    ok = st.button('Calculate')


for k_, v in input_variable_info_dict.items():
    if k_.startswith('T_'):
        _ = exec(f"{k_} = {v['value'] + 273.15}")
    else:
        _ = exec(f"{k_} = {v['value']}")

# =============== Calculation ===============

T_a_int_out = T_a_int_in - dT_a   # 실내기에서 나가는 공기 온도
T_a_ext_in = T_0        # 실외기로 들어가는 공기 온도(=환경온도)
T_a_ext_out = T_a_ext_in + dT_a   # 실외기에서 나가는 공기 온도
T_r_int_A = T_a_int_out - dT_r    # 실내기 측 냉매 온도(ASHP)
T_r_ext_A = T_a_ext_out + dT_r   # 실외기 측 냉매 온도(ASHP)
T_r_int_G = T_a_int_out - dT_r   # 실내기 측 냉매 온도(GSHP)
T_r_ext_G = T_g + dT_a   # 실외기 측 냉매 온도(GSHP)

cop_A = k * T_r_int_A / (T_r_ext_A - T_r_int_A)
cop_G = k * T_r_int_G / (T_r_ext_G - T_r_int_G)

# System capacity - ASHP
E_cmp_A = Q_r_int_A / cop_A    # kW, 압축기 전력(ASHP)
Q_r_ext_A = Q_r_int_A + E_cmp_A    # kW, 실외기 배출열량(ASHP)

# System capacity - GSHP
E_cmp_G = Q_r_int_G / cop_G    # kW, 압축기 전력(GSHP)
Q_r_ext_G = Q_r_int_G + E_cmp_G    # kW, 실외기 배출열량(GSHP)
Q_g = Q_r_ext_G + E_pmp_G    # kW, 토양 열교환량(GSHP)

# Air & Cooling water parameters
V_int = Q_r_int_A / (c_a * rho_a * (T_a_int_in - T_a_int_out))
V_ext = Q_r_ext_A / (c_a * rho_a * (T_a_ext_out - T_a_ext_in))
m_int = V_int * rho_a
m_ext = V_ext * rho_a

## Internal unit with evaporator
X_r_int_A = - Q_r_int_A * (1 - T_0 / T_r_int_A) # 냉매에서 실내 공기에 전달한 엑서지
X_int_out_A = c_a * m_int * ((T_a_int_out - T_0) - T_0 * math.log(T_a_int_out / T_0)) # 실외기 취출 공기 엑서지 
X_int_in_A = c_a * m_int * ((T_a_int_in - T_0) - T_0 * math.log(T_a_int_in / T_0)) # 실외기 흡기 공기 엑서지

Xin_int_A = E_f_int + X_r_int_A # 엑서지 인풋 (팬 투입 전력 + 냉매에서 실내 공기에 전달한 엑서지)
Xout_int_A = X_int_out_A - X_int_in_A # 엑서지 아웃풋
Xc_int_A = Xin_int_A - Xout_int_A # 엑서지 소비율

## Closed refrigerant loop system  
X_r_ext_A = Q_r_ext_A * (1 - T_0 / T_r_ext_A) # 냉매에서 실외 공기에 전달한 엑서지
X_r_int_A = - Q_r_int_A * (1 - T_0 / T_r_int_A) # 냉매에서 실내 공기에 전달한 엑서지

Xin_r_A = E_cmp_A # 엑서지 인풋 (컴프레서 투입 전력)
Xout_r_A = X_r_ext_A + X_r_int_A # 엑서지 아웃풋
Xc_r_A = Xin_r_A - Xout_r_A # 엑서지 소비율

## External unit with condenser
X_r_ext_A = Q_r_ext_A * (1 - T_0 / T_r_ext_A) # 냉매에서 실외 공기에 전달한 엑서지
X_ext_out_A = c_a * m_ext * ((T_a_ext_out - T_0) - T_0 * math.log(T_a_ext_out / T_0)) # 실외기 취출 공기 엑서지
X_ext_in_A = c_a * m_ext * ((T_a_ext_in - T_0) - T_0 * math.log(T_a_ext_in / T_0)) # 실외기 흡기 공기 엑서지 (외기)

Xin_ext_A = E_f_ext + X_r_ext_A # 엑서지 인풋 (팬 투입 전력 + 냉매에서 실외 공기에 전달한 엑서지)
Xout_ext_A = X_ext_out_A - X_ext_in_A # 엑서지 아웃풋
Xc_ext_A = Xin_ext_A - Xout_ext_A # 엑서지 소비율

## Total
Xin_A = E_cmp_A + E_f_int + E_f_ext # 총 엑서지 인풋 (컴프레서 + 실내팬 + 실외팬 전력)
Xout_A = X_int_out_A - X_int_in_A # 총 엑서지 아웃풋
Xc_A = Xin_A - Xout_A # 총 엑서지 소비율

## Internal unit with evaporator
X_r_int_G = - Q_r_int_G * (1 - T_0 / T_r_int_G) # 냉매에서 실내 공기에 전달한 엑서지
X_int_out_G = c_a * m_int * ((T_a_int_out - T_0) - T_0 * math.log(T_a_int_out / T_0)) # 실외기 취출 공기 엑서지
X_int_in_G = c_a * m_int * ((T_a_int_in - T_0) - T_0 * math.log(T_a_int_in / T_0)) # 실외기 흡기 공기 엑서지

Xin_int_G = E_f_int + X_r_int_G # 엑서지 인풋 (팬 투입 전력 + 냉매에서 실내 공기에 전달한 엑서지)
Xout_int_G = X_int_out_G - X_int_in_G # 엑서지 아웃풋
Xc_int_G = Xin_int_G - Xout_int_G # 엑서지 소비율

## Closed refrigerant loop system
X_r_ext_G = - Q_r_ext_G * (1 - T_0 / T_r_ext_G) # 냉매에서 실외기측에 전달한 엑서지
X_r_int_G = - Q_r_int_G * (1 - T_0 / T_r_int_G) # 냉매에서 실내 공기에 전달한 엑서지

Xin_r_G = E_cmp_G + X_r_ext_G # 엑서지 인풋 (컴프레서 투입 전력 + 냉매에서 실외기측에 전달한 엑서지)
Xout_r_G = X_r_int_G # 엑서지 아웃풋
Xc_r_G = Xin_r_G - Xout_r_G # 엑서지 소비율

## Circulating water in GHE
X_g = - Q_g * (1 - T_0 / T_g) # 땅에서 추출한 엑서지
X_r_ext_G = - Q_r_ext_G * (1 - T_0 / T_r_ext_G) # 냉매에서 실내 공기에 전달한 엑서지

Xin_ext_G = E_pmp_G + X_g # 엑서지 인풋 (펌프 투입 전력 + 땅에서 추출한 엑서지)
Xout_ext_G = X_r_ext_G # 엑서지 아웃풋
Xc_GHE = Xin_ext_G - Xout_ext_G # 엑서지 소비율

## Total
Xin_G = E_cmp_G + E_f_int + E_pmp_G # 총 엑서지 인풋 (컴프레서 + 실내팬 + 펌프 전력)
Xout_G = X_int_out_G - X_int_in_G # 총 엑서지 아웃풋
Xc_G = Xin_G - Xout_G # 총 엑서지 소비율

# =============== Calculation Done ==========



with col2:
    st.write('')
    st.markdown('##### 1. Waterfall plot')
    if ok:
        fig = ed.plot_waterfall(
            Xin_A, Xc_int_A, Xc_r_A, Xc_ext_A, X_ext_out_A, Xout_A,
            Xin_G, X_g, Xc_int_G, Xc_r_G, Xc_GHE, Xout_G,
        )
        st.write(fig)
    else:
        st.write('Press the button to calculate')