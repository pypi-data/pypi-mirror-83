define ([
    // 기본 
    'require'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpCommon'


], function (requirejs, vpConst, vpCommon) {
    /**
     * renderBreakContinueElsePaletteBlock
     * Break 동적 렌더링
     * @param {pythonComPageRenderer This} pythonComPageRendererThis 
     * @param {string} typeEnum 
     */
    var renderBreakContinueElsePaletteBlock = function(pythonComPageRendererThis, typeEnum) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();

        var uuid = vpCommon.getUUID();
        var title = ``;
        var data = ``;
        var type = ``;
        switch(typeEnum){
            case "BREAK": {
                title = `break`;
                data = `break`;
                type = `BREAK`;
                break;
            }
            case "CONTINUE": {
                title = `continue`;
                data = `continue`;
                type = `CONTINUE`;
                break;
            }
            case "ELSE": {
                title = `else`;
                data = `else`;
                type = `ELSE`;
                break;
            }
            default: {
                break;
            }
        }
        
        // 배열의 인덱스는 길이보다 1 작다
        var currLineIndex = pythonComStateGenerator.getState(`currLineNumber`) - 1;             
        var codeLineArray = pythonComStateGenerator.getState(`codeLineArray`);
        var paletteView =  pythonComPageRendererThis.getPaletteBodyView();
        paletteView.empty();

        /**
         * 컨테이너와 
         * Code Line을 생성하는 버튼 생성
         */
        var { paletteContainer, paletteConfirmButton } 
                = pythonComPageRendererThis._renderSelectCodeLineTokenBlockAndConfirmButton(title, uuid);
        pythonComPageRendererThis.setGenerateCodeButton(paletteConfirmButton, currLineIndex + 1);
        paletteContainer.append(paletteConfirmButton);
        paletteView.append(paletteContainer);

        /** break or continue or else 문 작성 완료 클릭 
         */
        $(importPackageThis.wrapSelector(`.vp-pythonCom-func-confirm-btn-${uuid}`)).click(function() {
            var newData = { type: type,
                            data: data, 
                            indentSpaceNum: codeLineArray[currLineIndex].indentSpaceNum
            }
            var newCodeLineArray = pythonComStateGenerator.updateOneArrayIndexValueAndGetNewArray(codeLineArray, 
                                                                                                  currLineIndex, 
                                                                                                  newData);
            pythonComStateGenerator.setState({
                codeLineArray: newCodeLineArray
            });   
            pythonComPageRendererThis.renderCodeLine();
        });

        // back 버튼 클릭
        $(importPackageThis.wrapSelector(`.vp-pythonCom-func-back-btn-${uuid}`)).click(function() {
            pythonComPageRendererThis.renderSelectPaletteButtonView();
        });
    }

    return renderBreakContinueElsePaletteBlock;
});
