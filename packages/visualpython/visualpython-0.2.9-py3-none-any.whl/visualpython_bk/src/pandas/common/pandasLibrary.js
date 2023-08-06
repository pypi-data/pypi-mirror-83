define([], function() {

    /**
     * name / description / code
     * variable / return :
     * {
     * name
     * label
     * type		    var / str / num
     * var_type	
     * required		false
     * pair		    true
     * show		    true
     * component	input / option / option_bool
     * option
     * option_label
     * attributes: { title / value / class / data- }
     * }
     */

    var _PANDAS_FUNCTION = {
        'pd001': {
            name: 'Series',
            description: '동일한 데이터 타입의 1차원 배열 생성',
            code: '{return} = pd.Series({v})',
            variable: [
                {
                    name: 'data',
                    label: 'Series 입력값',
                    type: ['var'],
                    var_type: ['Series', 'list', 'dict'],
                    required: true,
                    pair: false
                },
                {
                    name: 'index',
                    label: 'index',
                    type: ['var'],
                    var_type: ['list']
                },
                {
                    name: 'name',
                    label: 'Series 이름',
                    type: ['var', 'str']                  
                }
            ],
            return: [
                {
                    type: ['var'],
                    var_type: ['Series'],
                    label: 'Series 변수명'
                }
            ]
        },
        'pd002': {
            name: 'Dataframe',
            description: '2차원의 Table 형태 변수 생성',
            code: '{return} = pd.DataFrame({v})',
            variable: [
                {
                    name: 'data',
                    label: 'DataFrame 입력값',
                    type: ['var'],
                    var_type: ['DataFrame', 'list', 'dict'],
                    required: true,
                    pair: false
                },
                {
                    name: 'index',
                    label: '행 목록',
                    type: ['var'],
                    var_type: ['list']
                },
                {
                    name: 'columns',
                    label: '열 목록',
                    type: ['var'],
                    var_type: ['list']          
                }
            ],
            return: [
                {
                    type: ['var'],
                    var_type: ['DataFrame'],
                    label:'DataFrame 변수명'
                }
            ]
        },
        'pd003': {
            name: 'Index',
            description: '색인 객체 생성',
            code: '{return} = pd.Index({v})',
            variable: [
                {
                    name: 'data',
                    label: 'Index 배열',
                    type: ['var'],
                    var_type: ['list', 'Series', 'Index'],
                    required: true,
                    pair: false
                },
                {
                    name: 'dtype',
                    label: '넘파이 데이터유형',
                    type: ['str'],
                    component: 'option',
                    option: ['object', 'int32', 'int64', 'float32', 'float64', 'string', 'complex64', 'bool'],
                    option_label: ['객체', '정수형(32)', '정수형(64)', '실수형(32)', '실수형(64)', '문자형', '복소수(64bit)', 'bool형']
                },
                {
                    name: 'copy',
                    type: ['var'],
                    label: '복사 여부',
                    component: 'option_bool',
                    default: false
                },
                {
                    index: 3,
                    name: 'name',
                    type: ['var'],
                    label: '인덱스 명칭'
                },
                {
                    index: 4,
                    name: 'tupleize_cols',
                    type: ['bool'],
                    label: 'MultiIndex 생성 여부',
                    default: true,
                    component: 'option_bool'
                }
            ],
            return: [
                {
                    type: ['var'],
                    var_type: ['Index'],
                    label:'Index 변수명'
                }
            ]
        }
    };

    return {
        _PANDAS_FUNCTION: _PANDAS_FUNCTION
    }
});