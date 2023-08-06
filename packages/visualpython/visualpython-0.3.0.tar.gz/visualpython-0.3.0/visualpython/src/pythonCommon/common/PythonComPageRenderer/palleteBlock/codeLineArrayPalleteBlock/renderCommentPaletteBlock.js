
define ([
    // 기본 
    'require'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpCommon'

], function (requirejs, vpConst, vpCommon ) {
    /** renderConditionOperatorPalleteBlock
     *  비교 연산자를 생성하기 위한 token을  Pallete View 동적 렌더링
     *  @param { pythonComPageRenderer this } pythonComPageRendererThis 
     *  @param { string } type
     */
    var renderCommentPaletteBlock = function(pythonComPageRendererThis, type) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        // 배열의 인덱스는 길이보다 1 작다
        var currLineIndex = pythonComStateGenerator.getState(`currLineNumber`) - 1;   
        var codeLineArray = pythonComStateGenerator.getState('codeLineArray');
        var codeLineData = codeLineArray[currLineIndex].data;
        var codeLineType = codeLineArray[currLineIndex].type;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();

        var newMapFuncIdToPythonComFuncDataFunction = pythonComPageRendererThis.getNewMapFuncIdToPythonComFuncDataFunction()
        // // Python Common 패키지 Make Variable(변수 생성) 클래스 import
        var { pythonComCodeGenerator: pythonComCommentCodeGenerator
            , pythonComCodeValidator: pythonComCommentValidator
            , pythonComPageRenderer: pythonComCommentPageRenderer
            , pythonComStateGenerator: pythonComCommentStateGenerator } = newMapFuncIdToPythonComFuncDataFunction("JY409");
        
        /** 
         * PaletteBlock이 렌더링 되었는데, type이 COMMENT 타입이면 데이터를 함께 렌더링한다
         */
        if(codeLineType === type) {
            pythonComCommentStateGenerator.setState({
                comment: codeLineData
            });
        }

        var uuid = pythonComPageRendererThis.getOptionPageUUID();
        var paletteView = pythonComPageRendererThis.getPaletteBodyView();
        paletteView.empty();

        var { paletteContainer, paletteConfirmButton } 
            = pythonComPageRendererThis._renderSelectCodeLineTokenBlockAndConfirmButton(`Edit Comment Line ${currLineIndex + 1}`,uuid);
        pythonComPageRendererThis.setGenerateCodeButton(paletteConfirmButton, currLineIndex + 1);
        
        var subPaletteView = $(`<div class="vp-pythonCom-subPalette-range-view-body"></div>`);
        paletteContainer.append(subPaletteView);
        paletteContainer.append(paletteConfirmButton);
        paletteView.append(paletteContainer);

        /** Python Common 패키지 Comment 렌더링 */
        pythonComCommentPageRenderer.setImportPackageThis(importPackageThis);
        pythonComCommentPageRenderer.pageRender(`.vp-pythonCom-subPalette-range-view-body`);

        /**  Code Line 생성 클릭 */
        $(importPackageThis.wrapSelector(`.vp-pythonCom-func-confirm-btn-${uuid}`)).click(function() {

            // validation 검사
            var state = pythonComCommentStateGenerator.getStateAll();
            if (! pythonComCommentValidator.validate(state)) return;

            // 코드 생성
            pythonComCommentCodeGenerator.makeCode();
            var newData = {
                type: "COMMENT"
                , data: pythonComCommentCodeGenerator.getCodeAndClear()
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

        // back 버튼 클릭
        $(importPackageThis.wrapSelector(`.vp-pythonCom-func-back-btn-${uuid}`)).click(function() {
            pythonComPageRendererThis.renderSelectPaletteButtonView();
        });
    };
    return renderCommentPaletteBlock;
});
