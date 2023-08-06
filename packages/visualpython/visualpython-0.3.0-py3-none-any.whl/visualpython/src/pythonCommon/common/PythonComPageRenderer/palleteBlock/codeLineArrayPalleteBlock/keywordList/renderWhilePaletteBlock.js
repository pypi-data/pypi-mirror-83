
define ([
    // 기본 
    'require'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpCommon'

], function (requirejs, vpConst, vpCommon) {

    var renderWhilePaletteBlock = function(pythonComPageRendererThis, type) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        // 배열의 인덱스는 길이보다 1 작다
        var currLineIndex = pythonComStateGenerator.getState(`currLineNumber`) - 1;   
        var codeLineArray = pythonComStateGenerator.getState('codeLineArray');
        var codeLineData = codeLineArray[currLineIndex].data;
        var codeLineType = codeLineArray[currLineIndex].type;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        
        var newMapFuncIdToPythonComFuncDataFunction = pythonComPageRendererThis.getNewMapFuncIdToPythonComFuncDataFunction()
        /** Python Common 패키지 Code Line import */ 
        var {  pythonComCodeValidator: pythonComCodeLineValidator
              , pythonComPageRenderer: pythonComCodeLinePageRenderer 
              , pythonComStateGenerator: pythonComCodeLineStateGenerator} = newMapFuncIdToPythonComFuncDataFunction("JY404");
        
        /** 
         * PaletteBlock이 렌더링 되었는데, type이 WHILE 타입이면 데이터를 함께 렌더링한다
         */
        if(codeLineType === type) {
            pythonComCodeLineStateGenerator.setState({
                paramList:[
                    ...codeLineData
                ]
            });
        }

        var uuid = pythonComPageRendererThis.getOptionPageUUID();
        var paletteView = pythonComPageRendererThis.getPaletteBodyView();
        paletteView.empty();

        var { paletteContainer: tokenContainer, 
            paletteConfirmButton: tokenConfirmButton } 
         = pythonComPageRendererThis._renderSelectCodeLineTokenBlockAndConfirmButton(`Edit WHILE Line : ${currLineIndex + 1}`,uuid);
         pythonComCodeLinePageRenderer.setGenerateCodeButton(tokenConfirmButton, currLineIndex + 1);

        var subPaletteView = $(`<div class="vp-pythonCom-subPalette-while-view-body"></div>`);
        tokenContainer.append(subPaletteView);
        tokenContainer.append(tokenConfirmButton);
        paletteView.append(tokenContainer);



        // Python Common 패키지 Make Variable(변수 생성) 렌더링
        pythonComCodeLinePageRenderer.setImportPackageThis(importPackageThis);
        pythonComCodeLinePageRenderer.pageRender(`.vp-pythonCom-subPalette-while-view-body`, "Generate While문");

        $(importPackageThis.wrapSelector(`.vp-pythonCom-func-confirm-btn-${uuid}`)).click(function() {

            // validation 검사
            var state = pythonComCodeLineStateGenerator.getStateAll();
            if (! pythonComCodeLineValidator.validate(state)) return;

     
            var newData = {
                type: "WHILE"
                , data: pythonComCodeLineStateGenerator.getState(`paramList`)
                , indentSpaceNum: codeLineArray[currLineIndex].indentSpaceNum
            }

            var newCodeLineArray = pythonComStateGenerator.updateOneArrayIndexValueAndGetNewArray(codeLineArray, 
                                                                                                  currLineIndex, 
                                                                                                  newData);
            pythonComStateGenerator.setState({
                codeLineArray: newCodeLineArray
            });   
            pythonComPageRendererThis.renderCodeLine();
            pythonComPageRendererThis.renderPaletteView();
        });

        $(importPackageThis.wrapSelector(`.vp-pythonCom-func-back-btn-${uuid}`)).click(function() {
            pythonComPageRendererThis.renderSelectPaletteButtonView();
        });
    };
    return renderWhilePaletteBlock;
});
