define ([
    'require'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComCodeGenerator/parent/PythonComCodeGenerator'

    , 'nbextensions/visualpython/src/pythonCommon/api/pythonComStateApi'
], function(requirejs, sb, 
            PythonComCodeGenerator, pythonComStateApi) {
    "use strict";
    var { fixParameterValue } = pythonComStateApi;
    /**
     * @class PythonComEnumerateCodeGenerator
     * @constructor
    */
    var PythonComEnumerateCodeGenerator = function() {
        // 부모의 멤버변수를 가져오게 하는 call
        PythonComCodeGenerator.call(this);
    };


    PythonComEnumerateCodeGenerator.prototype = Object.create(PythonComCodeGenerator.prototype);

    /**
     * PythonComCodeGenerator makeCode 메소드 오버라이드
     */      
    PythonComEnumerateCodeGenerator.prototype.makeCode = function() {
        var pythonComStateGenerator = this.getStateGenerator();
        var { paramOption, paramList, returnVariable, isReturnVariable } = pythonComStateGenerator.getStateAll();
        var sbCode = this.getSbCode();
        var paramStr = ``;

        sbCode.append(`[`);
        paramList.forEach(element => {
            sbCode.append(`${fixParameterValue(element)},`);
        });
        sbCode.append(`]`);
        paramStr += sbCode.toString();
        sbCode.clear();

        switch(paramOption){
            // Basic
            case "1":{
                paramStr = `enumerate( ${paramStr} )`;
                break;
            }

            // To List
            case "2":{
                paramStr = `list( enumerate( ${paramStr} ) )`;
                break;
            }
            // To Tuple
            case "3":{
                paramStr = `tuple( enumerate( ${paramStr} ) )`;
                break;
            }
            default: {
                break;
            }
        }

        var _returnVarStrOrNull = this._validateReturnVar(returnVariable);
        if (isReturnVariable === true) {
            sbCode.appendFormatLine(`{0}${paramStr}`,`${_returnVarStrOrNull}`);
            this._appendPrintReturnVar(returnVariable);
        } else {
            sbCode.appendFormat(`{0}${paramStr}`, `${_returnVarStrOrNull}`);
        }
    }

    return PythonComEnumerateCodeGenerator;
});
