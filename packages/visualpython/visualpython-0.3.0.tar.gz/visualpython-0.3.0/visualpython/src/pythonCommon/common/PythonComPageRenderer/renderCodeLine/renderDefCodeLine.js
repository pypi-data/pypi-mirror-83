define ([
    // 기본 
    'require'
    , './helperFunc'
], function ( requirejs, helperFunc ) {
    var { bindCodeLineEventFunc, mapDefParamListToStr } = helperFunc;

    var renderDefCodeLine = function(pythonComPageRendererThis, index) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var codeLineArray = pythonComStateGenerator.getState(`codeLineArray`);
        var codeLineViewDom = pythonComPageRendererThis.getCodeLineViewDom();

        var inputFuncName = ( codeLineArray[index].data && codeLineArray[index].data.name ) 
                                ? codeLineArray[index].data.name 
                                : "";
        var inputParameterStr = ( codeLineArray[index].data && codeLineArray[index].data.paramList ) 
                                    ? mapDefParamListToStr(codeLineArray[index].type, codeLineArray[index].data.paramList)
                                    : "";
        var currIndentSpaceStr = pythonComPageRendererThis.getCurrIndentSpaceStr();                         
        var defBlock = $(`<div class="vp-pythonCom-line vp-pythonCom-line-${index + 1} vp-pythonCom-style-flex-row-between">
                           
                            <div class="vp-pythonCom-style-flex-row">
                                <span class="vp-pythonCom-style-flex-column-center"
                                    style="white-space: break-spaces;">Line ${index + 1} : ${currIndentSpaceStr}</span>
                                <strong class="vp-pythonCom-style-flex-column-center"
                                        style="margin-right:5px;">def </strong>
                                <span class="vp-multilang vp-pythonCom-style-flex-column-center" 
                                      style="margin-right:5px;"
                                      data-caption-id="${inputFuncName}"> ${inputFuncName}</span>
                                <span class="vp-multilang vp-pythonCom-style-flex-column-center" 
                                      style="margin-right:5px;"
                                      data-caption-id="${inputParameterStr}"> ${inputParameterStr} </span>
                                <span class="vp-multilang vp-pythonCom-style-flex-column-center" 
                                      style="margin-right:5px;"
                                      data-caption-id=":">
                                    <strong>:</strong>
                                </span>
                            </div>

                            <div class="vp-pythonCom-style-flex-row-end">
                                <button class="vp-pythonCom-func-btn vp-pythonCom-line-insertPalette-func-btn-${index + 1}"> 
                                    <span class="vp-multilang" data-caption-id="Insert_Palette"> Insert </span>
                                </button> 
                                <button class="vp-pythonCom-func-btn vp-pythonCom-line-indentSpace-plus-func-btn-${index + 1}"> +</button>
                                <button class="vp-pythonCom-func-btn vp-pythonCom-line-indentSpace-minus-func-btn-${index + 1}"> -</button>
                                <button class="vp-pythonCom-func-btn vp-pythonCom-line-up-func-btn-${index + 1}"> ▲</button> 
                                <button class="vp-pythonCom-func-btn vp-pythonCom-line-down-func-btn-${index + 1}"> ▼</button> 
                                <button class="vp-pythonCom-func-btn vp-pythonCom-line-delete-func-btn-${index + 1}"> X</button> 
                            </div>
                        </div>`);

        codeLineViewDom.append(defBlock);  
        bindCodeLineEventFunc(pythonComPageRendererThis,index);    
    }

    return renderDefCodeLine;
});
