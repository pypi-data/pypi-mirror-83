define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
        // python common 패키지를 위한 라이브러리 import 
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComCodeValidator/parent/PythonComCodeValidator'
], function(requirejs, vpCommon, 
            PythonComCodeValidator ) {
    "use strict";

    /**
     * @class PythonComMakeVariableValidator
     * @constructor
    */
    var PythonComMakeVariableValidator = function() {

    };

    /**
     * PythonComCodeValidator 에서 상속
    */
    PythonComMakeVariableValidator.prototype = Object.create(PythonComCodeValidator.prototype);

    /**
     * PythonComCodeValidator 클래스의 makeCode 메소드 오버라이드
     * @param {Obejct} state 
    */
    PythonComMakeVariableValidator.prototype.validate = function(state) {
        const { paramOption
                , paramData
                , returnVariable
                , dtype
                , isReturnVariable
                , indentSpaceNum } = state;
                
        // return 변수 입력시, 예약어를 썼는지 확인 validation or return 변수 입력시, 숫자를 썼는지 확인 validation
        if (this.checkisVarableReservedWord(returnVariable) || this.checkIsNumberString(returnVariable)) {
            return false;
        }

        switch (paramOption) {
            case "1" : {
                if (this.checkIsNullString(paramData.paramOption1DataStart) || this.checkIsString(paramData.paramOption1DataStart) ) {
                    return false;
                }
                
                break;
            }
            case "2" : {
                if (this.checkIsNullString(paramData.paramOption2DataStart) || this.checkIsString(paramData.paramOption2DataStart) ) {
                    return false;
                }
                if (this.checkIsNullString(paramData.paramOption2DataStop) || this.checkIsString(paramData.paramOption2DataStop) ) {
                    return false;
                }

                break;
            }

            case "3" : {
                if (this.checkIsNullString(paramData.paramOption3DataStart) || this.checkIsString(paramData.paramOption3DataStart) ) {
                    return false;
                }
                if (this.checkIsNullString(paramData.paramOption3DataStop) || this.checkIsString(paramData.paramOption3DataStop) ) {
                    return false;
                }
                if (this.checkIsNullString(paramData.paramOption3DataStep) || this.checkIsString(paramData.paramOption3DataStep) ) {
                    return false;
                }

                break;
            }

            default : {
                break;
            }
        }
        return true;
    }

    return PythonComMakeVariableValidator;
});
