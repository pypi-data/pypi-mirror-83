define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComStateGenerator/parent/PythonComStateGenerator'
], function( requirejs, vpCommon, 
             PythonComStateGenerator ) {
    "use strict";

    /**
     * @class PythonComCodeLineArrayStateGenerator
     * @constructor
    */
    var PythonComCodeLineArrayStateGenerator = function() {
        // state는 makeState함수로 동적 할당 됨
        this.state = {

        }
    };
    /**
     * PythonComStateGenerator 에서 상속
    */
    PythonComCodeLineArrayStateGenerator.prototype = Object.create(PythonComStateGenerator.prototype);

    /**
     * codeLineArray 멤버 변수를 get
     */
    PythonComCodeLineArrayStateGenerator.prototype.getCodeLineArray = function() {
        return this.state.codeLineArray;
    }

    /**
     * codeLineArray 멤버 변수의 length를 get
     */
    PythonComCodeLineArrayStateGenerator.prototype.getCodeLineArrayLength = function() {
        return this.state.codeLineArray.length;
    }

    /**
     * codeLineArray안에 모든 IndentSpaceNum을 get
     */
    PythonComCodeLineArrayStateGenerator.prototype.getIndentSpaceNumStack = function() {
        var indentSpaceNumStack = [];
        this.state.codeLineArray.forEach(element => {
            indentSpaceNumStack.push(element.indentSpaceNum);
        });
        return indentSpaceNumStack;
    }

    /**
     * codeLineArray멤버 변수에 새로운 indentSpaceNum 를 set
     * @param { indentSpaceNumStack } 
     */
    PythonComCodeLineArrayStateGenerator.prototype._setIndentSpaceNumStack = function(indentSpaceNumStack) {
        this.state.codeLineArray = this.state.codeLineArray.map((_,index) => {
           var newIndentSpaceNum = indentSpaceNumStack[index];
            return {
                ...this.state.codeLineArray[index]
                , indentSpaceNum: newIndentSpaceNum
            }
        });
    }

    PythonComCodeLineArrayStateGenerator.prototype.swapLineAtoB = function(index1, index2) {
        var codeLineArray = [...this.state.codeLineArray];
        var temp = 0;
        temp = codeLineArray[index2];
        codeLineArray[index2] = codeLineArray[index1];
        codeLineArray[index1] = temp;

        this.state.codeLineArray = codeLineArray;
    }

    /** codeLine을 index + 1에 추가한다
     * @param {object<codeLine>} newData 
     * @param {number} index 
     */
    PythonComCodeLineArrayStateGenerator.prototype.addCodeLineArrayIndexValueAndGetNewArray = function(newData, index) {
        this.state.codeLineArray = [ ...this.state.codeLineArray.slice(0,index + 1),newData,
                                     ...this.state.codeLineArray.slice(index + 1,this.state.codeLineArray.length)];
    }

    /** index번째의 codeLine을 제거한다
    * @param {number} index 
    */
    PythonComCodeLineArrayStateGenerator.prototype.deleteCodeLineArrayIndexValueAndGetNewArray = function(index) {
        this.state.codeLineArray = [ ...this.state.codeLineArray.slice(0 , index), 
                                     ...this.state.codeLineArray.slice(index + 1,this.state.codeLineArray.length) ];
    }

    PythonComCodeLineArrayStateGenerator.prototype.updateIndentSpaceNumStackIndexValue = function(newData, index) {
        var indentSpaceNumStack = [];
        this.state.codeLineArray.forEach(element => {
            indentSpaceNumStack.push(element.indentSpaceNum);
        });

        var newStack = [ ...indentSpaceNumStack.slice(0,index),newData,
                         ...indentSpaceNumStack.slice(index+1,indentSpaceNumStack.length)];

        this._setIndentSpaceNumStack(newStack);
    }
    PythonComCodeLineArrayStateGenerator.prototype.plusIndentSpaceNumStackIndexValue = function(index) {
        var indentSpaceNumStack = [];
        this.state.codeLineArray.forEach(element => {
            indentSpaceNumStack.push(element.indentSpaceNum);
        });

        var newData = indentSpaceNumStack[index] + 4;
        var newStack = [ ...indentSpaceNumStack.slice(0,index),newData,
                         ...indentSpaceNumStack.slice(index+1,indentSpaceNumStack.length)];

        this._setIndentSpaceNumStack(newStack);
    }
    PythonComCodeLineArrayStateGenerator.prototype.minusIndentSpaceNumStackIndexValue = function(index) {
        var indentSpaceNumStack = [];
        this.state.codeLineArray.forEach(element => {
            indentSpaceNumStack.push(element.indentSpaceNum);
        });
        // indentSpaceNum이 4보다 커야 4만큼 작게한다
        var newData = indentSpaceNumStack[index];
        if(newData > 3) {
            newData = newData - 4;
        }
        var newStack = [ ...indentSpaceNumStack.slice(0,index),newData,
                         ...indentSpaceNumStack.slice(index+1,indentSpaceNumStack.length)];

        this._setIndentSpaceNumStack(newStack);
    }

    PythonComCodeLineArrayStateGenerator.prototype.getCodeLineArrayStack = function() {
        return this.state.codeLineArrayStack;
    }

    PythonComCodeLineArrayStateGenerator.prototype.getCodeLineArrayStackLength = function() {
        return this.state.codeLineArrayStack.length;
    }

    PythonComCodeLineArrayStateGenerator.prototype.setInitCodeLineArray = function() {
        if(this.getCodeLineArrayStackLength() === 0){
            return;
        }

        this.state.codeLineArray = [...this.state.codeLineArrayStack[0]];
        this.state.codeLineArrayStack = [];
    }

    PythonComCodeLineArrayStateGenerator.prototype.pushCodeLineArrayStack = function() {
        this.state.codeLineArrayStack.push(this.state.codeLineArray);
    }
    
    PythonComCodeLineArrayStateGenerator.prototype.popCodeLineArrayStackAndSet = function() {
        if(this.state.codeLineArrayStack.length === 0){
            return;
        }

        this.state.codeLineArray = this.state.codeLineArrayStack.pop();
    }

    return PythonComCodeLineArrayStateGenerator;
});
