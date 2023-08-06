define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'

    , 'nbextensions/visualpython/src/pythonCommon/api/pythonComStateApi'
], function( requirejs, vpCommon,
             pythonComStateApi ) {
    "use strict";
    // numpy 함수의 state 데이터를 다루는 api
    var { changeOldToNewState, findStateValue,
          updateOneArrayIndexValueAndGetNewArray } = pythonComStateApi;
    /**
     * @class PythonComStateGenerator
     * @constructor
    */
    var PythonComStateGenerator = function() {
        this.state = {
            
        };
    };
     /** 자식 클래스에서 반드시! 오버라이드 되는 메소드
     *  nummpy 패키지에서 blueprint에 저장된 state를 받아 새로운 state를 만드는 함수
     * @override
     * @param {Object} state 
     */
    PythonComStateGenerator.prototype.makeState = function(state) {
        Object.assign(this.state, state);
    }
    
    /** 자식 클래스에서 반드시! 오버라이드 되는 메소드
        state 값 변경 함수
        @override
        @param {Object} newState
    */
    PythonComStateGenerator.prototype.setState = function(newState) {
        this.state = changeOldToNewState(this.state, newState);
        this.consoleState();
    }

    /** 자식 클래스에서 반드시! 오버라이드 되는 메소드
        모든 state 값을 가져오는 함수
        @override
    */
    PythonComStateGenerator.prototype.getStateAll = function() {
        return this.state;
    }

    /** 자식 클래스에서 반드시! 오버라이드 되는 메소드
        특정 state Name 값을 가져오는 함수
        @param {string} stateKeyName
        @override
    */
    PythonComStateGenerator.prototype.getState = function(stateKeyName) {
        return findStateValue(this.state, stateKeyName);
    }

    PythonComStateGenerator.prototype.consoleState = function() {
        // console.log(this.state);
    }

    /** updateOneArrayIndexValueAndGetNewArray
     *  배열의 특정 인덱스 값을 업데이트하고 업데이트된 새로운 배열을 리턴한다
     *  @param {Array} array 
     *  @param {number} index
     *  @param {number | string} newValue 
     *  @returns {Array} New array
     */

    PythonComStateGenerator.prototype.updateOneArrayIndexValueAndGetNewArray = function(array, index, newValue) {
        return updateOneArrayIndexValueAndGetNewArray(array, index, newValue);
    }
    return PythonComStateGenerator;
});
