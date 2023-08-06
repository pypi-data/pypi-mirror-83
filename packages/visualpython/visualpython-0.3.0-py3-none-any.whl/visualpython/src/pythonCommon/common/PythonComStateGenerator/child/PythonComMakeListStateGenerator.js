define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComStateGenerator/parent/PythonComStateGenerator'
], function( requirejs, vpCommon, 
             PythonComStateGenerator ) {
    "use strict";

    /**
     * @class PythonComMakeListStateGenerator
     * @constructor
    */
    var PythonComMakeListStateGenerator = function() {
        // state는 makeState함수로 동적 할당 됨
        this.state = {

        }
    };
    /**
     * PythonComStateGenerator 에서 상속
    */
    PythonComMakeListStateGenerator.prototype = Object.create(PythonComStateGenerator.prototype);

    return PythonComMakeListStateGenerator;
});
