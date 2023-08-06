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
    var palleteBlockState = new PalleteBlockState();

    /** 산술 연산자를 생성하기 위한 token을 만드는 PalleteBlock 렌더링
     * @param {pythonComPageRenderer this} pythonComPageRendererThis 
     */
    var renderCalculationOperatorPaletteBlock = function(pythonComPageRendererThis) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();

        var uuid = vpCommon.getUUID();
        var paletteBodyView = pythonComPageRendererThis.getPaletteBodyView();
        paletteBodyView.empty();

        const { paletteContainer } = pythonComPageRendererThis._renderSelectCodeLineTokenBlockAndConfirmButton("산술 연산자", uuid);

        var flexRow = $(`<div class="vp-pythonCom-style-flex-row-evenly"> </div>`);

        var btnDataArray = [`+`, `-`, `*`, `/`, `**`, `%`];
        var btnDomArray = makeBtnDomArray(btnDataArray);


        paletteContainer.append(flexRow);
        paletteBodyView.append(paletteContainer);

        // 버튼 클릭 : data 할당 
        for (var i = 0; i < btnDomArray.length; i++) {
            (function(j){
                flexRow.append(btnDomArray[j]);
                $(importPackageThis.wrapSelector(`.vp-pythonCom-palletteBlock-func-btn-${j}`)).click(function() {
                    var newData = { type: "CALCULATION_OPERATOR"
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

    return renderCalculationOperatorPaletteBlock;
});
