define ([
    // 기본 
    'require'
    , './helperFunc'
], function ( requirejs, helperFunc ) {
    var { bindCodeLineEventFunc } = helperFunc;
    var renderCommonFunctionCodeLine = function(pythonComPageRendererThis, index) {

        var currIndentSpaceStr = pythonComPageRendererThis.getCurrIndentSpaceStr();   
        var codeLineViewDom = pythonComPageRendererThis.getCodeLineViewDom();
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var codeLineArray = pythonComStateGenerator.getState('codeLineArray');
        
        var data = codeLineArray[index].data 
                    ? codeLineArray[index].data 
                    : "";
        var block = $(`<div class="vp-pythonCom-line vp-pythonCom-line-${index + 1} vp-pythonCom-style-flex-row-between">
                            
                            <div class="vp-pythonCom-style-flex-row">
                                <span class="vp-pythonCom-style-flex-column-center"
                                      style="white-space: break-spaces;">Line ${index + 1} : ${currIndentSpaceStr}</span>
                                <span class="vp-pythonCom-style-flex-column-center"
                                      style="margin-right:5px;"> ${data} </span>
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
        codeLineViewDom.append(block);   
        bindCodeLineEventFunc(pythonComPageRendererThis,index);      
    }
    return renderCommonFunctionCodeLine;

});
