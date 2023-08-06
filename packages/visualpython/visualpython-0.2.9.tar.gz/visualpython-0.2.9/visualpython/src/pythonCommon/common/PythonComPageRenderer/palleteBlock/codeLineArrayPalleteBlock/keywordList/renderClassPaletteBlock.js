
define ([
    // 기본 
    'require'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpCommon'

], function (requirejs, vpConst, vpCommon){
    /**
     * renderClassPaletteBlock
     * class Palette 동적 렌더링
     * @param {pythonComPageRenderer This} pythonComPageRendererThis 
     * @param {string} type
     */
    var renderClassPaletteBlock = function(pythonComPageRendererThis, type) {
        /**
         * 렌더링에 필요한 기본 데이터 불러오기
         */
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        var currLineIndex = pythonComStateGenerator.getState(`currLineNumber`) - 1;   
        var codeLineArray = pythonComStateGenerator.getState('codeLineArray');
        var codeLineData = codeLineArray[currLineIndex].data;
        var codeLineType = codeLineArray[currLineIndex].type;
        
        /** 
         * PaletteBlock이 렌더링 되었는데, type이 SELF_VARIABLE 타입이면 데이터를 함께 렌더링한다
         */
        if(codeLineType === type) { 
            pythonComStateGenerator.setState({
                className: codeLineData.name,
                classParamList: codeLineData.paramList
            });
        }

        var uuid = vpCommon.getUUID();
        
        var paletteView = pythonComPageRendererThis.getPaletteBodyView();
        paletteView.empty();

        /**
         * Edit CLASS컨테이너와 
         * Code Line을 생성하는 버튼 생성
         */
        var { paletteContainer, paletteConfirmButton } 
            = pythonComPageRendererThis._renderSelectCodeLineTokenBlockAndConfirmButton(`Edit CLASS Line : ${currLineIndex + 1}`,uuid);
        pythonComPageRendererThis.setGenerateCodeButton(paletteConfirmButton, currLineIndex + 1);
        
        var subPaletteView = $(`<div class="vp-pythonCom-subPalette-view-body"></div>`);
        /** 생성된 subPaletteView이 classNameViewBlock와 classParamViewBlock을 자식으로 append */
        var classNameViewBlock = pythonComPageRendererThis._renderPythonComBlockAppendToDom(subPaletteView,`Input Class Name`);
        var classParamViewBlock = pythonComPageRendererThis._renderPythonComBlockAppendToDom(subPaletteView,`Input Class Param`);
        var input = $(`<div>
                        <span class="vp-multilang" data-caption-id="name"> Name : </span>
                        <input id="vp_pythonCom-input-${uuid}" 
                               value="${codeLineData.name}"  
                               type="text">
                        </div>`)
  
        classNameViewBlock.append(input);
        paletteContainer.append(subPaletteView);
        paletteContainer.append(paletteConfirmButton);
        paletteView.append(paletteContainer);

        pythonComPageRendererThis._renderParamOneArrayIndexValueEditor(classParamViewBlock,'classParamList');
 
        /** 
         * class의 이름을 적는 이벤트 함수
         */
        $(importPackageThis.wrapSelector(`#vp_pythonCom-input-${uuid}`)).on("change keyup paste", function() {
            pythonComStateGenerator.setState({
                className : $(this).val()
            });
        });

        /** 
         *  class 데이터를 Code Line에 생성하는 이벤트 함수
         */
        $(importPackageThis.wrapSelector(`.vp-pythonCom-func-confirm-btn-${uuid}`)).click(function() {
            // 배열의 인덱스는 길이보다 1 작다
            var currLineIndex = pythonComStateGenerator.getState(`currLineNumber`) - 1;             
            var codeLineArray = pythonComStateGenerator.getState(`codeLineArray`);
            var newData = {
                type: "CLASS"
                , data: {
                    name: pythonComStateGenerator.getState(`className`)
                    , paramList: pythonComStateGenerator.getState(`classParamList`)
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

        // back 버튼 이벤트 함수 
        $(importPackageThis.wrapSelector(`.vp-pythonCom-func-back-btn-${uuid}`)).click(function() {
            pythonComPageRendererThis.renderSelectPaletteButtonView();
        });
    };
    return renderClassPaletteBlock;
});
