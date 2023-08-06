
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
    var renderRightBracketPaletteButton = function(pythonComPageRendererThis) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var selectedPaletteIndex = pythonComPageRendererThis.getSelectedPaletteIndex();
        var PythonComConstData = pythonComPageRendererThis.getPythonComConstData();
        // const { PYTHON_COMMON_GENERATE_CODE_MAKE_VARIABLE_ENUM } = PythonComConstData;
        // const { RIGHT_BRACKET_TYPE } = PYTHON_COMMON_GENERATE_CODE_MAKE_VARIABLE_ENUM;

        var rightBracketPaletteButton = $(`<button class="vp-pythonCom-func-btn"
                                            style="padding: 1rem; font-size:12px;">
                                            <span class="vp-multilang" data-caption-id=")">)</span>
                                        </button>`);
                                    
        rightBracketPaletteButton.click(function(){
            var newData = {
                type: "RIGHT_BRACKET"
                , data: ")"
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

        return rightBracketPaletteButton;
    }
    return renderRightBracketPaletteButton;
});