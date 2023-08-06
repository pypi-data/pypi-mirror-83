define ([
    'require'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComCodeGenerator/parent/PythonComCodeGenerator'
], function(requirejs, sb, 
            PythonComCodeGenerator) {
    "use strict";

    /**
     * @class PythonComCommentCodeGenerator
     * @constructor
    */
    var PythonComCommentCodeGenerator = function() {
        // 부모의 멤버변수를 가져오게 하는 call
        PythonComCodeGenerator.call(this);
    };

    PythonComCommentCodeGenerator.prototype = Object.create(PythonComCodeGenerator.prototype);

    /**
    * PythonComCodeGenerator makeCode 메소드 오버라이드
    */
    PythonComCommentCodeGenerator.prototype.makeCode = function() {
        var pythonComStateGenerator = this.getStateGenerator();
        const { paramData } = pythonComStateGenerator.getStateAll();
        const { comment } = paramData;

        var sbCode = this.getSbCode();
        sbCode.appendLine(`# ${comment}`);
  
    }

    return PythonComCommentCodeGenerator;
});
