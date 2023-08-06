define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    // numpy 패키지를 위한 라이브러리import 
    , 'nbextensions/visualpython/src/common/constant_pythonCommon'
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComPageRenderer/parent/PythonComPageRenderer'
    
    , '../renderCodeLine/index'
    , '../palleteBlock/index'
    , '../palleteButton/index'
], function( requirejs, vpCommon, 
             vpPythonCommonConst, PythonComPageRenderer,
             renderCodeLineList, palleteBlockList, palleteButtonList ) {
    "use strict";
    var {PYTHON_COMMON_RENDER_CODELINE_MAP } = renderCodeLineList;
    var { PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP } = palleteBlockList;
    var { renderCodeLineArrayPalleteButton  } = palleteButtonList;
    
    /**
     * @class PythonComCodeLineArrayPageRenderer
     * @constructor
    */

    var PythonComCodeLineArrayPageRenderer = function(pythonComOptionObj) {
        this.currIndentSpaceStr = ``;
        this.codeLineViewDom;
        
        this.codeLineTypeList = [ "CLASS", "DEF", "FOR", "IF", "WHILE", "CUSTOM_CODE_LINE" ,
                                    "RETURN", "BREAK", "CONTINUE", "ELIF", "ELSE",
                                    "PRINT_FUNC", "RANGE_FUNC", "ENUMERATE_FUNC", "COMMENT"  ];
        this.isOpenCodeLineArrayEditorModal = false;
        PythonComPageRenderer.call(this);
    };

    /**
     * PythonComPageRenderer 에서 상속
    */
    PythonComCodeLineArrayPageRenderer.prototype = Object.create(PythonComPageRenderer.prototype);

    PythonComCodeLineArrayPageRenderer.prototype.getCodeLineTypeList = function() {
        return this.codeLineTypeList;
    }

    PythonComCodeLineArrayPageRenderer.prototype.getCurrIndentSpaceStr = function() {
        return this.currIndentSpaceStr;
    }
    PythonComCodeLineArrayPageRenderer.prototype.setCurrIndentSpaceStr = function(currIndentSpaceStr) {
        this.currIndentSpaceStr = currIndentSpaceStr;
    }

    PythonComCodeLineArrayPageRenderer.prototype.getCodeLineViewDom = function() {
        return this.codeLineViewDom;
    }
    PythonComCodeLineArrayPageRenderer.prototype.setCodeLineViewDom = function(codeLineViewDom) {
        this.codeLineViewDom = codeLineViewDom;
    }

    PythonComCodeLineArrayPageRenderer.prototype.setPythonComMakeVariablePageRender = function(pythonComMakeVariablePageRender) {
        this.pythonComMakeVariablePageRender = pythonComMakeVariablePageRender;
    }

    PythonComCodeLineArrayPageRenderer.prototype.getPythonComMakeVariablePageRender = function() {
        return this.pythonComMakeVariablePageRender;
    }

    PythonComCodeLineArrayPageRenderer.prototype.setTrueIsOpenCodeLineArrayEditorModal = function() {
        this.isOpenCodeLineArrayEditorModal = true;
    }
    PythonComCodeLineArrayPageRenderer.prototype.setFalseIsOpenCodeLineArrayEditorModal = function() {
        this.isOpenCodeLineArrayEditorModal = false;
    }

    PythonComCodeLineArrayPageRenderer.prototype.getIsOpenCodeLineArrayEditorModal = function() {
        return this.isOpenCodeLineArrayEditorModal;
    }
    /**
    * PythonComPageRenderer 클래스의 pageRender 메소드 오버라이드
    * @param {string} tagSelector 
    */
    PythonComCodeLineArrayPageRenderer.prototype.pageRender = function(tagSelector) {
        var uuid = vpCommon.getUUID();
        var pythonComPageRendererThis = this;
        var importPackageThis = this.getImportPackageThis();
        var pythonComStateGenerator = this.getStateGenerator();

        pythonComPageRendererThis.setRootTagSelector(tagSelector || ".vp-pythonCom-block-view");
        var mRootTagSelector = pythonComPageRendererThis.getRootTagSelector();
        var rootTagDom = $(importPackageThis.wrapSelector(mRootTagSelector));
        rootTagDom.empty();
        
        pythonComPageRendererThis._renderCodeLineArrayViewBlock( `Edit Code Lines`, uuid); 
        var codeLineViewDom = $(importPackageThis.wrapSelector(`.vp-pythonCom-line-view-body-${uuid}`)); 
        this.setCodeLineViewDom(codeLineViewDom);
        codeLineViewDom.empty();

        var selectPaletteBodyView = pythonComPageRendererThis._renderPythonComBlockAnGetSelectedViewDom(`Select Pallete `);
        pythonComPageRendererThis.setPaletteBodyView(selectPaletteBodyView);

        this.renderCodeLine();

        // 이전 스택으로 이동
        $(importPackageThis.wrapSelector(`.vp-pythonCom-prevDirectory-func-btn`)).click(function(){
            pythonComStateGenerator.popCodeLineArrayStackAndSet();
            pythonComPageRendererThis.renderCodeLine();
            pythonComPageRendererThis.renderPaletteView();

            var currLineNumber = pythonComStateGenerator.getState(`currLineNumber`);
            pythonComPageRendererThis.setColorSelectedLine(currLineNumber);
        });

        // 상위 스택으로 이동
        $(importPackageThis.wrapSelector(`.vp-pythonCom-parentDirectory-func-btn`)).click(function(){
            pythonComStateGenerator.setInitCodeLineArray();

            pythonComPageRendererThis.renderCodeLine();
            pythonComPageRendererThis.renderPaletteView();

            var currLineNumber = pythonComStateGenerator.getState(`currLineNumber`);
            pythonComPageRendererThis.setColorSelectedLine(currLineNumber);
        });

        
        // codeLine 생성 클릭 이벤트 함수
        $(importPackageThis.wrapSelector(`.vp-pythonCom-plus-func-btn`)).click(function(){
            var codeLineArray = pythonComStateGenerator.getState(`codeLineArray`);

            pythonComStateGenerator.pushCodeLineArrayStack();
            
            var newNum = pythonComStateGenerator.getIndentSpaceNumStack()[codeLineArray.length-1] || 0;
            pythonComStateGenerator.setState({
                codeLineArray: [...codeLineArray, { type:"BLANK_CODE_LINE",data:"", indentSpaceNum: newNum}],
                currLineNumber: parseInt(codeLineArray.length + 1)
            });   

            pythonComPageRendererThis.renderCodeLine();
            pythonComPageRendererThis.renderPaletteView();
        });
    }
    
    PythonComCodeLineArrayPageRenderer.prototype._makeIndentSpace = function(indentSpaceNum) {
        var indentStr = ``;
        while (indentSpaceNum > 0) {
            indentStr += ` `;
            indentSpaceNum--;
        }
        return indentStr;
    }

    PythonComCodeLineArrayPageRenderer.prototype.renderCodeLine = function() {
        var pythonComPageRendererThis = this;
        var importPackageThis = this.getImportPackageThis();
        var pythonComStateGenerator = this.getStateGenerator();
        pythonComPageRendererThis.setCurrIndentSpaceStr(``);

        var codeLineViewDom = pythonComPageRendererThis.getCodeLineViewDom();
        codeLineViewDom.empty();

        var codeLineArray = pythonComStateGenerator.getState(`codeLineArray`);

        var indentSpaceNum = 0;
        // line 렌더링 :
        for (let i = 0; i < codeLineArray.length; i++) {
            ( function(indexA){
                // FIXME: indentSpaceNum 자동 계산 아직 구현 보류
                // indentSpaceNum = pythonComPageRendererThis._renderCalculateCodeLineIndentSpace(indexA);
                indentSpaceNum = pythonComStateGenerator.getIndentSpaceNumStack()[indexA]
                var _currIndentSpaceStr = pythonComPageRendererThis._makeIndentSpace(indentSpaceNum);
                pythonComPageRendererThis.setCurrIndentSpaceStr(_currIndentSpaceStr);

                var renderCodeLine = PYTHON_COMMON_RENDER_CODELINE_MAP.get(codeLineArray[indexA].type);
                if (codeLineArray[indexA].type === "BREAK" || codeLineArray[indexA].type === "CONTINUE" 
                    || codeLineArray[indexA].type === "ELSE") {
                    renderCodeLine(pythonComPageRendererThis, indexA, codeLineArray[indexA].type);
                } else {
                    renderCodeLine(pythonComPageRendererThis, indexA);
                }
      
            })(i);
        }

        // select된 Line 색깔 변경
        var currLineNumber = pythonComStateGenerator.getState(`currLineNumber`);   
        pythonComPageRendererThis.setColorSelectedLine(currLineNumber);
    }

    PythonComCodeLineArrayPageRenderer.prototype.renderSelectPaletteButtonView = function() {
        var pythonComPageRendererThis = this;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var paletteView = pythonComPageRendererThis.getPaletteBodyView();
        paletteView.empty();

        var currLineNumber = pythonComStateGenerator.getState("currLineNumber");
        var codeLineArray = pythonComStateGenerator.getState('codeLineArray');

        var paletteBlock = $(`<div>
                                <div class="vp-pythonCom-style-flex-column">
                                    <span  class="vp-multilang" data-caption-id="Select_Line">
                                        <strong>Select Line</strong> : ${currLineNumber}
                                    </span>
                                </div>
                              </div>`);

        var flexRowDiv1 = $(`<div class="vp-pythonCom-style-flex-row-evenly"
                                 style="margin:10px 0;"></div>`);
        var flexRowDiv2 = $(`<div class="vp-pythonCom-style-flex-row-evenly"
                                  style="margin:10px 0;"></div>`);
        var flexRowDiv3 = $(`<div class="vp-pythonCom-style-flex-row-evenly"
        style="margin:10px 0;"></div>`);

        this.codeLineTypeList.forEach((type, index) => {
            var btn = renderCodeLineArrayPalleteButton(pythonComPageRendererThis, type, currLineNumber);
            btn.click( function() {
                pythonComStateGenerator.setState({
                    currLineNumber: parseInt($(this).val())
                });
                pythonComPageRendererThis.mapCodeLineTypeToRenderPaletteBlock(type);
            });
            var isFinish = false;

            if(index > 11){
                flexRowDiv3.append(btn); 
                isFinish = true;
            }

            if(isFinish === false && index > 5){
                flexRowDiv2.append(btn); 
                isFinish = true;
            }

            if(isFinish === false){
                flexRowDiv1.append(btn);
            }
        });

        paletteBlock.append(flexRowDiv1);
        paletteBlock.append(flexRowDiv2);
        paletteBlock.append(flexRowDiv3);
        paletteView.append(paletteBlock);

        var currLineNumber = pythonComStateGenerator.getState(`currLineNumber`);   
        $(importPackageThis.wrapSelector(`.vp-pythonCom-select-line-number-view`)).html(`Select Line : ${currLineNumber}`);
    }

    PythonComCodeLineArrayPageRenderer.prototype.renderPaletteView = function() {

        var pythonComPageRendererThis = this;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var paletteView = pythonComPageRendererThis.getPaletteBodyView();
        paletteView.empty();

        var currLineNumber = pythonComStateGenerator.getState("currLineNumber");
        var codeLineArray = pythonComStateGenerator.getState('codeLineArray');
        // codeLineArray가 다 제거되고 0개면 아래코드를 실행하지 않고 리턴
        if(codeLineArray.length === 0 || currLineNumber > codeLineArray.length){
            return;
        } 
        var codeLineType = codeLineArray[currLineNumber-1].type;
        pythonComPageRendererThis.mapCodeLineTypeToRenderPaletteBlock(codeLineType);

        $(importPackageThis.wrapSelector(`.vp-pythonCom-select-line-number-view`)).html(`Select Line : ${currLineNumber}`);
        
        if(codeLineType !== "BLANK_CODE_LINE"){
            return;
        }
        pythonComPageRendererThis.renderSelectPaletteButtonView();

        
    }

    /**
    * select된 Line 색깔 변경
    * 선택된 색깔 beige,  선택되지 않은 색깔 white
    * @param {number} index
    */ 
    PythonComCodeLineArrayPageRenderer.prototype.setColorSelectedLine = function(index) {
        var pythonComPageRendererThis = this;
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        $(importPackageThis.wrapSelector(`.vp-pythonCom-line`)).css("backgroundColor","white");
        $(importPackageThis.wrapSelector(`.vp-pythonCom-line-${index}`)).css("backgroundColor","beige");
    }
           
    PythonComCodeLineArrayPageRenderer.prototype.mapCodeLineTypeToRenderPaletteBlock = function(type) {
        var pythonComPageRendererThis = this;
        var renderPaletteBlock = PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.get(type);
        renderPaletteBlock(pythonComPageRendererThis, type);
    }

    return PythonComCodeLineArrayPageRenderer;
});
