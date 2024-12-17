COOLING_ASGP = {
    'parameters':{
        'T_0': {
            'explanation': {'EN': 'Environment Temperature', 'KR': '환경온도'},
            'latex': r'$T_0$',
            'default': 32.0,
            'range': [-50, 50],
            'unit': '℃',
            'step': 0.1,
        },
        'T_a_int_in': {
            'explanation': {'EN': 'Indoor Unit Inlet Air Temperature', 'KR': '실내기로 들어가는 공기 온도'},
            'latex': r'$T_{a,int,in}$',
            'default': 24.0,
            'range': [-50, 50],
            'unit': '℃',
            'step': 0.1,
        },
        'T_a_int_out': {
            'explanation': {'EN': 'Indoor Unit Outlet Air Temperature (=Indoor Temperature)', 'KR': '실내기에서 나가는 공기 온도'},
            'latex': r'$T_{a,int,out}$',
            'default': 14.0,
            'range': [-60, 'T_a_int_in-2'],
            'unit': '℃',
            'step': 0.5,
        },
        'T_a_ext_out': {
            'explanation': {'EN': 'Outdoor Unit Outlet Air Temperature', 'KR': '실외기에서 나가는 공기 온도'},
            'latex': r'$T_{a,ext,out}$',
            'default': 42.0,
            'range': ['T_0+2', 80],
            'unit': '℃',
            'step': 0.5,
        },
        'T_r_int_A': {
            'explanation': {'EN': 'Indoor Unit Refrigerant Temperature', 'KR': '실내기 측 냉매 온도(ASHP)'},
            'latex': r'$T_{r,int,A}$',
            'default': 9.0,
            'range': [-80, 'T_a_int_out-2'],
            'unit': '℃',
            'step': 0.5,
        },
        'T_r_ext_A': {
            'explanation': {'EN': 'Outdoor Unit Refrigerant Temperature', 'KR': '실외기 측 냉매 온도(ASHP)'},
            'latex': r'$T_{r,ext,A}$',
            'default': 47.0,
            'range': ['T_a_ext_out+2', 100],
            'unit': '℃',
            'step': 0.5,
        },
        'k': {
            'explanation': {'EN': 'COP Correction Factor', 'KR': 'COP 보정 계수'},
            'latex': r'$k$',
            'default': 0.4,
            'range': [0, 1],
            'unit': '-',
            'step': 0.01,
        },
        'E_f_int': {
            'explanation': {'EN': 'Indoor Unit Fan Power', 'KR': '실내기 측 팬 전력'},
            'latex': r'$E_{f,int}$',
            'default': 0.21,
            'range': [0, 1],
            'unit': 'kW',
            'step': 0.01,
        },
        'E_f_ext': {
            'explanation': {'EN': 'Outdoor Unit Fan Power', 'KR': '실외기 측 팬 전력'},
            'latex': r'$E_{f,ext}$',
            'default': 0.29,
            'range': [0, 1],
            'unit': 'kW',
            'step': 0.01,
        },
        'Q_r_int_A': {
            'explanation': {'EN': 'Indoor Unit Heat Absorption', 'KR': '실내기 실내 흡열량'},
            'latex': r'$Q_{r,int,A}$',
            'default': 15.252,
            'range': [0, 30],
            'unit': 'kW',
            'step': 0.001,
        },
    }
}


COOLING_GSHP = {
    'parameters':{
        'T_0': {
            'explanation': {'EN': 'Environment Temperature', 'KR': '환경온도'},
            'latex': r'$T_0$',
            'default': 32.0,
            'range': [-50, 50],
            'unit': '℃',
            'step': 0.5,
        },
        'T_g': {
            'explanation': {'EN': 'Ground Temperature', 'KR': '토양온도'},
            'latex': r'$T_g$',
            'default': 19.0,
            'range': [-30, 'T_0'],
            'unit': '℃',
            'step': 0.5,
        },
        'T_a_int_in': {
            'explanation': {'EN': 'Indoor Unit Inlet Air Temperature', 'KR': '실내기로 들어가는 공기 온도'},
            'latex': r'$T_{a,int,in}$',
            'default': 24.0,
            'range': [-50, 50],
            'unit': '℃',
            'step': 0.5,
        },
        'T_a_int_out': {
            'explanation': {'EN': 'Indoor Unit Outlet Air Temperature(=Indoor Temperature)', 'KR': '실내기에서 나가는 공기 온도'},
            'latex': r'$T_{a,int,out}$',
            'default': 14.0,
            'range': [-60, 'T_a_int_in-2'],
            'unit': '℃',
            'step': 0.1,
        },
        'T_r_int_G': {
            'explanation': {'EN': 'Indoor Unit Refrigerant Temperature', 'KR': '실내기 측 냉매 온도'},
            'latex': r'$T_{r,int,G}$',
            'default': 9.0,
            'range': [-80, 'T_a_int_out-2'],
            'unit': '℃',
            'step': 0.1,
        },
        'T_r_ext_G': {
            'explanation': {'EN': 'Outdoor Unit Refrigerant Temperature', 'KR': '실외기 측 냉매 온도'},
            'latex': r'$T_{r,ext,G}$',
            'default': 29.0,
            'range': ['T_g+2', 'T_0-2'],
            'unit': '℃',
            'step': 0.1,
        },
        'k': {
            'explanation': {'EN': 'COP Correction Factor', 'KR': 'COP 보정 계수'},
            'latex': r'$k$',
            'default': 0.4,
            'range': [0, 1],
            'unit': '-',
            'step': 0.01,
        },
        'E_f_int': {
            'explanation': {'EN': 'Indoor Unit Fan Power', 'KR': '실내기 측 팬 전력'},
            'latex': r'$E_{f,int}$',
            'default': 0.21,
            'range': [0, 1],
            'unit': 'kW',
            'step': 0.01,
        },
        'E_f_ext': {
            'explanation': {'EN': 'Outdoor Unit Fan Power', 'KR': '실외기 측 팬 전력'},
            'latex': r'$E_{f,ext}$',
            'default': 0.29,
            'range': [0, 1],
            'unit': 'kW',
            'step': 0.01,
        },
        'E_pmp_G': {
            'explanation': {'EN': 'Outdoor Unit Fan Power', 'KR': '실외기 측 팬 전력'},
            'latex': r'$E_{f,ext}$',
            'default': 0.29,
            'range': [0, 1],
            'unit': 'kW',
            'step': 0.01,
        },
        'Q_r_int_G': {
            'explanation': {'EN': 'Indoor Unit Heat Absorption', 'KR': '실내기 실내 흡열량'},
            'latex': r'$Q_{r,int,A}$',
            'default': 15.252,
            'range': [0, 30],
            'unit': 'kW',
            'step': 0.001,
        },
    },
}


SYSTEM_CASE = {
    'COOLING': {
        'ASHP': COOLING_ASGP,
        'GSHP': COOLING_GSHP,
    },
    'HEATING': {
    },
    'HOT WATER': {
      
    },
}
