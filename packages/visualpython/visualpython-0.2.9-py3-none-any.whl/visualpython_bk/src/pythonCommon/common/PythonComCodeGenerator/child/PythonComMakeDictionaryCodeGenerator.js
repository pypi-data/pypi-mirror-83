define ([
    'require'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComCodeGenerator/parent/PythonComCodeGenerator'
], function(requirejs, sb, 
            PythonComCodeGenerator) {
    "use strict";

    /**
     * @class PythonComMakeDictionaryCodeGenerator
     * @constructor
    */
    var PythonComMakeDictionaryCodeGenerator = function() {
        // 부모의 멤버변수를 가져오게 하는 call
        PythonComCodeGenerator.call(this);
    };

    PythonComMakeDictionaryCodeGenerator.prototype = Object.create(PythonComCodeGenerator.prototype);

    /**
    * PythonComCodeGenerator makeCode 메소드 오버라이드
    */
    PythonComMakeDictionaryCodeGenerator.prototype.makeCode = function() {
    
    }

    return PythonComMakeDictionaryCodeGenerator;
});
