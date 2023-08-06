define ([
    // 기본 
    'require'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpCommon'

], function (requirejs, vpConst, vpCommon ) {
    /**
     * renderForPaletteBlock
     * for Palette 동적 렌더링
     * @param {pythonComPageRenderer This} pythonComPageRendererThis 
     * @param {string} type
     */
    var renderForPaletteBlock = function(pythonComPageRendererThis, type ) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var currLineIndex = pythonComStateGenerator.getState(`currLineNumber`) - 1;   
        var codeLineArray = pythonComStateGenerator.getState('codeLineArray');
        var codeLineData = codeLineArray[currLineIndex].data;
        var codeLineType = codeLineArray[currLineIndex].type;
        var { indexValueList, operator ,iterableObjData } = codeLineData;

        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        var uuid = pythonComPageRendererThis.getOptionPageUUID();
        var paletteView = pythonComPageRendererThis.getPaletteBodyView();
        paletteView.empty();

        var newMapFuncIdToPythonComFuncDataFunction = pythonComPageRendererThis.getNewMapFuncIdToPythonComFuncDataFunction()
        /** Python Common 패키지 Code Line(변수 생성) 클래스 import */
        var { pythonComCodeGenerator: pythonComCodeLineCodeGenerator
            , pythonComCodeValidator: pythonComCodeLineValidator
            , pythonComPageRenderer: pythonComCodeLinePageRenderer
            , pythonComStateGenerator: pythonComCodeLineStateGenerator} = newMapFuncIdToPythonComFuncDataFunction("JY404");
        
        /** 
         * PaletteBlock이 렌더링 되었는데, type이 FOR 타입이면 데이터를 함께 렌더링한다
         */
        if(codeLineType === type) { 
            pythonComStateGenerator.setState({
                forIndexValueList: indexValueList,
                forOperator : operator
            }); 
            pythonComCodeLineStateGenerator.setState({
                paramList:[
                    ...iterableObjData
                ]
            });
        }

        // Python Common 패키지 Make Variable(변수 생성) 렌더링
        pythonComCodeLinePageRenderer.setImportPackageThis(importPackageThis);

        // pallete container 렌더링

        var { paletteContainer: tokenContainer, 
              paletteConfirmButton: tokenConfirmButton } 
              = pythonComPageRendererThis._renderSelectCodeLineTokenBlockAndConfirmButton(`Edit FOR Line : ${currLineIndex + 1}`,uuid);
        pythonComCodeLinePageRenderer.setGenerateCodeButton(tokenConfirmButton, currLineIndex + 1);
        

        /** for 블럭 첫번째 블럭 렌더링 */
        var indexListViewBlock = pythonComPageRendererThis._renderPythonComBlockAppendToDom(tokenContainer, `Input IndexList`);
        
        /** for 두번째 블럭 렌더링 */
        var forConditionOperatorViewBlock = pythonComPageRendererThis._renderPythonComBlockAppendToDom(tokenContainer, `Select Operator`);
        var selectBlock = $(`<div>
                                <select class="vp-pythonCom-select-dtype" id="vp_pythonCom-select-${uuid}">
                                </select>
                             </div>`);

        forConditionOperatorViewBlock.append(selectBlock);


        // 세번째 블럭 렌더링
        var iterableBlock = $(`<div class="vp-pythonCom-style-flex-column 
                                         vp-pythonCom-subPalette-view-body"></div>`);
        tokenContainer.append(iterableBlock);
        tokenContainer.append(tokenConfirmButton);
        paletteView.append(tokenContainer);

        var forOperatorArray = ["in", "not in"];
        forOperatorArray.forEach(function (element) {
            $(importPackageThis.wrapSelector(`#vp_pythonCom-select-${uuid}`)).append(`<option value="${element}"> ${element}</option>`)
        });

        // 첫번째 블럭에 IndexValueEditor 렌더링
        pythonComPageRendererThis._renderParamOneArrayIndexValueEditor(indexListViewBlock,'forIndexValueList');
        // 세번째 블럭에 CodeLinePageRender 렌더링
        pythonComCodeLinePageRenderer.pageRender(`.vp-pythonCom-subPalette-view-body`, "Input Iterable Object");
        

        $(importPackageThis.wrapSelector(`#vp_pythonCom-select-${uuid}`)).change(function()  {
            pythonComStateGenerator.setState({
                forOperator : $(':selected', this).val()
            });
        });

        /** Line view에 For문 작성 완료 클릭  */
        $(importPackageThis.wrapSelector(`.vp-pythonCom-func-confirm-btn-${uuid}`)).click(function() {
            // validation 검사
            var state = pythonComCodeLineStateGenerator.getStateAll();
            if (! pythonComCodeLineValidator.validate(state)) return;

            // 배열의 인덱스는 길이보다 1 작다
            // var currLineIndex = pythonComStateGenerator.getState(`currLineNumber`) - 1;             
            // var codeLineArray = pythonComStateGenerator.getState(`codeLineArray`);
            var newData = { type: "FOR" 
                            , data:{ 
                                indexValueList: pythonComStateGenerator.getState(`forIndexValueList`),
                                operator: pythonComStateGenerator.getState(`forOperator`),
                                iterableObjData: pythonComCodeLineStateGenerator.getState(`paramList`)
                            }
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
    }
    return renderForPaletteBlock;
});
