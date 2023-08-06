
define ([
    // 기본 
    'require'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpCommon'
    // + 추가 python common 폴더 패키지 : 이진용 주임
    , 'nbextensions/visualpython/src/pythonCommon/api/pythonComStateApi'
    , '../../palleteBlock/index'
], function (requirejs, vpConst, vpCommon,
             pythonComStateApi, palleteBlockList ) {

    "use strict";
    var { renderInputVarPaletteBlock } = palleteBlockList;

    var renderInputVarPaletteButton = function(pythonComPageRendererThis, typeEnum) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var PythonComConstData = pythonComPageRendererThis.getPythonComConstData();
        const { PYTHON_COMMON_GENERATE_CODE_MAKE_VARIABLE_ENUM } = PythonComConstData;
        const { DATA_VARIABLE_TYPE, DATA_NUMBER_TYPE, DATA_STRING_TYPE,
                 DATA_LIST_TYPE, DATA_DICTIONARY_TYPE, DATA_TUPLE_TYPE, DATA_SET_TYPE } = PYTHON_COMMON_GENERATE_CODE_MAKE_VARIABLE_ENUM;
 
        var title = ``;
        var type = ``;
        switch(typeEnum){
            case DATA_VARIABLE_TYPE: {
                title = `변수 입력`;
                type = `VARIABLE`;
                break;
            } 
            case DATA_NUMBER_TYPE: {
                title = `숫자 입력`;
                type = `NUMBER`;
                break;
            }
            case DATA_STRING_TYPE: {
                title = `문자열 입력`;
                type = `STRING`;
                break;
            }
            case DATA_LIST_TYPE: {
                title = `리스트 입력`;
                type = `LIST`;
                break;  
            }
            case DATA_DICTIONARY_TYPE: {
                title = `딕셔너리 입력`;
                type = `DICTIONARY`;
                break;
            }
            case DATA_TUPLE_TYPE: {
                title = `튜플 입력`;
                type = `TUPLE`;
                break;
            }
            case DATA_SET_TYPE: {
                title = `집합 입력`;
                type = `SET`;
                break;
            }
            default: {
                break;
            }
        }
        var palleteButton = $(`<button class="vp-pythonCom-func-btn"
                                                        style="padding: 1rem; font-size:12px;">
                                                    <span class="vp-multilang" data-caption-id="${title}">
                                                        ${title}
                                                    </span>
                                                </button>`);
        palleteButton.click(function() {
            renderInputVarPaletteBlock(pythonComPageRendererThis, typeEnum);
        });

        return palleteButton;
    }

    return renderInputVarPaletteButton;
});

