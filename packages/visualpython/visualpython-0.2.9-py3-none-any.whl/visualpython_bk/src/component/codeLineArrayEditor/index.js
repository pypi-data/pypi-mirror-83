define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'

    //  
    , 'nbextensions/visualpython/src/component/api/componentConstApi'
    , 'nbextensions/visualpython/src/numpy/api/numpyStateApi'
    , './state'
], function (requirejs, $, vpCommon, vpConst, sb, vpFuncJS,
             componentConstApi, numpyStateApi, CodeLineArrayEditorState ) {


    var sbCode = new sb.StringBuilder();
    var codeLineArrayEditorState = new CodeLineArrayEditorState();  
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "codeLineArrayEditor"
        , funcID : "JY904"  // TODO: ID 규칙 생성 필요
    }
    var vpFuncJS = new vpFuncJS.VpFuncJS(funcOptProp);
    var { controlToggleInput, closeParamArrayEditor, closeComponent } = componentConstApi;

    /** initEditor 시작 함수
     * @param {this} pythonComPageRendererThis 
     */
    var initEditor = function(pythonComPageRendererThis) {
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        
        controlToggleInput();
        codeLineArrayEditorState.setPythonComPageRendererThis(pythonComPageRendererThis);
        codeLineArrayEditorState.setImportPackageThis(importPackageThis);

        pythonComPageRendererThis.pageRender(`.codeLineArrayEditor-inner`);

        if(document.querySelector(".codeLineArrayEditor-inner")) {
            document.querySelector(".codeLineArrayEditor-inner").childNodes[0].style.width = "60%";
            document.querySelector(".codeLineArrayEditor-inner").childNodes[0].style.overflowY = "auto";
            document.querySelector(".codeLineArrayEditor-inner").childNodes[0].style.borderRight = "1px solid #ddd";
            document.querySelector(".codeLineArrayEditor-inner").childNodes[0].classList.add("scrollbar");
            document.querySelector(".codeLineArrayEditor-inner").childNodes[0].style.borderBottom = "1px solid white";
            document.querySelector(".codeLineArrayEditor-inner").childNodes[1].style.width = "40%";
            document.querySelector(".codeLineArrayEditor-inner").childNodes[1].style.overflowY = "auto"; 
            document.querySelector(".codeLineArrayEditor-inner").childNodes[1].classList.add("scrollbar");
            document.querySelector(".codeLineArrayEditor-inner").childNodes[1].style.borderBottom = "1px solid white";
        }
    }

    /** 이벤트 바인딩 함수
     */
    var bindEventFunctions = function() {
        var importPackageThis = codeLineArrayEditorState.getImportPackageThis();
        // oneArrayEditor 편집기를 닫았을때 실행되는 click 함수
        var pythonComPageRendererThis =  codeLineArrayEditorState.getPythonComPageRendererThis();
        $(importPackageThis.wrapSelector('.directoryComponent-closedBtn')).click(() => {
            /**
             * editor 편집기를 받으니 isOpenCodeLineArrayEditorModal을 false로 한다
             * pythonComCodeLineArrayStateGenerator 의 state인 currLineNumber을 1로 한다
             */
            pythonComPageRendererThis.setFalseIsOpenCodeLineArrayEditorModal();
            var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
            pythonComStateGenerator.setState({
                currLineNumber: 1
            });

            /**
             * editor 편집기를 지우고 페이지에 렌더링한다
             */
            $(importPackageThis.wrapSelector('#vp_codeLineArrayEditor')).addClass("hide");
            $(importPackageThis.wrapSelector('#vp_codeLineArrayEditor')).removeClass("show");
            $(importPackageThis.wrapSelector('#vp_codeLineArrayEditor')).remove();
            pythonComPageRendererThis.pageRender();
        });

        $(importPackageThis.wrapSelector('.vp-pythonCom-codeLineArrayEditor-func-executeCodeBtn')).click(() => {

            var importPackageThis = codeLineArrayEditorState.getImportPackageThis();
            pythonComCodeGenerator = importPackageThis.pythonComCodeGenerator;
            // make code
            pythonComCodeGenerator.makeCode();
            // execute code
            vpFuncJS.cellExecute(pythonComCodeGenerator.getCodeAndClear(), true);
            console.log("코드 실행");
        });
    }

    return {
        initEditor,
        bindEventFunctions
    }
});