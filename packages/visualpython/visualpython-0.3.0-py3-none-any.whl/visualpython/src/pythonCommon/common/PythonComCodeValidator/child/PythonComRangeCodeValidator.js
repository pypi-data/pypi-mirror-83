define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
        // python common 패키지를 위한 라이브러리 import 
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComCodeValidator/parent/PythonComCodeValidator'
], function(requirejs, vpCommon, 
            PythonComCodeValidator ) {
    "use strict";

    /**
     * @class PythonComCodeValidator
     * @constructor
    */
    var PythonComRangeCodeValidator = function() {

    };

    /**
     * PythonComCodeValidator 에서 상속
    */
    PythonComRangeCodeValidator.prototype = Object.create(PythonComCodeValidator.prototype);

    /**
     * PythonComCodeValidator 클래스의 makeCode 메소드 오버라이드
     * @param {Obejct} state 
    */
    // FIXME: 임시로 true
    PythonComRangeCodeValidator.prototype.validate = function(state) {
        return true;
    }

    return PythonComRangeCodeValidator;
});
