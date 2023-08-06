define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComStateGenerator/parent/PythonComStateGenerator'
], function( requirejs, vpCommon, 
             PythonComStateGenerator ) {
    "use strict";

    /**
     * @class PythonComCodeLineStateGenerator
     * @constructor
    */
    var PythonComCodeLineStateGenerator = function() {
        // state는 makeState함수로 동적 할당 됨
        this.state = {

        }
    };
    /**
     * PythonComStateGenerator 에서 상속
    */
    PythonComCodeLineStateGenerator.prototype = Object.create(PythonComStateGenerator.prototype);

    return PythonComCodeLineStateGenerator;
});
