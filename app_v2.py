import math
import functools
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

def create_dynamic_multiview(dataframes, cols=2):
    """
    다양한 길이의 데이터프레임 리스트로부터 동적 다중 뷰 플롯 생성
    
    Parameters:
    - dataframes: 차트로 만들 데이터프레임 리스트
    - cols: 열의 개수 (기본값 2)
    """
    colors = [
        '#4c95d9',
        '#a8d9ff',
        '#ff6a6a',
        '#ffc4c4',
        '#69c7ba',
        '#a4f3bd',
        '#ffab4c',
        '#ffde96',
        '#9878d2',
        '#e1e5ec',
    ] * 50
    # 각 데이터프레임에 대한 기본 차트 생성 함수
    def create_base_chart(df, title, n):
        print('color:', colors[n])

        # 데이터프레임의 숫자형 컬럼 찾기
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 1:
            # 단일 숫자 컬럼인 경우 히스토그램
            chart = alt.Chart(df).mark_bar(color=colors[n]).encode(
                alt.X(f'{numeric_cols[0]}:Q', bin=True),
                alt.Y('count()', stack=None)
            )
        elif len(numeric_cols) >= 2:
            # 두 개 이상의 숫자 컬럼인 경우 산점도
            chart = alt.Chart(df).mark_circle(color=colors[n]).encode(
                x=f'{numeric_cols[0]}:Q',
                y=f'{numeric_cols[1]}:Q',
                color=alt.value('steelblue')
            )
        else:
            # 숫자 컬럼이 없는 경우 막대 그래프
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns
            if len(categorical_cols) > 0:
                chart = alt.Chart(df).mark_bar(color=colors[n]).encode(
                    x=f'{categorical_cols[0]}:N',
                    y='count()'
                )
            else:
                raise ValueError("플롯할 적절한 컬럼이 없습니다.")
        
        chart.configure_mark(
            color=colors[n],
        )

        return chart.properties(
            title=title, 
            width=300, 
            height=200
        )
    
    # 동적으로 차트 리스트 생성
    charts = [
        create_base_chart(df, df['system'].iloc[0], i) 
        for i, df in enumerate(dataframes)
    ]
    
    # 열 수에 맞춰 동적으로 레이아웃 생성
    def chunk_charts(lst, chunk_size):
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]
    
    # 차트들을 chunk로 나누어 수평/수직 결합
    chart_rows = [
        alt.hconcat(*row_charts) 
        for row_charts in chunk_charts(charts, cols)
    ]
    
    # 최종 수직 결합
    return alt.vconcat(*chart_rows)

st.set_page_config(
    page_title='Exergy Analysis',
    page_icon=':fire:',
    layout='wide',
    initial_sidebar_state='expanded'
)

sss = st.session_state

if 'systems' not in sss:
    sss.systems = {}

if 'system_count' not in sss:
    sss.system_count = 0


case_system = {
    'cooling': {
        'ASHP': {

        },
        'GSHP': {
        },
    },
    'heating': {
        'ASHP': {
        },
        'GSHP': {
        },
    },
    'hotwater': {
        'ASHP': {
        },
        'GSHP': {
        },
    },
}

def create_system(type_='ASHP'):
    sss.system_count += 1

    system = {
        'name': f'System {sss.system_count}',
        'type': type_,
        'parameters': {
            'COP': {   
                'explaination': 'Coefficient of Performance',
                'latex': r'$COP$',
                'default': 4.0,
                'unit': '-',
            },
            'Q_r_int': {
                'explaination': 'Internal heat gain',
                'latex': r'$Q_{r,int}$',
                'default': 15.252,
                'unit': 'kW',
            },
            'E_pmp': {
                'explaination': 'Pump power',
                'latex': r'$E_{pmp}$',
                'default': 0.48,
                'unit': 'kW',
            },
            'dT_a': {
                'explaination': 'Temperature difference between inlet and outlet air',
                'latex': r'$\Delta T_a$',
                'default': 10.0,
                'unit': '℃',
            },
            'QQQ': {
                'explaination': 'Stock god',
                'latex': r'$QQQ$',
                'default': 10.0,
                'unit': '℃',
            },
        },
    }

    return system

# data = create_system(type_='ASHP')
# sss.systems[data['name']] = data

def add_system(type_):
    print('=' * 80)
    data = create_system(type_)
    print(data)
    sss.systems[data['name']] = data

st.header(':fire: Exergy Analyzer  ', help='This is a help message.')

with st.sidebar:
    st.title('시스템 설정')

    st.divider()
    st.subheader('시스템 추가')
    selected = st.selectbox('System type', ['ASHP', 'GSHP'])
    st.button(
        'Add system',
        use_container_width=True,
        on_click=functools.partial(add_system, type_=selected),
    )

    # st.divider()
    # st.subheader('시스템 제거')
    # st.button('Remove system', use_container_width=True)

    st.divider()
    st.subheader('Exergy Analysis')
    st.button('Calculate', use_container_width=True)

    st.divider()
    st.subheader('Plot')
    st.button('Plot', use_container_width=True)

    st.write('Gas constant')
    st.number_input('R', value=8.314, step=0.1, format="%.1f")


# st.get_option('layout')
ml, mr = 0.0001, 0.0001
pad = 0.2
col_border = False
_, title_col, _ = st.columns([ml, 4 + pad + 5, mr], border=col_border)
_, title_col1, _, title_col2, _ = st.columns([ml, 4, pad, 5, mr], border=col_border)
_, col1, _, col2, _ = st.columns([ml, 4, pad, 5, mr], border=col_border)


def remove_system(name):
    sss.systems.pop(name)


with col1:
    st.header('System Inputs :dart:')
    if len(sss.systems) == 0:
        st.write('No system added yet.')
        # st.stop()
    else:
        st.write(' ')
        st.write(' ')
        tabs = st.tabs(sss.systems.keys())
        for tab, system in zip(tabs, sss.systems.values()):
            if system['type'] == 'ASHP':
                tab.write('### Air Source Heat Pump :snowflake:')
            elif system['type'] == 'GSHP':
                tab.write('### Ground Source Heat Pump :earth_americas:')

            for k, v in system['parameters'].items():
                system['parameters'][k]['value'] = tab.number_input(
                    f"{v['explaination']}, {v['latex']} [{v['unit']}]",
                    value=v['default'],
                    step=0.1,
                    format="%.1f",
                    # label_visibility='collapsed',
                    key=f"{system['name']}_{k}",
                )

            tab.button(
                'Remove system',
                use_container_width=True,
                key=system['name'],
                on_click=functools.partial(remove_system, name=system['name']),
            )

    # [system['name'] for system in sss.systems.values()]


with col2:
    st.header('Output Data :chart_with_upwards_trend:')
    options = st.multiselect(
        'Select systems to display',
        [system['name'] for system in sss.systems.values()],
        # default=sss.selected_options if 'selected_options' in sss else None,
    )

    if len(options) != 0:
        st.subheader('1. Random property (overlay)')
        # Draw random altair chart. but use options.
        chart_data = pd.DataFrame(
            data={
                'a': np.random.randn(100),
                'b': np.random.randn(100),
                'c': np.random.randn(100),
                'system': np.random.choice(options, 100),
            },
        )

        c = alt.Chart(chart_data).mark_circle().encode(
            x='a', y='b', size='c', color='system', tooltip=['a', 'b', 'c']
        ).interactive()

        st.altair_chart(c, use_container_width=True)

        st.subheader('2. Random property (subplot)')
        # Draw random altair chart. but use options.
        chart_data = pd.DataFrame(
            data={
                'a': np.random.randn(100),
                'b': np.random.randn(100),
                'c': np.random.randn(100),
                'system': np.random.choice(options, 100),
            },
        )

        dataframes = [
            chart_data[chart_data['system'] == option]
            for option in options
        ]

        c = create_dynamic_multiview(dataframes, cols=3)

        # c = alt.Chart(chart_data).mark_circle().encode(
        #     x='a', y='b', size='c', column='system', tooltip=['a', 'b', 'c']
        # ).interactive()

        st.altair_chart(c)