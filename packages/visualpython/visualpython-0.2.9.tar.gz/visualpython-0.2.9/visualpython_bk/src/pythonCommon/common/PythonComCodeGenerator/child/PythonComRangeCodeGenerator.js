define ([
    'require'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComCodeGenerator/parent/PythonComCodeGenerator'
], function(requirejs, sb, 
            PythonComCodeGenerator) {
    "use strict";

    /**
     * @class PythonComRangeCodeGenerator
     * @constructor
    */
    var PythonComRangeCodeGenerator = function() {
        // 부모의 멤버변수를 가져오게 하는 call
        PythonComCodeGenerator.call(this);
    };

    PythonComRangeCodeGenerator.prototype = Object.create(PythonComCodeGenerator.prototype);

    /**
    * PythonComCodeGenerator makeCode 메소드 오버라이드
    */
    PythonComRangeCodeGenerator.prototype.makeCode = function() {
        var pythonComStateGenerator = this.getStateGenerator();
        const { paramOption
                , paramData
                , returnVariable 
                , isReturnVariable} = pythonComStateGenerator.getStateAll();
        const { param1Start, 
                param2Start, param2Stop , 
                param3Start, param3Stop, param3Step} = paramData;


        var paramStr = ``;
        switch (paramOption) {
            case "1": {
                paramStr += `${param1Start}`;
                break;
            }
            case "2": {
                paramStr += `${param2Start},${param2Stop}`;
                break;
            }
            case "3": {
                paramStr += `${param3Start},${param3Stop},${param3Step}`;
                break;
            }
            default: {
                break;
            }
        }
        var sbCode = this.getSbCode();
        var _returnVarStrOrNull = this._validateReturnVar(returnVariable);

        if (isReturnVariable === true) {
            sbCode.appendFormatLine(`{0}range( ${paramStr} )`,`${_returnVarStrOrNull}`);
            this._appendPrintReturnVar(returnVariable);
        } else {
            sbCode.appendFormat(`{0}range( ${paramStr} )`, `${_returnVarStrOrNull}`);
        }
  
    }

    return PythonComRangeCodeGenerator;
});
