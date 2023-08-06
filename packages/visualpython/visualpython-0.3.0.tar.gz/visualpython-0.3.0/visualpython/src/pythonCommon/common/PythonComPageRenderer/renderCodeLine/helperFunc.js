define ([
    // 기본 
    'require'

], function ( requirejs ) {
    var bindCodeLineEventFunc = function(pythonComPageRendererThis, index) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var codeLineArray = pythonComStateGenerator.getState(`codeLineArray`);
        // index a번째 line 편집용 팔레트 클릭 

        //index a번째 line 편집용 팔레트 클릭 
        $(importPackageThis.wrapSelector(`.vp-pythonCom-line-${index + 1}`)).click(function(){
            pythonComStateGenerator.setState({
                currLineNumber: parseInt(index + 1)
            });
            pythonComPageRendererThis.renderPaletteView();
            $(importPackageThis.wrapSelector(`.vp-pythonCom-line`)).css("backgroundColor","white");
            $(this).css("backgroundColor","beige");
        });

        // index a번째 line 삭제
        $(importPackageThis.wrapSelector(`.vp-pythonCom-line-delete-func-btn-${index + 1}`)).click(function() {
            pythonComStateGenerator.pushCodeLineArrayStack();
            var newCodeLineArray = pythonComStateGenerator.deleteCodeLineArrayIndexValueAndGetNewArray(index);
            pythonComStateGenerator.setState({
                codeLineArray: newCodeLineArray,
                currLineNumber: parseInt(index)
            });    

            /**
             * codeLineArray가 전부 삭제되었을 때 리턴
             */
            pythonComPageRendererThis.renderCodeLine();
            pythonComPageRendererThis.renderPaletteView();
        });

        // code line indentSpace += 4
        $(importPackageThis.wrapSelector(`.vp-pythonCom-line-indentSpace-plus-func-btn-${index + 1}`)).click(function() {
            pythonComStateGenerator.pushCodeLineArrayStack();
            pythonComStateGenerator.plusIndentSpaceNumStackIndexValue(index );

            pythonComPageRendererThis.renderCodeLine();
            pythonComPageRendererThis.setColorSelectedLine(index + 1);
        });

        // code line indentSpace -= 4
        $(importPackageThis.wrapSelector(`.vp-pythonCom-line-indentSpace-minus-func-btn-${index + 1}`)).click(function() {
            pythonComStateGenerator.pushCodeLineArrayStack();
            pythonComStateGenerator.minusIndentSpaceNumStackIndexValue(index);
            
            pythonComPageRendererThis.renderCodeLine();
            pythonComPageRendererThis.setColorSelectedLine(index + 1);
        });

        // code line up 
        $(importPackageThis.wrapSelector(`.vp-pythonCom-line-up-func-btn-${index + 1}`)).click(function() {
            //index 0 이하일 경우 작동 정지
            if(index < 1){
                return;
            }
            pythonComStateGenerator.pushCodeLineArrayStack();

            pythonComStateGenerator.swapLineAtoB(index - 1, index);
            pythonComPageRendererThis.renderCodeLine();
            pythonComPageRendererThis.renderPaletteView();
            pythonComPageRendererThis.setColorSelectedLine(index + 1);

            $(importPackageThis.wrapSelector(`.vp-pythonCom-select-line-number-view`)).html(`Select Line : ${index + 1}`);
        });

        // code line down 
        $(importPackageThis.wrapSelector(`.vp-pythonCom-line-down-func-btn-${index + 1}`)).click(function() {
            var codeLineArrayLength = pythonComStateGenerator.getCodeLineArrayLength();
            // index가 codeLineArrayLength 이상일 경우 작동 정지
            if(index > codeLineArrayLength - 2){
                return;
            }
            pythonComStateGenerator.pushCodeLineArrayStack();

            pythonComStateGenerator.swapLineAtoB(index + 1, index);
            pythonComPageRendererThis.renderCodeLine();
            pythonComPageRendererThis.renderPaletteView();
            pythonComPageRendererThis.setColorSelectedLine(index + 1);

            $(importPackageThis.wrapSelector(`.vp-pythonCom-select-line-number-view`)).html(`Select Line : ${index + 1}`);
        });

        // index 다음번째에 codeLine 생성
        $(importPackageThis.wrapSelector(`.vp-pythonCom-line-insertPalette-func-btn-${index + 1}`)).click(function() {
            var newData = {
                type:"BLANK_CODE_LINE"
                , data:""
                , indentSpaceNum: 0
            }
            pythonComStateGenerator.pushCodeLineArrayStack();

            var newCodeLineArray = pythonComStateGenerator.addCodeLineArrayIndexValueAndGetNewArray(newData, index)
            pythonComStateGenerator.setState({
                codeLineArray: newCodeLineArray,
                currLineNumber: parseInt(index + 1)
            });    

            pythonComPageRendererThis.renderCodeLine();
            pythonComPageRendererThis.renderPaletteView();
            pythonComPageRendererThis.setColorSelectedLine(index + 1);
        });
    }

    var mapCodeLineDataToStr = function(paramList) {
        var paramStr = ``;
        paramList.forEach((param,index) => {
            var indentSpaceSbCode = ` `;
            if(index === 0){
                indentSpaceSbCode = ``;
            } else {
                indentSpaceSbCode = ` `;
            }
            
            // index 번째의 코드를 만들기 위한 데이터가 아무것도 없을시 건너 뛴다
            if(param.type === "UNDEFINED"){
      
            } else {
                var code = indentSpaceSbCode + param.data;
                paramStr += code;
            }
        });

        return paramStr;
    }
    var mapDefParamListToStr = function(codeLineType, paramList) {
        var paramStr = `(`;

        // prefix self 파라미터
        if(codeLineType === "DEF_INIT" || codeLineType === "DEF_DEL"){
            paramStr += `self`;
            if(paramList.length !== 0){
                paramStr += ` ,`;
            }
        } 

        paramList.forEach(function(element, index) {
            if(index === paramList.length - 1){
                paramStr += `${element}`;
            } else {
                paramStr += `${element},`;
            }
        }); 
        paramStr += `)`;
        return paramStr;
    }
    var mapParamListToStr = function(paramList) {
        var paramStr = ``;

        paramList.forEach(function(element, index) {
            if(index === paramList.length - 1){
                paramStr += `${element}`;
            } else {
                paramStr += `${element},`;
            }
        }); 
  
        return paramStr;
    }
    return {
        bindCodeLineEventFunc
        , mapCodeLineDataToStr
        , mapDefParamListToStr
        , mapParamListToStr
    };     

});