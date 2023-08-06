define ([
    'require'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComCodeGenerator/parent/PythonComCodeGenerator'
], function(requirejs, sb, 
            PythonComCodeGenerator) {
    "use strict";

    /**
     * @class PythonComMakeTupleCodeGenerator
     * @constructor
    */
    var PythonComMakeTupleCodeGenerator = function() {
        // 부모의 멤버변수를 가져오게 하는 call
        PythonComCodeGenerator.call(this);
    };

    PythonComMakeTupleCodeGenerator.prototype = Object.create(PythonComCodeGenerator.prototype);

    /**
    * PythonComCodeGenerator makeCode 메소드 오버라이드
    */
    PythonComMakeTupleCodeGenerator.prototype.makeCode = function() {
    
    }

    return PythonComMakeTupleCodeGenerator;
});
