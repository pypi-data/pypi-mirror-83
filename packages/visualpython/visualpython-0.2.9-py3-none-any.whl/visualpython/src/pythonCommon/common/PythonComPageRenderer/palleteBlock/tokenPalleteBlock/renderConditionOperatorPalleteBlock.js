define ([
    // 기본 
    'require'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpCommon'
    // + 추가 python common 폴더 패키지 : 이진용 주임
    , '../helperFunc'
    , '../state'
], function (requirejs, vpConst, vpCommon,
             helperFuncList, PalleteBlockState ) {
    "use strict";
 
    var { makeBtnDomArray
          , clickPaletteConfirmButton
          , bindClickBackButton } = helperFuncList;

    /** renderConditionOperatorPalleteBlock
     *  비교 연산자를 생성하기 위한 token을  Pallete View 동적 렌더링
     *  @param { pythonComPageRenderer this } pythonComPageRendererThis 
     */
    var renderConditionOperatorPalleteBlock = function(pythonComPageRendererThis) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();

        var uuid = vpCommon.getUUID();
        var paletteBodyView = pythonComPageRendererThis.getPaletteBodyView();
        paletteBodyView.empty();

        const { paletteContainer } = pythonComPageRendererThis._renderSelectCodeLineTokenBlockAndConfirmButton("비교 연산자", uuid);
    
        var flexRow = $(`<div class="vp-python-com-style-flex-row-evenly"> </div>`);

        var btnConditionOperatorDataArray = [`<`, `>`, `>=`, `<=`, `==`, `!=`];
        var btnDomArray = makeBtnDomArray(btnConditionOperatorDataArray);

        paletteContainer.append(flexRow);
        paletteBodyView.append(paletteContainer);

        // 비교 연산자 data 할당 
        for (var i = 0; i < btnDomArray.length; i++) {
            (function(j){
                flexRow.append(btnDomArray[j]);

                // 버튼 클릭 
                $(importPackageThis.wrapSelector(`.vp-pythonCom-palletteBlock-func-btn-${j}`)).click(function() {
                    var newData = { type: "CONDITION_OPERATOR"
                                    , data: $(this).val()
                                    , indentSpaceNum: 0
                                }  
                    clickPaletteConfirmButton(pythonComPageRendererThis, newData);
                });
              
            })(i);
        }

        //bind back Button
        bindClickBackButton(pythonComPageRendererThis, uuid);
    }

    return renderConditionOperatorPalleteBlock;
});
