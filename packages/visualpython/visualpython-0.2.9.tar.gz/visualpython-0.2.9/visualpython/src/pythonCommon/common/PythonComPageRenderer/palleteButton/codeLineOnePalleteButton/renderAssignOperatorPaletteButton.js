define ([
    // 기본 
    'require'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpCommon'
    // + 추가 python common 폴더 패키지 : 이진용 주임
    , 'nbextensions/visualpython/src/pythonCommon/api/pythonComStateApi'
], function (requirejs, vpConst, vpCommon,
             pythonComStateApi ) {
    "use strict";
    var { updateOneArrayIndexValueAndGetNewArray } = pythonComStateApi;
    var renderAssignOperatorPaletteButton = function(pythonComPageRendererThis) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var selectedPaletteIndex = pythonComPageRendererThis.getSelectedPaletteIndex();
        var PythonComConstData = pythonComPageRendererThis.getPythonComConstData();
        const { PYTHON_COMMON_GENERATE_CODE_MAKE_VARIABLE_ENUM } = PythonComConstData;
        const { ASSIGN_OPERATOR_TYPE } = PYTHON_COMMON_GENERATE_CODE_MAKE_VARIABLE_ENUM;

        var assignOperatorBlock = $(`<button class="vp-pythonCom-func-btn"
                                        style="padding: 1rem; font-size:12px;">
                                        <span>=</span>
                                    </button>`);
                                    
        assignOperatorBlock.click(function(){
            var newData = {
                type: "ASSIGN_OPERATOR"
                , data: "="
            }

            pythonComStateGenerator.setState({
                paramList: updateOneArrayIndexValueAndGetNewArray( pythonComStateGenerator.getState("paramList"),
                                                                    selectedPaletteIndex, 
                                                                    newData)    
            });
            var mRootTagSelector = pythonComPageRendererThis.getRootTagSelector();
            var mRootBlockTitle = pythonComPageRendererThis.getRootBlockTitle();
            pythonComPageRendererThis.pageRender(mRootTagSelector, mRootBlockTitle);
            pythonComPageRendererThis.showGenerateCodeButton();
        });

        return assignOperatorBlock;
    }
    return renderAssignOperatorPaletteButton;
});