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
     * @class PythonComMakeListCodeGenerator
     * @constructor
    */
    var PythonComMakeListCodeGenerator = function() {
        // 부모의 멤버변수를 가져오게 하는 call
        PythonComCodeGenerator.call(this);
    };


    PythonComMakeListCodeGenerator.prototype = Object.create(PythonComCodeGenerator.prototype);

    /**
     * PythonComCodeGenerator makeCode 메소드 오버라이드
     */      
    PythonComMakeListCodeGenerator.prototype.makeCode = function() {
        var pythonComStateGenerator = this.getStateGenerator();
        var { paramList, returnVariable, isReturnVariable } = pythonComStateGenerator.getStateAll();
        var sbCode = this.getSbCode();
        var paramStr = ``;

        sbCode.append(`[`);
        paramList.forEach(element => {
            sbCode.append(`${fixParameterValue(element)},`);
        });
        sbCode.append(`]`);
        paramStr += sbCode.toString();
        sbCode.clear();

        var _returnVarStrOrNull = this._validateReturnVar(returnVariable);

        if (isReturnVariable === true) {
            sbCode.appendFormatLine(`{0}${paramStr}`,`${_returnVarStrOrNull}`);
            this._appendPrintReturnVar(returnVariable);
        } else {
            sbCode.appendFormat(`{0}${paramStr}`, `${_returnVarStrOrNull}`);
        }
    }

    return PythonComMakeListCodeGenerator;
});
