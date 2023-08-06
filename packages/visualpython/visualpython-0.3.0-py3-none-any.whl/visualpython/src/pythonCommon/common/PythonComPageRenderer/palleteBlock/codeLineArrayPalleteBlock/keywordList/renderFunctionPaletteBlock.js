define ([
    // 기본 
    'require'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpCommon'
    // + 추가 python common 폴더 패키지 : 이진용 주임

], function (requirejs, vpConst, vpCommon) {

    var renderFunctionPaletteBlock = function(pythonComPageRendererThis, type) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        var currLineIndex = pythonComStateGenerator.getState(`currLineNumber`) - 1;   
        var codeLineArray = pythonComStateGenerator.getState('codeLineArray');
        var codeLineData = codeLineArray[currLineIndex].data;
        var codeLineType = codeLineArray[currLineIndex].type;

        /** 
         * PaletteBlock이 렌더링 되었는데, type이 FUNCTION 타입이면 데이터를 함께 렌더링한다
         */
        if(codeLineType === type) { 
            pythonComStateGenerator.setState({
                defName: codeLineData.name,
                defParamList: codeLineData.paramList
            });
        }
        
        var uuid = vpCommon.getUUID();
        
        var defType = `DEF`;

        var paletteView = pythonComPageRendererThis.getPaletteBodyView();
        paletteView.empty();

        var subPaletteView = $(`<div class=" vp-pythonCom-subPalette-view-body"></div>`);

        var defNameViewBlock = pythonComPageRendererThis._renderPythonComBlockAppendToDom(subPaletteView,`Input Def Name`);
        var buttonContainer = $(`<div class="vp-pythonCom-style-flex-row"></div>`);

        var nameInput = $(`<div class="vp-pythonCom-style-flex-row
                                        vp-pythonCom-style-margin-top-10px">
                                <span class=" vp-multilang
                                            vp-pythonCom-style-flex-column-center
                                            vp-pythonCom-style-margin-right-5px" data-caption-id="name"> 
                                    <strong>Name : </strong>
                                </span>
                                <input class="vp-pythonCom-input-def-name-${uuid}"
                                       value="${codeLineData.name}"
                                       type="text">
                            </div>`);
        var defOptionBtn1 = $(`<button class="vp-pythonCom-func-btn 
                                              vp-pythonCom-def-btn-${uuid}
                                              vp-pythonCom-def-btn-1-${uuid}
                                              vp-pythonCom-selected" 
                                            style="width:100%;">
                                        <span class="vp-multilang" data-caption-id="Input_Name"> 
                                        Input Name
                                        </span>
                                    </button>`);

        var defOptionBtn2 = $(`<button class="vp-pythonCom-func-btn 
                                              vp-pythonCom-def-btn-${uuid}
                                              vp-pythonCom-def-btn-2-${uuid}" 
                                            style="width:100%;"
                                        value="__init__">
                                        <span class="vp-multilang" data-caption-id="__init__"> 
                                        __init__
                                        </span>
                                    </button>`);

        var defOptionBtn3 = $(`<button class="vp-pythonCom-func-btn 
                                            vp-pythonCom-def-btn-${uuid}
                                            vp-pythonCom-def-btn-3-${uuid}" 
                                        style="width:100%;"
                                        value="__del__">
                                        <span class="vp-multilang" data-caption-id="__del__"> 
                                        __del__
                                        </span>
                                    </button>`);
                       
        // defOption 3개의 버튼 클릭시
        var btnArray = [ defOptionBtn1, defOptionBtn2, defOptionBtn3 ];   
        btnArray.forEach(function(btn){
            buttonContainer.append(btn);
        });
        for(var i = 0; i < btnArray.length; i++) {
            ( function(j) {
                btnArray[j].click(function() {
                    $(this).removeClass("vp-pythonCom-selected");
                    if ($(this).hasClass("vp-pythonCom-selected")){
                        $(this).removeClass("vp-pythonCom-selected");
                    } else {
                        $(this).addClass("vp-pythonCom-selected");
                    }
                    switch(j){
                        case 0:{
                            $(importPackageThis.wrapSelector(`.vp-pythonCom-input-def-name-${uuid}`)).val(``);
                            $(importPackageThis.wrapSelector(`.vp-pythonCom-input-def-name-${uuid}`)).attr("disabled",false); 
                            $(importPackageThis.wrapSelector('.vp-pythonCom-self-input-container')).css("display","none");
                            defType = "DEF";
                            break; 
                        }
                        case 1:{
                            $(importPackageThis.wrapSelector(`.vp-pythonCom-input-def-name-${uuid}`)).val(`__init__`);
                            $(importPackageThis.wrapSelector(`.vp-pythonCom-input-def-name-${uuid}`)).attr("disabled",true); 
                            $(importPackageThis.wrapSelector('.vp-pythonCom-self-input-container')).css("display","flex");
                            pythonComStateGenerator.setState({
                                defName: `__init__`
                            });
                            defType = "DEF_INIT";
                            break; 
                        }
                        case 2:{
                            $(importPackageThis.wrapSelector(`.vp-pythonCom-input-def-name-${uuid}`)).val(`__del__`);
                            $(importPackageThis.wrapSelector(`.vp-pythonCom-input-def-name-${uuid}`)).attr("disabled",true); 
                            $(importPackageThis.wrapSelector('.vp-pythonCom-self-input-container')).css("display","flex");
                            pythonComStateGenerator.setState({
                                defName: `__del__`
                            });
                            defType = "DEF_DEL";
                            break; 
                        }
                        default:{
                            break;
                        }
                    }
                });
            })(i);
        }

        // 첫번째 블록 defNameBlock 렌더링
        defNameViewBlock.append(buttonContainer);
        defNameViewBlock.append(nameInput);
   
        // 두번째 블록 paramListBlock 렌더링
        var paramListBlockView = pythonComPageRendererThis._renderPythonComBlockAppendToDom(subPaletteView,`Input ParamList`);
        var selfInput = $(`<div class="vp-pythonCom-self-input-container flex-row"
                                style="display:none">
                                <div class="flex-column-center margin-right-5px font-weight-700">
                                    param 0 : 
                                </div> 
                                <input class="vp-numpy-input" disabled
                                        value="self" type="text" placeholder="input param 0">
                                </input>
                        </div>`);
        paramListBlockView.append(selfInput);
        var paramListBlock = $(`<div class="vp-pythonCom-style-flex-column "></div>`);
        paramListBlockView.append(paramListBlock);

        // paletteContainer가 첫번째 블록 defNameBlock 두번째 블록 paramListBlock을 append
        var { paletteContainer, paletteConfirmButton } 
        = pythonComPageRendererThis._renderSelectCodeLineTokenBlockAndConfirmButton(`Edit DEF Line : ${currLineIndex + 1}`,uuid);
        pythonComPageRendererThis.setGenerateCodeButton(paletteConfirmButton, currLineIndex + 1);

        paletteContainer.append(subPaletteView);
        paletteContainer.append(paletteConfirmButton);
        paletteView.append(paletteContainer);

        pythonComPageRendererThis._renderParamOneArrayIndexValueEditor(paramListBlock,'defParamList');

        if(codeLineType == "DEF_DEL" || codeLineType == "DEF_INIT"){
            $(importPackageThis.wrapSelector(`.vp-pythonCom-input-def-name-${uuid}`)).attr("disabled", true); 
            $(importPackageThis.wrapSelector('.vp-pythonCom-self-input-container')).css("display","flex");
        }

        $(importPackageThis.wrapSelector(`.vp-pythonCom-input-def-name-${uuid}`)).on("change keyup paste", function() {
            pythonComStateGenerator.setState({
                defName: $(this).val()
            });
        });

        $(importPackageThis.wrapSelector(`.vp-pythonCom-func-confirm-btn-${uuid}`)).click(function() {
            // validation 검사

            var newData = {
                type: defType,
                data: {
                    name: pythonComStateGenerator.getState(`defName`)
                    , paramList: pythonComStateGenerator.getState(`defParamList`)
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

        $(importPackageThis.wrapSelector(`.vp-pythonCom-func-back-btn-${uuid}`)).click(function() {
            pythonComPageRendererThis.renderSelectPaletteButtonView();
        });
    };

    return renderFunctionPaletteBlock;
});
