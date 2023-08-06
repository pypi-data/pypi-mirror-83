
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
    var { renderInputVarPaletteBlock, renderConditionOperatorPalleteBlock } = palleteBlockList;
    var { updateOneArrayIndexValueAndGetNewArray } = pythonComStateApi;

    var renderConditionOperatorPalleteButton = function(pythonComPageRendererThis) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var conditionOperatorPalleteButton = $(`<button class="vp-pythonCom-func-btn"
                                                        style="padding: 1rem; font-size:12px;">
                                                    <span class="vp-multilang" data-caption-id="비교 연산자">
                                                        비교 연산자
                                                    </span>
                                                </button>`);
        conditionOperatorPalleteButton.click(function() {

            renderConditionOperatorPalleteBlock(pythonComPageRendererThis);
        });

        return conditionOperatorPalleteButton;
    }

    return renderConditionOperatorPalleteButton;
});

