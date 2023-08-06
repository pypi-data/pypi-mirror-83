define ([
    // 기본 
    'require'
    , './helperFunc'
], function ( requirejs, helperFunc ) {
    var { bindCodeLineEventFunc, mapParamListToStr, mapCodeLineDataToStr } = helperFunc;

    var renderForCodeLine = function(pythonComPageRendererThis, index) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var currIndentSpaceStr = pythonComPageRendererThis.getCurrIndentSpaceStr(); 
        var codeLineViewDom = pythonComPageRendererThis.getCodeLineViewDom();  
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var codeLineArray = pythonComStateGenerator.getState(`codeLineArray`);

        var indexValueList = mapParamListToStr(codeLineArray[index].data.indexValueList) || `( 인덱스 값 )`;
        var iterableObjData = mapCodeLineDataToStr(codeLineArray[index].data.iterableObjData) || `( 이터러블 객체 )`;
        var operator = codeLineArray[index].data.operator || `( 연산자 )`;
        var defBlock = $(`<div class="vp-pythonCom-line vp-pythonCom-line-${index + 1} vp-pythonCom-style-flex-row-between">
                            
                            <div class="vp-pythonCom-style-flex-row">
                                <span class="vp-pythonCom-style-flex-column-center"
                                    style="white-space: break-spaces;">Line ${index + 1} : ${currIndentSpaceStr}</span>
                                <strong class="vp-pythonCom-style-flex-column-center"
                                        style="margin-right:5px;">for </strong>
                                <span class="vp-pythonCom-style-flex-column-center"
                                        style="margin-right:5px;"> ${indexValueList} </span>
                                <span class="vp-pythonCom-style-flex-column-center"
                                        style="margin-right:5px;"> ${operator} </span>
                                <span class="vp-pythonCom-style-flex-column-center"
                                      style="margin-right:5px;"> ${iterableObjData} </span>
                                <span class="vp-pythonCom-style-flex-column-center"
                                      style="margin-right:5px;"> : </span>
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

    return renderForCodeLine;
});
