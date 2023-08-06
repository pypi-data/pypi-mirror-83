define ([
    'require'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComCodeGenerator/parent/PythonComCodeGenerator'
], function(requirejs, sb, 
            PythonComCodeGenerator) {
    "use strict";

    /**
     * @class PythonComCodeLineArrayCodeGenerator
     * @constructor
    */
    var PythonComCodeLineArrayCodeGenerator = function() {
         PythonComCodeGenerator.call(this);
    };

    PythonComCodeLineArrayCodeGenerator.prototype = Object.create(PythonComCodeGenerator.prototype);

    PythonComCodeLineArrayCodeGenerator.prototype._makeCustomCodeLine = function(paramList) {
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

    /**
     * PythonComCodeGenerator makeCode 메소드 오버라이드
     */
    PythonComCodeLineArrayCodeGenerator.prototype.makeCode = function() {
        var { codeLineArray } = this.pythonComStateGenerator.getStateAll();
    
        // code line 마다 IndentSpaceStr 계산
        for (let i = 0; i < codeLineArray.length; i++) {
            var IndentSpaceStr = this._makeIndentSpace(codeLineArray[i].indentSpaceNum);
            codeLineArray[i] = {
                ...codeLineArray[i]
                , IndentSpaceStr
            }
        }

        codeLineArray.forEach((codeLine,index) => {
            var code = ``;

            if(codeLine.type === "CLASS" ){
                code = codeLine.IndentSpaceStr + `class` + ` ` + codeLine.data.name + this._mapOneArrayToCodeStr(codeLine.data.paramList) + `:`;
            } else if(codeLine.type === "DEF"){
                code = codeLine.IndentSpaceStr + `def` + ` ` + codeLine.data.name + this._mapOneArrayToCodeStr(codeLine.data.paramList) + `:`;
            } else if(codeLine.type === "DEF_INIT" || codeLine.type === "DEF_DEL"){
                codeLine.data.paramList.unshift("self");
                code = codeLine.IndentSpaceStr + `def` + ` ` + codeLine.data.name + this._mapOneArrayToCodeStr(codeLine.data.paramList) + `:`;
            } else if(codeLine.type === "FOR") {
                code = codeLine.IndentSpaceStr + `for` + ` ` + this._mapOneArrayToCodeStr(codeLine.data.indexValueList) + ` ` + codeLine.data.operator + ` `  + this._makeCustomCodeLine(codeLine.data.iterableObjData) + `:`;
            }
            else if(codeLine.type === "IF") {
                code = codeLine.IndentSpaceStr + `if` + ` ` + this._makeCustomCodeLine(codeLine.data) + `:`;
            }
            else if(codeLine.type === "WHILE") {
                code = codeLine.IndentSpaceStr + `while` + ` ` + this._makeCustomCodeLine(codeLine.data) + `:`;
            }
            else if(codeLine.type === "BREAK") {
                code = codeLine.IndentSpaceStr + `break`;
            }
            else if(codeLine.type === "CONTINUE") {
                code = codeLine.IndentSpaceStr + `continue`;
            }
            else if(codeLine.type === "RETURN") {
                code = codeLine.IndentSpaceStr + `return` + ` ` + this._makeCustomCodeLine(codeLine.data);
            }
            else if(codeLine.type === "ELIF") {
                code = codeLine.IndentSpaceStr + `elif` + ` ` + this._makeCustomCodeLine(codeLine.data) + `:`;
            }
            else if(codeLine.type === "ELSE") {
                code = codeLine.IndentSpaceStr + `else` + `:`;
            }
            else if(codeLine.type === "CUSTOM_CODE_LINE") {
                code = codeLine.IndentSpaceStr + this._makeCustomCodeLine(codeLine.data);
            }
            else if(codeLine.type === "SELF_VARIABLE"){
                code = codeLine.IndentSpaceStr + `self.${codeLine.data} = ${codeLine.data}`;
            }
            else if(codeLine.type === "COMMENT"){
                code = codeLine.IndentSpaceStr + `# ` + codeLine.data;
            }
            else if(codeLine.type === "COMMON_FUNCTION"){
                code = codeLine.IndentSpaceStr + codeLine.data;
            }
            // BLANK_CODE_LINE
            else {        
                code = codeLine.IndentSpaceStr + ``;
            }
            var sbCode = this.getSbCode();
            sbCode.appendLine(code);

    
        });
    }

    return PythonComCodeLineArrayCodeGenerator;
});
