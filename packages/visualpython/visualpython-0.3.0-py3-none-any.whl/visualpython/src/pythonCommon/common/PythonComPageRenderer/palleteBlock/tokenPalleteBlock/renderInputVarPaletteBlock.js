define ([
    // 기본 
    'require'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpCommon'
    // + 추가 python common 폴더 패키지 : 이진용 주임
    // , 'nbextensions/visualpython/src/pythonCommon/api/pythonComStateApi'
    , '../helperFunc'
    , '../state'
], function (requirejs, vpConst, vpCommon,
             helperFuncList, PalleteBlockState ) {
    "use strict";
 
    var { makeBtnDomArray
          , bindClickPaletteConfirmButton
          , bindClickBackButton } = helperFuncList;
    var palleteBlockState = new PalleteBlockState();

    /** renderConditionOperatorPalleteBlock
     *  변수, 문자, 숫자 생성하기 위한 token을 만드는 PalleteBlock 렌더링
     *  @param { pythonComPageRenderer this} pythonComPageRendererThis
     *  @param { Symbol } typeEnum
     */
    var renderInputVarPaletteBlock = function(pythonComPageRendererThis, typeEnum) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var PythonComConstData = pythonComPageRendererThis.getPythonComConstData();
        const { PYTHON_COMMON_GENERATE_CODE_MAKE_VARIABLE_ENUM } = PythonComConstData;
        const { DATA_VARIABLE_TYPE, DATA_NUMBER_TYPE, DATA_STRING_TYPE,
                 DATA_LIST_TYPE, DATA_DICTIONARY_TYPE, DATA_TUPLE_TYPE, DATA_SET_TYPE } = PYTHON_COMMON_GENERATE_CODE_MAKE_VARIABLE_ENUM;
 
        var uuid = vpCommon.getUUID();

        var paletteBodyView = pythonComPageRendererThis.getPaletteBodyView();
        paletteBodyView.empty();
        var typeName = ``;
        var typeEnum;
        switch(typeEnum){
            case DATA_VARIABLE_TYPE: {
                typeName = `변수 입력`;
                break;
            } 
            case DATA_NUMBER_TYPE: {
                typeName = `숫자 입력`;
                break;
            }
            case DATA_STRING_TYPE: {
                typeName = `문자 입력`;
                break;
            }
            case DATA_LIST_TYPE: {
                typeName = `리스트 입력`;
                break;  
            }
            case DATA_DICTIONARY_TYPE: {
                typeName = `딕셔너리 입력`;
                break;
            }
            case DATA_TUPLE_TYPE: {
                typeName = `튜플 입력`;
                break;
            }
            case DATA_SET_TYPE: {
                typeName = `집합 입력`;
                break;
            }
            default: {
                break;
            }
        }
        const { paletteContainer
                , paletteConfirmButton } = pythonComPageRendererThis._renderSelectCodeLineTokenBlockAndConfirmButton(`${typeName}`, uuid);

        var flexRow = $(`<div class="vp-pythonCom-style-flex-row">
                        </div>`);
        var input = $(`<input type="text"/>`);
        flexRow.append(input);
        paletteContainer.append(flexRow);
        paletteContainer.append(paletteConfirmButton);
        paletteBodyView.append(paletteContainer);

        // 변수 입력 input
        $(input).on("change keyup paste", function() {
            var newData = {
                type: typeEnum 
                , data: $(this).val()
                , indentSpaceNum: 0
            }
            palleteBlockState.setPalleteBlockState(newData);
        });

        //paletteConfirmButton 클릭
        bindClickPaletteConfirmButton(pythonComPageRendererThis, palleteBlockState, uuid);
        // back button 클릭
        bindClickBackButton(pythonComPageRendererThis, uuid);
    }

    return renderInputVarPaletteBlock;
});