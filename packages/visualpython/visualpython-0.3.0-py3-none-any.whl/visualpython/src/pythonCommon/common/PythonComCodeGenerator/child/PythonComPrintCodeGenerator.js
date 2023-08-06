define ([
    'require'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComCodeGenerator/parent/PythonComCodeGenerator'
], function(requirejs, sb, 
            PythonComCodeGenerator) {
    "use strict";

    /**
     * @class PythonComPrintCodeGenerator
     * @constructor
    */
    var PythonComPrintCodeGenerator = function() {
        // 부모의 멤버변수를 가져오게 하는 call
        PythonComCodeGenerator.call(this);
    };

    PythonComPrintCodeGenerator.prototype = Object.create(PythonComCodeGenerator.prototype);

    /**
    * PythonComCodeGenerator makeCode 메소드 오버라이드
    */
    PythonComPrintCodeGenerator.prototype.makeCode = function() {
        var pythonComStateGenerator = this.getStateGenerator();
        const { paramData } = pythonComStateGenerator.getStateAll();
        const { paramVariable } = paramData;

        var sbCode = this.getSbCode();
        sbCode.appendLine(`print( ${paramVariable} )`);
  
    }

    return PythonComPrintCodeGenerator;
});
