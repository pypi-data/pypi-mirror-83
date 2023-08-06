define ([
    'require'
    , 'nbextensions/visualpython/src/common/StringBuilder'
        // python common 패키지를 위한 라이브러리 import 
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComCodeGenerator/parent/PythonComCodeGenerator'
], function(requirejs, sb, 
            PythonComCodeGenerator) {
    "use strict";

    /**
     * @class PythonComMakeVariableGenerator
     * @constructor
    */
    var PythonComCodeLineCodeGenerator = function() {
        PythonComCodeGenerator.call(this);
    };


    PythonComCodeLineCodeGenerator.prototype = Object.create(PythonComCodeGenerator.prototype);


    /**
     * PythonComCodeGenerator makeCode 메소드 오버라이드
     */
    PythonComCodeLineCodeGenerator.prototype.makeCode = function() {
        var pythonComStateGenerator = this.getStateGenerator();
        var { paramList } = pythonComStateGenerator.getStateAll();
    /**
     * 예시
     *  // 0: {type: "CONDITION_OPERATOR", data: ">"}
        // 1: {type: "ASSIGN_OPERATOR", data: "="}
        // 2: {type: "RIGHT_BRACKET", data: ")"}
        // 3: {type: "INPUT_VARIABLE", data: "aa"}
        // 4: {type: "CONDITION_OPERATOR", data: "<"}
    */
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
                this.sbCode.append(code);
            }
        });
    }

    return PythonComCodeLineCodeGenerator;
});
