define([
    'nbextensions/visualpython/src/common/constant'
], function ( vpConst ) {
    // var getUUID = function() {
    //     return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    //         (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    //     );
    // }

    // stateApi
    /** findStateValue 함수
    *  state를 while루프로 돌면서 돌면서 keyName과 일치하는 state의 value값을 찾아 리턴한다
    *  없으면 null을 리턴한다.
    *  @param {object} state 
    *  @param {string} keyName 
    *  @returns {any | null} returnValueOrNull
    */           
    var findStateValue = function(state, keyName) {
        var result = [];
        var stack = [{ context: result
                    , key: 0
                        , value: state }];
        var currContext;
        var returnValueOrNull = null; 
        while (currContext = stack.pop()) {
            var { context, key, value } = currContext;

            if (!value || typeof value != 'object') {
                if (key === keyName) {
                    returnValueOrNull = value;
                    break;
                }
                
                context[key] = value; 
            }
            else if (Array.isArray(value)) {
                if (key === keyName) {
                    returnValueOrNull = value;
                    break;
                }
        
            } else {
                if (key === keyName) {
                    returnValueOrNull = value;
                    break;
                }
                context = context[key] = Object.create(null);
                Object.entries(value).forEach(([ key,value ]) => {
                    stack.push({ context, key, value });
                });
            }
        };
        return returnValueOrNull;
    };

    /** changeOldToNewState 함수
    *  oldState(이전 state 데이터)와 newState(새로운 state 데이터)를 비교해서
        newState로 들어온 새로운 값을 oldState에 덮어 씌운다.
    *  @param {Object} oldState 
    *  @param {Object} newState 
    *  @returns {Object}
    */
    var changeOldToNewState = function(oldState, newState) {
        var result = [];
        var stack = [{ context: result
                        , key: 0
                        , value: oldState }];
        var currContext;
        while (currContext = stack.pop()) {
            var { context, key, value } = currContext;

            if (!value || typeof value != 'object') {
                var newValue = findStateValue(newState, key);
                if ( newValue === "") {
                    context[key] = "";
                }
                else if (newValue === false) {
                    context[key] = false;
                }
                else {
                    context[key] = newValue || value;
                }
            }
            else if (Array.isArray(value)) {
                var newValue = findStateValue(newState, key);
                context[key] = newValue || value;
            } 
            else {
                context = context[key] = Object.create(null);
                Object.entries(value).forEach(([ key, value ]) => {
                    stack.push({context, key, value});
                });
            }
        };
        return result[0];
    };    
    /** updateOneArrayIndexValueAndGetNewArray
        *  배열의 특정 인덱스 값을 업데이트하고 업데이트된 새로운 배열을 리턴한다
        *  @param {Array} array 
        *  @param {number} index
        *  @param {number | string} newValue 
        *  @returns {Array} New array
        */
    var updateOneArrayIndexValueAndGetNewArray = function(array, index, newValue) {
        return [ ...array.slice(0, index), newValue,
                ...array.slice(index+1, array.length) ]
    }

    /** deleteOneArrayIndexValueAndGetNewArray
    *  배열의 특정 인덱스 값을 삭제하고 삭제된 새로운 배열을 리턴한다
    *  @param {Array} array 
    *  @param {number} index 
    *  @returns {Array} New array
    */
    var deleteOneArrayIndexValueAndGetNewArray = function(array, index) {
        return [ ...array.slice(0, index), 
                ...array.slice(index+1, array.length) ]
    }

    /** updateTwoArrayIndexValueAndGetNewArray
    *  2차원 배열의 특정 인덱스 값을 업데이트하고 업데이트된 새로운 배열을 리턴한다
    *  @param {Array} array 
    *  @param {number} row
    *  @param {number} col
    *  @param {number | string} newValue 
    *  @returns {Array} New array
    */
    var updateTwoArrayIndexValueAndGetNewArray = function(twoarray, row, col, newValue) {
        var newArray = [...twoarray[row].slice(0, col),newValue,
                        ...twoarray[row].slice(col + 1, twoarray[row].length)]
        return [ ...twoarray.slice(0, row), newArray,
                ...twoarray.slice(row+1, twoarray.length) ]
    }
    /** deleteTwoArrayIndexValueAndGetNewArray
    *  2차원 배열의 특정 인덱스 값을 삭제하고 삭제된 새로운 배열을 리턴한다
    *  @param {Array} array 
    *  @param {number} row 
    *  @param {number} col
    *  @returns {Array} New array
    */
    var deleteTwoArrayIndexValueAndGetNewArray = function(twoarray, row, col) {
        var newArray = [...twoarray[row].slice(0, col),
                        ...twoarray[row].slice(col + 1, twoarray[row].length)]
        return [ ...twoarray.slice(0, row), newArray,
                ...twoarray.slice(row+1, twoarray.length) ]
    }

    var mapTypeToName = function(type) {
        var name = ``;
        switch (type) {
            case 1: {
                name = 'class';
                break;
            }
            case 2: {
                name = 'def';
                break;
            }
            case 3: {
                name = 'if';
                break;
            }
            case 4: {
                name = 'for';
                break;
            }
            case 5: {
                name = 'while';
                break;
            }
            case 6: {
                name = 'import';
                break;
            }
            case 7: {
                name = 'api';
                break;
            }
            case 8: {
                name = 'try';
                break;
            }
            case 9: {
                name = 'return';
                break;
            }
            case 10: {
                name = 'break';
                break;
            }
            case 11: {
                name = 'continue';
                break;
            }
            case 12: {
                name = 'pass';
                break;
            }
            case 13: {
                name = 'property';
                break;
            }
            case 100: {
                name = 'elif';
                break;
            }
            case 200: {
                name = 'else';
                break;
            }
            case 201: {
                name = 'else';
                break;
            }
            case 300: {
                name = '__init__';
                break;
            }
            case 400: {
                name = '__del__';
                break;
            }
            case 500: {
                name = 'except';
                break;
            }
            case 600: {
                name = 'finally';
                break;
            }
            case 999: {
                name = 'code';
                break;
            }
            case 1000: {
                name = '';
                break;
            }
            default: {
                break;
            }
        }
        return name;
    }

    var removeSomeBlockAndGetBlockList = function(allArray, exceptArray) {
        var lastArray = [];
        allArray.forEach((block) => {
            var is = exceptArray.some((exceptBlock) => {
                if ( block.getUUID() === exceptBlock.getUUID() ) {
                    return true;
                } 
            });

            if (is !== true) {
                lastArray.push(block);
            } 
        });
        return lastArray;
    }
    
    /** if, for 블럭 등에서 여러개 변수 중 특정 랜덤 변수를 선택할 때 사용 */
    var shuffleArray = function(array) {
        let shuffled = array
          .map(a => ([Math.random(),a]))
          .sort((a,b) => a[0]-b[0])
          .map(a => a[1]);
        return shuffled[0];
    }

    /** 이미지 아이콘 셀렉트 함수 */
    var getImageUrl = function(imageFile) {
        var url = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.RESOURCE_PATH + 'api_block/' + imageFile;
        return url;
    }

    return {
        changeOldToNewState
        , findStateValue
        , mapTypeToName
        , removeSomeBlockAndGetBlockList

        , shuffleArray

        , getImageUrl
    }
});
