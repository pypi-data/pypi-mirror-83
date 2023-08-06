define([
    'nbextensions/visualpython/src/common/vpCommon'

    , './api.js'
    , './constData.js'
], function (vpCommon, api, constData ) {
    const { changeOldToNewState
        , findStateValue
        , mapTypeToName } = api;
    const {BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , BLOCK_DIRECTION
            , BLOCK_TYPE
            , MAKE_CHILD_BLOCK

            , NUM_INDENT_DEPTH_PX
            , NUM_MAX_ITERATION
            , STR_NULL
            , STR_TOP
            , STR_LEFT

            , STATE_breakCodeLine
            , STATE_continueCodeLine
            , STATE_passCodeLine
            , STATE_customCodeLine

            , COLOR_BLUE
            , COLOR_RED
            , COLOR_GREEN } = constData;

    var BlockContainer = function() {
        this.blockList = [];
        this.blockStackList = [];
    }

    /** 현재 API Block에 존재하는 블럭을 위에서 부터 맨 아래까지 traverse 하면서 console.log 찍는다. */
    BlockContainer.prototype.traverseBlockList = function() {
        var that = this;
        var blockList = this.blockList;
        var rootBlockList = [];
        blockList.forEach(block => {
            if (block.getBlockCodeLineType() === BLOCK_CODELINE_TYPE.HOLDER || block.getBlockCodeLineType() === BLOCK_CODELINE_TYPE.NULL ) {
                return;
            }
            var rootBlock = block.getRootBlock();
            if (rootBlockList.includes(rootBlock)) {
    
            } else {
                rootBlockList.push(rootBlock);
            }
        });
    
        rootBlockList.forEach(rootBlock => {
            /**  */
            var thisNextBlockDataList = rootBlock.getNextBlockList();
            var stack = [];
    
            if (thisNextBlockDataList.length !== 0) {
                stack.push(thisNextBlockDataList);
            }
    
            var travelBlockDataList = [rootBlock];
    
            var iteration = 0;
            var current;
            while (stack.length !== 0) {
                current = stack.shift();
                /** FIXME: 무한루프 체크 */
                iteration++;
                if (iteration > NUM_MAX_ITERATION) {
                    console.log('무한루프');
                    break;
                }
    
                /** 배열 일 때 */
                if (Array.isArray(current)) {
                    var tempList = [];
                    current.forEach(element => {
                        tempList.push(element);
                    });
                    
                    tempList = tempList.sort((a,b) => {
                        if (a.getDirection() === BLOCK_DIRECTION.INDENT) {
                            return 1;
                        } else {
                            return -1;
                        }
                    });
                    tempList.forEach(el => {
                        stack.unshift(el);
                    });
                } else {
                    var currBlock = current;
                    var direction = current.getDirection();
                    var newData = {
                        currBlock
                        , direction
                    }
                    
                    if (currBlock.getBlockCodeLineType() === BLOCK_CODELINE_TYPE.HOLDER || currBlock.getBlockCodeLineType()  === BLOCK_CODELINE_TYPE.NULL) {
                    } else {
                        travelBlockDataList.push(newData);
                    }
    
                    var nextBlockDataList = current.getNextBlockList();
                    stack.unshift(nextBlockDataList);
                }
            }
            console.log('travelBlockDataList', travelBlockDataList);
        });
    }

    /** block을 blockList에 add */
    BlockContainer.prototype.addBlock = function(block) {
        this.blockList = [...this.blockList, block];
    }

    /** blockList를 가져옴*/
    BlockContainer.prototype.getBlockList = function() {
        return this.blockList;
    }

    /** blockList를 파라미터로 받은 blockList로 덮어 씌움*/
    BlockContainer.prototype.setBlockList = function(blockList) {
        this.blockList = blockList;
    }


    BlockContainer.prototype.getRootBlockList = function() {
        var blockList = this.getBlockList();

        var rootBlockList = [];

        blockList.forEach(block => {
            var rootBlock = block.getRootBlock();
            if (rootBlockList.includes(rootBlock)) {
            } else {
                rootBlockList.push(rootBlock);
            }
        });
        return rootBlockList;
    }

    BlockContainer.prototype.deleteBlock = function(blockUUID) {
        var selectedIndex = -1;
    
        /** blockList를 돌며 삭제하고자 하는 block을 찾음.
         *  block은 고유의 UUID 
         *  파라미터로 들어온 block의 UUID가 blockList의 UUID와 일치하는 블럭이 있는지 찾는 과정.
         *  찾으면 isBlock true, blockList에서 index를 얻음
         *  못찾으면 isBlock false, 아무것도 하지 않고 메소드 작업을 종료.
         */
        var isBlock = this.blockList.some((block, index) => {
            if (block.getUUID() === blockUUID) {
                selectedIndex = index;
                return true;
            } else {
                return false;
            }
        });
    
        if (isBlock) {
            var selectedBlock = this.blockList[selectedIndex];
    
            this.blockList.splice(selectedIndex,1);
    
            if ( selectedBlock.getNullBlock() ) {
                this.blockList.some((block, index) => {
                    if (selectedBlock.getNullBlock().getUUID() === block.getUUID()) {
                        this.blockList.splice(index, 1);
                        return true;
                    }
                });
            }
    
            if ( selectedBlock.getHolderBlock() ) {
                this.blockList.some((block, index) => {
                    if (selectedBlock.getHolderBlock().getUUID() === block.getUUID()) {
                        this.blockList.splice(index, 1);
                        return true;
                    }
                });
            }
        } 
    }

    /** FIXME: blockList를 돌며 API Block 화면 밖으로 나간 block을 찾아 삭제할 메소드 
     *  추후 개발 예정
     */
    BlockContainer.prototype.deleteDisappearedBlock = function() {

    }

    /** API Block 화면에 조립된 Block의 정렬 순서와 값들을 토대로 코드 생성하는 메소드 */
    BlockContainer.prototype.makeCode = function() {
        var that = this;
        var blockList = this.blockList;
        var rootBlockList = [];
        blockList.forEach(block => {
            if (block.getBlockCodeLineType() === BLOCK_CODELINE_TYPE.HOLDER || block.getBlockCodeLineType() === BLOCK_CODELINE_TYPE.NULL ) {
                return;
            }
            var rootBlock = block.getRootBlock();
            if (rootBlockList.includes(rootBlock)) {

            } else {
                rootBlockList.push(rootBlock);
            }
        });

        var codeLineStrDataList = [];
        var codeLineStr = STR_NULL;
        rootBlockList.forEach(rootBlock => {
            
            /**  */
            var thisNextBlockDataList = rootBlock.getNextBlockList();
            var stack = [];

            if (thisNextBlockDataList.length !== 0) {
                stack.push(thisNextBlockDataList);
            }

            var travelBlockDataList = [rootBlock];

            var iteration = 0;
            var current;
            while (stack.length !== 0) {
                current = stack.shift();
                iteration++;
                /** 배열 일 때 */
                if (Array.isArray(current)) {
                    var temp = [];
                    current.forEach(element => {
                        temp.push(element);
                    });
                    
                    temp = temp.sort((a,b) => {
                        if (a.getDirection() === BLOCK_DIRECTION.INDENT) {
                            return 1;
                        } else {
                            return -1;
                        }
                    });
                    temp.forEach(el => {
                        stack.unshift(el);
                    });
    

                } else {
                    var currBlock = current;
                    var direction = current.getDirection();
                    var newData = {
                        currBlock
                        , direction
                    }
                    if (currBlock.getBlockCodeLineType() === BLOCK_CODELINE_TYPE.HOLDER || currBlock.getBlockCodeLineType()  === BLOCK_CODELINE_TYPE.NULL) {

                    } else {
                        travelBlockDataList.push(newData);
                    }

                    var nextBlockDataList = current.getNextBlockList();
                    stack.unshift(nextBlockDataList);
                }
            }

            travelBlockDataList.some((travelBlockData, index) => {
                var depth = 0;
    
                var blockName = STR_NULL;
                var direction = STR_NULL;
    
                var currBlock;
                // root 블럭일 경우
                if (index === 0) {
                    currBlock = travelBlockData;
                    blockName = travelBlockData.getName();
        
                    travelBlockData.setDirection(BLOCK_DIRECTION.ROOT);
                } else {
                    currBlock = travelBlockData.currBlock;
                    blockName = travelBlockData.currBlock.getName();
                    direction = travelBlockData.direction;

                    travelBlockData.currBlock.getDirection(direction);
         
                    if (direction === BLOCK_DIRECTION.INDENT) {
                        var prevBlock = travelBlockData.currBlock;
                        while (prevBlock.getPrevBlock() !== null) {
                            prevBlock = prevBlock.getPrevBlock();
                            if (prevBlock.getDirection() === BLOCK_DIRECTION.DOWN ) {
                    
                            } else {
                                depth++;
                            }
                        }
                    } else {
                        var prevBlock = travelBlockData.currBlock;
                        while (prevBlock.getPrevBlock() !== null) {
                            prevBlock = prevBlock.getPrevBlock();
                            if (prevBlock.getDirection() === BLOCK_DIRECTION.INDENT) {
                                depth++;
                            } else {
                        
                            }
                        }
                    }
                }

                /*  */


                /** depth 계산 */
                var _depth = depth;
                var indentString = STR_NULL;
                while (_depth-- !== 0) {
                    indentString += `    `;
                }

                var codeLine = STR_NULL;
                codeLine += indentString;

                var type = currBlock.getBlockCodeLineType();
                switch (type) {
                    case BLOCK_CODELINE_TYPE.CLASS: {
                        codeLine += `${blockName.toLowerCase()} `;
                        codeLine += currBlock.getState('className');

                        if (currBlock.getState(`classInParamList`).length === 0) {
                            codeLine +=  `()`;
                            codeLine += `:`;
                        } else {
                            codeLine += `(`;
                            currBlock.getState(`classInParamList`).forEach((defInParam, index ) => {
                                codeLine += `${defInParam}`;
                                if (currBlock.getState(`classInParamList`).length - 1 !== index ) {
                                    codeLine += `, `;
                                }
                            });
                            codeLine += `)`;
                            codeLine += `:`;
                        }

                        break;
                    }
                    case BLOCK_CODELINE_TYPE.DEF: {
                        codeLine += `${blockName.toLowerCase()} `;
                        codeLine += currBlock.getState('defName');

                        if (currBlock.getState(`defInParamList`).length === 0) {
                            codeLine +=  `()`;
                            codeLine += `:`;
                        } else {
                            codeLine += `(`;
                            currBlock.getState(`defInParamList`).forEach((defInParam, index ) => {
                                codeLine += `${defInParam}`;
                                if (currBlock.getState(`defInParamList`).length - 1 !== index ) {
                                    codeLine += `, `;
                                }
                            });
                            codeLine += `)`;
                            codeLine += `:`;
                        }
            
                    
                        break;
                    }
                    case BLOCK_CODELINE_TYPE.IF: {
                        codeLine += `${blockName.toLowerCase()} `;
                        codeLine += currBlock.getState('ifCodeLine');
                        codeLine += `:`;
                        break;
                    }
                    case BLOCK_CODELINE_TYPE.FOR: {
                        codeLine += `${blockName.toLowerCase()} `;
                        codeLine += currBlock.getState('forCodeLine');
                        codeLine += `:`;
                        break;
                    }
                    case BLOCK_CODELINE_TYPE.WHILE: {
                        codeLine += `${blockName.toLowerCase()} `;
                        codeLine += currBlock.getState('whileCodeLine');
                        codeLine += `:`;
                        break;
                    }
                    /** import */
                    case BLOCK_CODELINE_TYPE.IMPORT: {
                        var baseImportList = currBlock.getState('baseImportList').filter(baseImport => {
                            if ( baseImport.isImport === true) {
                                return true;
                            } else {
                                return false;
                            }
                        });
                        var customImportList = currBlock.getState('customImportList').filter(customImport => {
                            if ( customImport.isImport === true) {
                                return true;
                            } else {
                                return false;
                            }
                        });
                        baseImportList.forEach((baseImport,index) => {
                            if (index > 0 ) {
                                var _depth = depth;
                                var indentString = ``;
                                while (_depth-- !== 0) {
                                    indentString += `    `;
                                }
                                codeLine += indentString;
                            }

                            codeLine += `${blockName.toLowerCase()} ${baseImport.baseImportName} as ${baseImport.baseAcronyms}\n`;
                        });
                        customImportList.forEach((baseImport,index ) => {
                            if (index > 0 ) {
                                var _depth = depth;
                                var indentString = ``;
                                while (_depth-- !== 0) {
                                    indentString += `    `;
                                }
                                codeLine += indentString;
                            }
                            codeLine += `${blockName.toLowerCase()} ${baseImport.baseImportName} as ${baseImport.baseAcronyms}\n`;
                        });
                        break;
                    }
                    /** api */
                    case BLOCK_CODELINE_TYPE.API: {
                        break;
                    }
                    /** try */
                    case BLOCK_CODELINE_TYPE.TRY: {
                        codeLine += `${blockName.toLowerCase()}:`;
                        break;
                    }
                    /** return */
                    case BLOCK_CODELINE_TYPE.RETURN: {
                        codeLine += `${blockName.toLowerCase()} `;
                        if (currBlock.getState(`returnOutParamList`).length === 0) {
                
                        } else {
                            codeLine += ``;
                            currBlock.getState(`returnOutParamList`).forEach((defInParam, index ) => {
                                codeLine += `${defInParam}`;
                                if (currBlock.getState(`returnOutParamList`).length - 1 !== index ) {
                                    codeLine += `, `;
                                }
                            });
                            codeLine += ``;
                        }

                        break;
                    }

                    /** break */
                    case BLOCK_CODELINE_TYPE.BREAK: {
                        codeLine += `${currBlock.getState(STATE_breakCodeLine)} `;
                        break;
                    }
                    /** continue */
                    case BLOCK_CODELINE_TYPE.CONTINUE: {
                        codeLine += `${currBlock.getState(STATE_continueCodeLine)} `;
                        break;
                    }
                    /** pass */
                    case BLOCK_CODELINE_TYPE.PASS: {
                        // codeLine += `${blockName.toLowerCase()} `;
                        codeLine += `${currBlock.getState(STATE_passCodeLine)} `;
                        break;
                    }
                    /** elif */
                    case BLOCK_CODELINE_TYPE.ELIF: {
                        codeLine += `${blockName.toLowerCase()} `;
                        codeLine += currBlock.getState('elifCodeLine');
                        codeLine += `:`;
                        break;
                    }
                    /** else */
                    case BLOCK_CODELINE_TYPE.ELSE: {
                        codeLine += `${blockName.toLowerCase()}:`;
                        break;
                    }
                    /** for else */
                    case BLOCK_CODELINE_TYPE.FOR_ELSE: {
                        codeLine += `${blockName.toLowerCase()}:`;
                        break;
                    }
                    /** init */
                    case 300: {
                        codeLine += `${blockName.toLowerCase()} `;
                        break;
                    }
                    /** del */
                    case 400: {
                        codeLine += `${blockName.toLowerCase()} `;
                        break;
                    }
                    /** except */
                    case BLOCK_CODELINE_TYPE.EXCEPT: {
                        codeLine += `${blockName.toLowerCase()}`;
                        codeLine += currBlock.getState('exceptCodeLine');
                        codeLine += `:`;
                        break;
                    }
                    /** finally */
                    case BLOCK_CODELINE_TYPE.FINALLY: {
                        codeLine += `${blockName.toLowerCase()}:`;
                        break;
                    }
                    /** code */
                    case BLOCK_CODELINE_TYPE.CODE: {
                        codeLine += currBlock.getState(STATE_customCodeLine);
                        break;
                    }
                }
                codeLine += `\n`;
                codeLineStr += codeLine;
            });

            codeLineStrDataList.push({
                pointY: rootBlock.getContainerPointY()
                , codeLineStr
            });
            codeLineStr = ``;
        });

        codeLineStrDataList = codeLineStrDataList.sort((a,b) => {
            if (a.pointY - b.pointY > 0) {
                return 1;
            } else {
                return -1;
            }
        });

        var returnCodeLineStr = ``;
        returnCodeLineStr += `# Auto-Generated by VisualPython\n`;
        codeLineStrDataList.forEach((codeLineStrData,index) => {
            returnCodeLineStr += `${codeLineStrData.codeLineStr}\n`;
        });
        return returnCodeLineStr;
    }


    BlockContainer.prototype.renderBlockLeftHolderListHeight = function() {
        var blockList = this.getBlockList();
        var selectedBlockList = [];

        blockList.forEach(block => {
            var type = block.getBlockCodeLineType();
            if (type === BLOCK_CODELINE_TYPE.CLASS || type === BLOCK_CODELINE_TYPE.DEF || type === BLOCK_CODELINE_TYPE.IF ||
                type === BLOCK_CODELINE_TYPE.FOR || type === BLOCK_CODELINE_TYPE.WHILE || type === BLOCK_CODELINE_TYPE.TRY ||
                type === BLOCK_CODELINE_TYPE.ELSE || type === BLOCK_CODELINE_TYPE.ELIF || type === BLOCK_CODELINE_TYPE.FOR_ELSE || 
                type === BLOCK_CODELINE_TYPE.EXCEPT || type === BLOCK_CODELINE_TYPE.FINALLY ) {
                selectedBlockList.push(block);
            }
        });

        selectedBlockList.forEach(block => {
            var mainDom = block.getMainDom();
            if ($(mainDom).find('.vp-block-left-holder')[0]) {
                var leftHolderClientRect = $(mainDom).find('.vp-block-left-holder')[0].getBoundingClientRect();

                var holderBlock = block.getHolderBlock();
                var holderBlockClientRect = $(holderBlock.getMainDom())[0].getBoundingClientRect();

                var distance = holderBlockClientRect.y - leftHolderClientRect.y;
                $(mainDom).find('.vp-block-left-holder').css('height',`${distance}px`);
                block.setTempBlockLeftHolderHeight(distance);
            }
        });
    }

    return BlockContainer;
});
