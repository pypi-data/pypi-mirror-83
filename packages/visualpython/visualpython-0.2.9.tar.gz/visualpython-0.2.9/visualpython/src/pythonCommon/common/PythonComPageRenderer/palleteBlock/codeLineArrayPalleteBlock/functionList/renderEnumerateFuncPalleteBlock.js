
define ([
    // 기본 
    'require'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpCommon'

], function (requirejs, vpConst, vpCommon ) {

    /** EnumerateFuncPalleteBlock 동적 렌더링
     * @param { pythonComPageRenderer prototype this} pythonComPageRendererThis  
     */
    var renderEnumerateFuncPalleteBlock = function(pythonComPageRendererThis) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        // 배열의 인덱스는 길이보다 1 작다
        var currLineIndex = pythonComStateGenerator.getState(`currLineNumber`) - 1;   
        var codeLineArray = pythonComStateGenerator.getState('codeLineArray');
        var codeLineData = codeLineArray[currLineIndex].data;
        var codeLineType = codeLineArray[currLineIndex].type;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();

        var newMapFuncIdToPythonComFuncDataFunction = pythonComPageRendererThis.getNewMapFuncIdToPythonComFuncDataFunction()
        // // Python Common 패키지 Code Line 클래스 import
        var { pythonComCodeGenerator: pythonComCodeLineCodeGenerator
            , pythonComCodeValidator: pythonComCodeLineValidator
            , pythonComPageRenderer: pythonComCodeLinePageRenderer
            , pythonComStateGenerator: pythonComCodeLineStateGenerator } = newMapFuncIdToPythonComFuncDataFunction("JY404");

        // if(codeLineType === type) {
            pythonComCodeLineStateGenerator.setState({
                paramList:[
                    {type:"COMMON_FUNCTION", data:"enumerate([0])"}
                ]
            });
        // }

        var uuid = pythonComPageRendererThis.getOptionPageUUID();
        var paletteView = pythonComPageRendererThis.getPaletteBodyView();
        paletteView.empty();

        var { paletteContainer, paletteConfirmButton } 
            = pythonComPageRendererThis._renderSelectCodeLineTokenBlockAndConfirmButton(`Enumerate()`,uuid);

        var subPaletteView = $(`<div class="vp-pythonCom-subPalette-enumerate-view-body"></div>`);
        paletteContainer.append(subPaletteView);
        paletteContainer.append(paletteConfirmButton);
        paletteView.append(paletteContainer);

        // Python Common 패키지 Make Variable(변수 생성) 렌더링
        pythonComCodeLinePageRenderer.setImportPackageThis(importPackageThis);
        pythonComCodeLinePageRenderer.pageRender(`.vp-pythonCom-subPalette-enumerate-view-body`);

        $(importPackageThis.wrapSelector(`.vp-pythonCom-func-confirm-btn-${uuid}`)).click(function() {

            // validation 검사
            var state = pythonComCodeLinePageRenderer.pythonComStateGenerator.getStateAll();
            if (! pythonComCodeLineValidator.validate(state)) return;

            var newData = {
                type: "CUSTOM_CODE_LINE"
                , data: pythonComCodeLineStateGenerator.getState('paramList')
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
    return renderEnumerateFuncPalleteBlock;
});
