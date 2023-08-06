define ([
    // 기본 
    'require'
    , './helperFunc'
], function ( requirejs, helperFunc ) {
    var { bindCodeLineEventFunc } = helperFunc;
    var renderBreakContinueElseElifCodeLine = function(pythonComPageRendererThis, index, typeEnum) {
        var currIndentSpaceStr = pythonComPageRendererThis.getCurrIndentSpaceStr();   
        var codeLineViewDom = pythonComPageRendererThis.getCodeLineViewDom();
        // var pythonComConstData = pythonComPageRendererThis.getPythonComConstData();
        // var { PYTHON_COMMON_GENERATE_CODE_LINE_ENUM } = pythonComConstData;
        // var { CLASS_TYPE, DEF_TYPE, FOR_TYPE, IF_TYPE, WHILE_TYPE, ELIF_TYPE,
        //       ELSE_TYPE, MAKE_VARIABLE_TYPE, BREAK_TYPE, CONTINUE_TYPE } = PYTHON_COMMON_GENERATE_CODE_LINE_ENUM;
        var title = ``;

        switch(typeEnum){
            case  "BREAK": {
                title = `Break`;
      
                break;
            }
            case "CONTINUE" : {
                title = `Continue`;
          
                break;
            }
            case "ELSE": {
                title = `else`;
    
                break;
            }

            default: {
                break;
            }
        }

        var defBlock = $(`<div class="vp-pythonCom-line vp-pythonCom-line-${index + 1} vp-pythonCom-style-flex-row-between">
                        
                            <div class="vp-pythonCom-style-flex-row">
                                <span class="vp-pythonCom-style-flex-column-center"
                                    style="white-space: break-spaces;">Line ${index + 1} : ${currIndentSpaceStr}</span>
                                <strong class="vp-pythonCom-style-flex-column-center"
                                        style="margin-right:5px;">${title} </strong>
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
    return renderBreakContinueElseElifCodeLine;

});
