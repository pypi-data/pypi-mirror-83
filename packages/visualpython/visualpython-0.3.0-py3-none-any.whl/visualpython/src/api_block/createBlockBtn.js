define([
    'nbextensions/visualpython/src/common/vpCommon'

    , './api.js'
    , './constData.js'
    , './block.js'
    , './shadowBlock.js'
], function (vpCommon, api, constData, blockData, shadowBlock ) {
    const { changeOldToNewState
            , findStateValue
            , mapTypeToName } = api;
    const { BLOCK_CODELINE_BTN_TYPE
            , BLOCK_CODELINE_TYPE
            , BLOCK_DIRECTION
            , BLOCK_TYPE
            , MAKE_CHILD_BLOCK 

            , NUM_BLOCK_HEIGHT_PX
            , NUM_INDENT_DEPTH_PX
            , NUM_MAX_ITERATION
            , NUM_ZERO
            , NUM_DEFAULT_POS_X
            , NUM_DEFAULT_POS_Y
            , STR_TOP
            , STR_LEFT
            , STR_DIV
            , STR_BORDER
            , STR_PX
            , STR_OPACITY
            , STR_MARGIN_TOP
            , STR_MARGIN_LEFT
            , STR_DISPLAY
            , STR_BACKGROUND_COLOR
            , STR_HEIGHT
            , STR_YES
            , STR_DATA_NUM_ID 
            , STR_DATA_DEPTH_ID
            , STR_NONE
            , STR_BLOCK
            , STR_SELECTED
            , STR_COLON_SELECTED
            , STR_POSITION
            , STR_STATIC
            , STR_RELATIVE
            , STR_ABSOLUTE

            , STR_CLASS
            , STR_DEF
            , STR_IF
            , STR_FOR
            , STR_WHILE
            , STR_IMPORT
            , STR_API
            , STR_TRY
            , STR_RETURN
            , STR_BREAK
            , STR_CONTINUE
            , STR_PASS
            , STR_CODE
            , STR_ELIF
            , STR_PROPERTY

            , STR_CSS_CLASS_VP_BLOCK_CONTAINER
            , STR_CSS_CLASS_VP_BLOCK_NULLBLOCK
            , STR_CSS_CLASS_VP_BLOCK_SHADOWBLOCK
            , STR_CSS_CLASS_VP_BLOCK_DELETE_BTN
            , STR_CSS_CLASS_VP_NODEEDITOR_LEFT
            , STR_CSS_CLASS_VP_NODEEDITOR_BOTTOM_TAB_VIEW
            , STR_CSS_CLASS_VP_BLOCK_LEFT_HOLDER
            , STR_CSS_CLASS_VP_NODEEDITOR_MINIMIZE
            , STR_CSS_CLASS_VP_NODEEDITOR_ARROW_UP
            , STR_CSS_CLASS_VP_NODEEDITOR_ARROW_DOWN
            , STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK
            , STR_CHANGE_KEYUP_PASTE

            , STATE_classInParamList
            , STATE_className
            , STATE_defName
            , STATE_defInParamList
            , STATE_ifCodeLine
            , STATE_isIfElse
            , STATE_isForElse
            , STATE_elifCodeLine
            , STATE_elifList
            , STATE_forCodeLine
            , STATE_whileCodeLine
            , STATE_baseImportList
            , STATE_customImportList
            , STATE_exceptList
            , STATE_exceptCodeLine
            , STATE_isFinally
            , STATE_returnOutParamList
            , STATE_customCodeLine
            
            , COLOR_BLUE
            , COLOR_RED
            , COLOR_GREEN } = constData;  
    const {Block, mapTypeToBlock } = blockData;
    const ShadowBlock = shadowBlock;

    var CreateBlockBtn = function(blockContainerThis, type) { 
        this.blockContainerThis = blockContainerThis;
        this.state = {
            type
            , name: ''
            , isStart: false
            , isDroped: false
        }
        this.rootDomElement = null;

        this.mapTypeToName(type);
        this.render();
        this.bindDragEvent();
    }

    CreateBlockBtn.prototype.getBlockContainerThis = function() {
        return this.blockContainerThis;
    }

    CreateBlockBtn.prototype.setIsStart = function(isStart) {
        this.setState({
            isStart
        });
    }
    CreateBlockBtn.prototype.getIsStart = function() {
        return this.state.isStart;
    }
    CreateBlockBtn.prototype.setIsDroped = function(isDroped) {
        this.setState({
            isDroped
        });
    }
    CreateBlockBtn.prototype.getIsDroped  = function() {
        return this.state.isDroped;
    }

    CreateBlockBtn.prototype.getName = function() {
        return this.state.name;
    }

    CreateBlockBtn.prototype.setName = function(name) {
        this.setState({
            name
        });
    }
    CreateBlockBtn.prototype.getBlockCodeLineType = function() {
        return this.state.type;
    }

    CreateBlockBtn.prototype.mapTypeToName = function(type) {
        var name = ``;
        switch (type) {
            case BLOCK_CODELINE_TYPE.CLASS: {
                name = STR_CLASS;
                break;
            }
            case BLOCK_CODELINE_TYPE.DEF: {
                name = STR_DEF;
                break;
            }
            case BLOCK_CODELINE_TYPE.IF: {
                name = STR_IF;
                break;
            }
            case BLOCK_CODELINE_TYPE.FOR: {
                name = STR_FOR;
                break;
            }
            case BLOCK_CODELINE_TYPE.WHILE: {
                name = STR_WHILE;
                break;
            }
            case BLOCK_CODELINE_TYPE.IMPORT: {
                name = STR_IMPORT;
                break;
            }
            case BLOCK_CODELINE_TYPE.API: {
                name = STR_API;
                break;
            }
            case BLOCK_CODELINE_TYPE.TRY: {
                name = STR_TRY;
                break;
            }
            case BLOCK_CODELINE_TYPE.RETURN: {
                name = STR_RETURN;
                break;
            }
            case BLOCK_CODELINE_TYPE.BREAK: {
                name = STR_BREAK;
                break;
            }
            case BLOCK_CODELINE_TYPE.CONTINUE: {
                name = STR_CONTINUE;
                break;
            }
            case BLOCK_CODELINE_TYPE.PASS: {
                name = STR_PASS;
                break;
            }
            case BLOCK_CODELINE_TYPE.PROPERTY: {
                name = STR_PROPERTY;
                break;
            }
            case BLOCK_CODELINE_TYPE.CODE: {
                name = STR_CODE;
                break;
            }

            default: {
                break;
            }
        }

        this.setState({
            name
        });
    }





    CreateBlockBtn.prototype.getMainDom = function() {
        return this.rootDomElement;
    }

    CreateBlockBtn.prototype.setMainDom = function(rootDomElement) {
        this.rootDomElement = rootDomElement;
    }
    CreateBlockBtn.prototype.getMainDomPosition = function() {
        var rootDom = this.getMainDom();
        var clientRect = $(rootDom)[0].getBoundingClientRect();
        return clientRect;
    }







    // ** Block state 관련 메소드들 */
    CreateBlockBtn.prototype.setState = function(newState) {
            this.state = changeOldToNewState(this.state, newState);
            this.consoleState();
    }
    /**
        특정 state Name 값을 가져오는 함수
        @param {string} stateKeyName
    */
    CreateBlockBtn.prototype.getState = function(stateKeyName) {
        return findStateValue(this.state, stateKeyName);
    }
    CreateBlockBtn.prototype.getStateAll = function() {
        return this.state;
    }
    CreateBlockBtn.prototype.consoleState = function() {
        // console.log(this.state);
    }






    CreateBlockBtn.prototype.render = function() {
        var blockContainer;
        var rootDomElement = $(`<div class='vp-nodeeditor-tab-navigation-node-block-body-btn'>
                                    <span class='vp-block-name'>
                                        ${this.getName()}
                                    </span>
                                </div>`);
        this.setMainDom(rootDomElement);

        var blockCodeType = this.getBlockCodeLineType();
        if (blockCodeType === BLOCK_CODELINE_TYPE.CLASS || blockCodeType === BLOCK_CODELINE_TYPE.DEF
            || blockCodeType === BLOCK_CODELINE_TYPE.RETURN || blockCodeType === BLOCK_CODELINE_TYPE.PROPERTY) {
            blockContainer = $(`.vp-nodeeditor-tab-navigation-node-subblock-1-body-inner`);
            $(rootDomElement).addClass('vp-block-class-def');

        } else if (blockCodeType === BLOCK_CODELINE_TYPE.IF || blockCodeType === BLOCK_CODELINE_TYPE.FOR
            || blockCodeType === BLOCK_CODELINE_TYPE.WHILE || blockCodeType === BLOCK_CODELINE_TYPE.TRY
            || blockCodeType === BLOCK_CODELINE_TYPE.ELSE || blockCodeType === BLOCK_CODELINE_TYPE.ELIF
            || blockCodeType === BLOCK_CODELINE_TYPE.FOR_ELSE || blockCodeType === BLOCK_CODELINE_TYPE.EXCEPT 
            || blockCodeType === BLOCK_CODELINE_TYPE.FINALLY) {
            blockContainer = $(`.vp-nodeeditor-tab-navigation-node-subblock-2-body-inner`);
            $(rootDomElement).addClass('vp-block-if');
  
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.BREAK || blockCodeType === BLOCK_CODELINE_TYPE.CONTINUE || blockCodeType === BLOCK_CODELINE_TYPE.PASS) {
            blockContainer = $(`.vp-nodeeditor-tab-navigation-node-subblock-2-body-inner`);
            $(rootDomElement).css(STR_BACKGROUND_COLOR, COLOR_RED);
        } else {
            blockContainer = $(`.vp-nodeeditor-tab-navigation-node-subblock-3-body-inner`);
            $(rootDomElement).css(STR_BACKGROUND_COLOR, COLOR_GREEN);
     
        }

        blockContainer.append(rootDomElement);
    }



    CreateBlockBtn.prototype.bindDragEvent = function() {
        var that = this;
        var rootDom = this.getMainDom();
        var blockContainerThis = this.getBlockContainerThis();
        var createBlockBtnType = this.getBlockCodeLineType();

        var pos1 = 0;
        var pos2 = 0; 
        var pos3 = 0; 
        var pos4 = 0;
        var buttonX = 0;
        var buttonY = 0;
        // var newPointX = 0;
        // var newPointY = 0;
        var selectedBlockDirection;
        var shadowBlockList = [];

        // var isCollision = false;
        // var collitionBlock = null;

        // $(this).addClass(`vp-nodeeditor-draggable`);
        $(rootDom).draggable({ 
            appendTo: STR_CSS_CLASS_VP_NODEEDITOR_LEFT,
            cursor: 'move', 
            helper: 'clone',
            start: function(event, ui) {
                var rootBlockList = blockContainerThis.getRootBlockList();
               
                rootBlockList.forEach((rootBlock, index) => {
                    var shadowBlock = new ShadowBlock(blockContainerThis, createBlockBtnType, {pointX: 0, pointY: 0}, [],  BLOCK_TYPE.SHADOW_BLOCK);
                    shadowBlock.setRootBlockUUID(rootBlock.getUUID());
                    shadowBlockList.push(shadowBlock);

                    var containerDom = rootBlock.getContainerDom();
                    $(shadowBlock.getMainDom()).css(STR_DISPLAY,STR_NONE);
                    $(shadowBlock.getMainDom()).removeClass(STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK);
                    $(containerDom).append(shadowBlock.getMainDom());
                });
                blockContainerThis.renderBlockLeftHolderListHeight();
            },
            drag: (event, ui) => {       
                // console.log('shadowBlockList', shadowBlockList);

                blockContainerThis.renderBlockLeftHolderListHeight();
                buttonX = event.clientX; 
                buttonY = event.clientY; 

                pos1 = pos3 - buttonX;
                pos2 = pos4 - buttonY;
                pos3 = buttonX;
                pos4 = buttonY;
                var { x: thisX, 
                      y: thisY, 
                      width: thisBlockWidth,
                      height: thisBlockHeight } = that.getMainDomPosition();

                var maxWidth = $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).width();
                var maxHeight = $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).height();
                var scrollHeight = $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).prop('scrollHeight');

                newPointX = buttonX - pos2 - $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).offset().left  - thisBlockWidth / 2;
                newPointY = buttonY - pos1 - $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).offset().top + (scrollHeight - maxHeight);
                if (newPointX < 0) {
                    // newPointX = 0;
        
                }
                /** 이동한 블럭들의 루트블럭 x좌표가 editor 화면의 maxWidth 이상 일때 */
                if (newPointX > maxWidth - $(rootDom).width()) {
                    // newPointX = maxWidth - $(rootDom).width();
                }

                var blockList = blockContainerThis.getBlockList();
                blockList.forEach(block => {
            
                    var { x , y
                          , width: blockWidth
                          , height: blockHeight } = block.getMainDomPosition();
                    var rootBlock = block.getRootBlock();
                    var blockCodeType = block.getBlockCodeLineType();

                    var blockLeftHolderHeight = block.getTempBlockLeftHolderHeight() === 0 
                                                                                        ? blockHeight 
                                                                                        : block.getTempBlockLeftHolderHeight();
                    // console.log(`${block.getName()} : blockLeftHolderHeight`, blockLeftHolderHeight);

                    if ( (x > buttonX 
                        || buttonX > (x + blockWidth)
                        || y  > buttonY 
                        || buttonY > (y + blockHeight + blockHeight /2 + blockLeftHolderHeight) )
                        && block.getIsCollision() === true ) {
                        // console.log(`${block.getName()}충돌 벗어남`);        
                        block.renderBlockHolderShadow_2(STR_NONE);
                        block.setIsCollision(false);
                    }

                    if ( x < buttonX
                        && buttonX < (x + blockWidth )
                        && y  < buttonY
                        && buttonY < (y + blockHeight + blockLeftHolderHeight) ) {     
                        block.renderBlockHolderShadow_2(STR_BLOCK);
                    }

                    if ( x < buttonX
                        && buttonX < (x + blockWidth )
                        && y  < buttonY
                        && buttonY < (y + blockHeight  + blockHeight) ) {     
                        // console.log(`${block.getName()}충돌`);
                        var blockList = blockContainerThis.getBlockList();
                        blockList.forEach(block => {
                            block.setIsCollision(false);
                        });

                        block.setIsCollision(true);

                        if (blockCodeType === BLOCK_CODELINE_TYPE.NULL) {
                            return;
                        }

                        shadowBlockList.forEach(shadowBlock => {
                            $(shadowBlock.getMainDom()).removeClass(STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK);
                            $(shadowBlock.getMainDom()).css(STR_DISPLAY, STR_NONE);
                            shadowBlock.setSelectBlock(null);
                        });

                        shadowBlockList.some(shadowBlock => {
                            if (shadowBlock.getRootBlockUUID() === rootBlock.getUUID()) {
                                $(shadowBlock.getMainDom()).css(STR_DISPLAY,STR_BLOCK);
                                $(shadowBlock.getMainDom()).addClass(STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK);
                                shadowBlock.setSelectBlock(block);
                                return true;
                            }
                        });

                        if (blockCodeType === BLOCK_CODELINE_TYPE.CLASS || blockCodeType === BLOCK_CODELINE_TYPE.DEF || blockCodeType === BLOCK_CODELINE_TYPE.IF ||
                            blockCodeType === BLOCK_CODELINE_TYPE.FOR || blockCodeType === BLOCK_CODELINE_TYPE.WHILE || blockCodeType === BLOCK_CODELINE_TYPE.TRY
                            || blockCodeType === BLOCK_CODELINE_TYPE.ELIF || blockCodeType === BLOCK_CODELINE_TYPE.ELSE
                            || blockCodeType === BLOCK_CODELINE_TYPE.FOR_ELSE || blockCodeType === BLOCK_CODELINE_TYPE.EXCEPT || blockCodeType === BLOCK_CODELINE_TYPE.FINALLY) {
                            selectedBlockDirection = BLOCK_DIRECTION.INDENT;
                        } else if (blockCodeType === BLOCK_CODELINE_TYPE.HOLDER) {
                            selectedBlockDirection = BLOCK_DIRECTION.DOWN; 
                        } else {
                            selectedBlockDirection = BLOCK_DIRECTION.DOWN; 
                        }

                        rootBlock.reArrangeChildBlockDomList(block, undefined, selectedBlockDirection);
                    } else {
                        var rootBlockList = blockContainerThis.getRootBlockList();
                        rootBlockList.some(rootBlock => {
                            var containerDom = rootBlock.getContainerDom();
                            var containerDomRect = $(containerDom)[0].getBoundingClientRect();

                            var { x, y, width: containerDomWidth, height: containerDomHeight} = containerDomRect;
                            if ( x < buttonX
                                && buttonX < (x + containerDomWidth)
                                && y  < buttonY
                                && buttonY < (y + containerDomHeight) ) {  
                                // console.log('in colision');
                            } else {
                                shadowBlockList.forEach(shadowBlock => {
                                    // if (shadowBlock.getRootBlockUUID() === rootBlock.getUUID()) {
                                        $(shadowBlock.getMainDom()).removeClass(STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK);
                                        $(shadowBlock.getMainDom()).css(STR_DISPLAY, STR_NONE);
                                        shadowBlock.setSelectBlock(null);

                                    // }    
                                });
                                // console.log('not colision');
                            }
                        });
                    }
                });
            },
            stop: function() {
                var selectedBlock = null;
                var blockList = blockContainerThis.getBlockList();

                var rootBlockList = blockContainerThis.getRootBlockList();
                shadowBlockList.forEach(shadowBlock => {
                    if ( $(shadowBlock.getMainDom()).hasClass(STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK) ) {
                        selectedBlock = shadowBlock.getSelectBlock();
                    } 
                });

                rootBlockList.forEach(rootBlock => {
                    var rootBlockContainerDom = rootBlock.getContainerDom();
                    $(rootBlockContainerDom).find(STR_CSS_CLASS_VP_BLOCK_SHADOWBLOCK).remove();
                });
                var blockList = blockContainerThis.getBlockList();
                if (selectedBlock !== null) {

                    var block = mapTypeToBlock(blockContainerThis, createBlockBtnType, {pointX: 0, pointY: 0})
                    if (createBlockBtnType === BLOCK_CODELINE_TYPE.CLASS || createBlockBtnType === BLOCK_CODELINE_TYPE.DEF ) {
                        $(block.getHolderBlock().getMainDom()).css(STR_BACKGROUND_COLOR,`${COLOR_BLUE}`);
                    }
                    selectedBlock.appendBlock(block, selectedBlockDirection);

                    var rootBlock = selectedBlock.getRootBlock();
                    var x = rootBlock.getContainerPointX();
                    var y = rootBlock.getContainerPointY();
                    newPointX = x - $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).offset().left;
                    newPointY = y - $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).offset().top;
                    var containerDom = rootBlock.getContainerDom();
                   
                    $(containerDom).css(STR_TOP,`${NUM_DEFAULT_POS_Y}${STR_PX}`);
                    $(containerDom).css(STR_LEFT,`${NUM_DEFAULT_POS_X}${STR_PX}`);
                    rootBlock.setContainerPointX(NUM_DEFAULT_POS_X);
                    rootBlock.setContainerPointY(NUM_DEFAULT_POS_Y);

                    block.renderResetColor();
                    block.renderClickColor();
                    block.renderBottomOption();
                    block.selectThisBlock();
                    block.calculateDepthFromRootBlockAndSetDepth();
                }  else { 
                    if (blockList.length === 0) {

                        var block = mapTypeToBlock(blockContainerThis, createBlockBtnType, {pointX: 0, pointY: 0});
                        /** ContainerDom 삭제 */
                        {
                            var containerDom = block.getContainerDom();
                            $(containerDom).empty();
                            $(containerDom).remove();
                        }
                        var containerDom = document.createElement(STR_DIV);
                        containerDom.classList.add(STR_CSS_CLASS_VP_BLOCK_CONTAINER);
                        block.setContainerDom(containerDom);

                        var blockMainDom = block.getMainDom();
                        $(containerDom).append(blockMainDom);

                        block.setContainerPointX(NUM_DEFAULT_POS_X);
                        block.setContainerPointY(NUM_DEFAULT_POS_Y);
                        $(containerDom).css(STR_TOP,`${NUM_DEFAULT_POS_Y}${STR_PX}`);
                        $(containerDom).css(STR_LEFT,`${NUM_DEFAULT_POS_X}${STR_PX}`);

                        if (createBlockBtnType === BLOCK_CODELINE_TYPE.CLASS){
                     
                            $(containerDom).append(block.getNullBlock().getMainDom());
                            $(containerDom).append(block.getNullBlock().getNullBlock().getMainDom());
                            $(containerDom).append(block.getNullBlock().getHolderBlock().getMainDom());
                            
                            if (createBlockBtnType === BLOCK_CODELINE_TYPE.CLASS || createBlockBtnType === BLOCK_CODELINE_TYPE.DEF ) {
                                $(block.getHolderBlock().getMainDom()).css(STR_BACKGROUND_COLOR, COLOR_BLUE);
                            }
                            $(containerDom).append(block.getHolderBlock().getMainDom());
                            block.bindHoverEvent();
                        }

                        if (createBlockBtnType === BLOCK_CODELINE_TYPE.DEF 
                            || createBlockBtnType === BLOCK_CODELINE_TYPE.IF || createBlockBtnType === BLOCK_CODELINE_TYPE.FOR 
                            || createBlockBtnType === BLOCK_CODELINE_TYPE.WHILE || createBlockBtnType === BLOCK_CODELINE_TYPE.TRY
                            || createBlockBtnType === BLOCK_CODELINE_TYPE.FOR_ELSE || createBlockBtnType === BLOCK_CODELINE_TYPE.EXCEPT 
                            || createBlockBtnType === BLOCK_CODELINE_TYPE.FINALLY) {

                            $(containerDom).append(block.getNullBlock().getMainDom());

                            if (createBlockBtnType === BLOCK_CODELINE_TYPE.CLASS || createBlockBtnType === BLOCK_CODELINE_TYPE.DEF ) {
                                $(block.getHolderBlock().getMainDom()).css(STR_BACKGROUND_COLOR, COLOR_BLUE);
                            }
                            $(containerDom).append(block.getHolderBlock().getMainDom());
                            block.bindHoverEvent();
                        }

                        $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).append(containerDom);
                        block.renderResetColor();
                        block.renderClickColor();
                        block.renderBottomOption();
                        block.selectThisBlock();
                        block.calculateDepthFromRootBlockAndSetDepth();

                        if (createBlockBtnType === BLOCK_CODELINE_TYPE.CLASS){
                            block.calculateLeftHolderHeightAndSet();
                            block.getNullBlock().calculateLeftHolderHeightAndSet();
                        } else {
                            block.calculateLeftHolderHeightAndSet();
                        }
                      
                     
                    } else {
                        var rootBlockList = blockContainerThis.getRootBlockList();
                        // rootBlockList.forEach(rootBlock => {

                        // });
                        var rootBlock = rootBlockList[0];

                        var nextBlockList = rootBlock.getNextBlockList();
                        var stack = [];
                        if (nextBlockList.length !== 0) {
                            stack.push(nextBlockList);
                        }

                        var current = null;
                        while (stack.length !== 0) {
                            current = stack.shift();
                            if (Array.isArray(current)) {
                                current.forEach(block => {
                                    if (block.getDirection() === BLOCK_DIRECTION.DOWN) {
                                        stack.unshift(block);
                                    }
                                });
                            } else{
                                var nextBlockList = current.getNextBlockList();
                                var isDownBlock = nextBlockList.some(nextBlock => {
                                    if (nextBlock.getDirection() === BLOCK_DIRECTION.DOWN) {
                                        current = nextBlock;
                                        stack.unshift(nextBlock);
                                        return true;
                                    }
                                });
                                if ( !isDownBlock ) {
                                    break;
                                }
                            }
                        }

                        var blockCodeType = rootBlock.getBlockCodeLineType();
                        var newBlock = mapTypeToBlock(blockContainerThis, createBlockBtnType, {pointX: 0, pointY: 0});

                        if (blockCodeType === BLOCK_CODELINE_TYPE.CLASS || blockCodeType === BLOCK_CODELINE_TYPE.DEF || blockCodeType === BLOCK_CODELINE_TYPE.IF ||
                            blockCodeType === BLOCK_CODELINE_TYPE.FOR || blockCodeType === BLOCK_CODELINE_TYPE.WHILE || blockCodeType === BLOCK_CODELINE_TYPE.TRY ||
                            blockCodeType === BLOCK_CODELINE_TYPE.ELSE || blockCodeType === BLOCK_CODELINE_TYPE.ELIF || blockCodeType === BLOCK_CODELINE_TYPE.FOR_ELSE || 
                            blockCodeType === BLOCK_CODELINE_TYPE.EXCEPT || blockCodeType === BLOCK_CODELINE_TYPE.FINALLY ) {
                            if (current === null) {
                                rootBlock.getHolderBlock().appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                            } else {
                                current.appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                            }
                        } else {
                            if (current === null) {
                                rootBlock.appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                            } else {
                                current.appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                            }
                        }

                        newBlock.renderResetColor();
                        newBlock.renderClickColor();
                        newBlock.renderBottomOption();
                        newBlock.selectThisBlock();
                        newBlock.calculateDepthFromRootBlockAndSetDepth();
                        newBlock.calculateLeftHolderHeightAndSet();
                    }
                }

                /** 생성 연결된 블럭이 화면 height를 넘칠때(즉 y축으로 스크롤이 생성 될 때) 로직*/
                var maxHeight = $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).height();
                var scrollHeight = $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).prop('scrollHeight');

                {
                    var childBlockDomListHeight = NUM_BLOCK_HEIGHT_PX;
                    var rootBlockList = blockContainerThis.getRootBlockList();
                    var childBlockDomList = rootBlockList[0].getRootBlock().makeChildBlockDomList(MAKE_CHILD_BLOCK.MOVE);
                    childBlockDomList.forEach(childDom => {
                        childBlockDomListHeight += NUM_BLOCK_HEIGHT_PX;
                    });
                    if (childBlockDomListHeight > scrollHeight) {
                        $('.vp-nodeeditor-scrollbar').css('overflow-x','hidden');
                        $('.vp-nodeeditor-scrollbar').css('overflow-y','auto');
        
                    } else {
                        $('.vp-nodeeditor-scrollbar').css('overflow-x','hidden');
                        $('.vp-nodeeditor-scrollbar').css('overflow-y','hidden');
                    }
                }

                var blockList = blockContainerThis.getBlockList();
                blockList.forEach(block => {
                    var mainDom = block.getMainDom();
                    block.calculateWidthAndSet();
                    $(mainDom).find(STR_CSS_CLASS_VP_BLOCK_DELETE_BTN).remove();
                    block.renderBlockHolderShadow(STR_NONE);
                });

                blockContainerThis.renderBlockLeftHolderListHeight();
                
                /** 메모리에 남은 shadowBlockList 삭제 */
                shadowBlockList = [];
            }
        });
    }

    return CreateBlockBtn;
});
