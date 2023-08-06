define ([
    // 기본 
    'require'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpCommon'

], function (requirejs, vpConst, vpCommon) {
    "use strict";
 
    /** Class의 self 변수 렌더링
     * @param { pythonComPageRenderer This } pythonComPageRendererThis 
     * @param { string } type 
     */
    var renderClassSelfVariablePaletteBlock = function(pythonComPageRendererThis, type) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        // 배열의 인덱스는 길이보다 1 작다
        var currLineIndex = pythonComStateGenerator.getState(`currLineNumber`) - 1;   
        var codeLineArray = pythonComStateGenerator.getState('codeLineArray');
        var codeLineData = codeLineArray[currLineIndex].data;
        var codeLineType = codeLineArray[currLineIndex].type;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();

        var selfVariabledata = codeLineData;
        var uuid = vpCommon.getUUID();

        var paletteBodyView = pythonComPageRendererThis.getPaletteBodyView();
        paletteBodyView.empty();

        var { paletteContainer, paletteConfirmButton } 
                = pythonComPageRendererThis._renderSelectCodeLineTokenBlockAndConfirmButton(`SELF VARIABLE`,uuid);

        var flexRow = $(`<div class="vp-pythonCom-style-flex-row">
                            <div class="vp-pythonCom-style-flex-column-center">
                                <span style="font-size:17px;">self.${selfVariabledata}</span>
                            </div>
                        </div>`);
        var input = $(`<input type="text"
                              value="${selfVariabledata}"/>`);
        flexRow.append(input);
        paletteContainer.append(flexRow);
        paletteContainer.append(paletteConfirmButton);
        paletteBodyView.append(paletteContainer);

        /** 변수 입력 input */
        $(input).on("change keyup paste", function() {
            selfVariabledata = $(this).val();
        });

        /** SELF VARIABLE 생성 */
        $(importPackageThis.wrapSelector(`.vp-pythonCom-func-confirm-btn-${uuid}`)).click(function() {
            var newData = {
                type: "SELF_VARIABLE"
                , data: selfVariabledata
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
    }

    return renderClassSelfVariablePaletteBlock;
});