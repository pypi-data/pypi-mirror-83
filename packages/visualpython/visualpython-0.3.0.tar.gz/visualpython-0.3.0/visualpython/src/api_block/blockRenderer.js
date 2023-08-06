define([
    './constData.js'
], function ( constData ) {
    const { BLOCK_CODELINE_TYPE
            , STR_NULL
            , STR_DIV
            , STR_SELECTED
            , STR_ONE_SPACE
            , STR_ONE_INDENT

            , STR_BREAK
            , STR_CONTINUE
            , STR_PASS

            , STR_INPUT_YOUR_CODE
            
            , STR_CSS_CLASS_VP_NODEEDITOR_OPTION_INPUT_REQUIRED

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
            , STATE_breakCodeLine
            , STATE_passCodeLine
            , STATE_continueCodeLine
            , STATE_baseImportList
            , STATE_customImportList
            , STATE_exceptList
            , STATE_exceptCodeLine
            , STATE_isFinally
            , STATE_returnOutParamList
            , STATE_customCodeLine
        
            , COLOR_GRAY_input_your_code } = constData;

    var renderMainDom = function() {
        var mainDom = document.createElement(STR_DIV);
        mainDom.classList.add('vp-block');
        return mainDom;
    }

    var renderMainInnerDom = function() {
        var mainInnerDom = $(`<div class='vp-block-inner'></div>`);
        return mainInnerDom;
    }

    var generateClassInParamList = function(that) {
        var classInParamList = that.getState(STATE_classInParamList);
        var classInParamStr = `(`;
        classInParamList.forEach((classInParam, index ) => {
            classInParamStr += `${classInParam}`;
            if (that.getState(STATE_classInParamList).length - 1 !== index ) {
                classInParamStr += `, `;
            }
        });
        classInParamStr += `) : `;
        return classInParamStr;
    }

    var generateDefInParamList = function(that) {
        /** 함수 파라미터 */
        var defInParamList = that.getState(STATE_defInParamList);
        var defInParamStr = `(`;
        defInParamList.forEach((defInParam, index ) => {
            defInParamStr += `${defInParam}`;
            if (that.getState(STATE_defInParamList).length - 1 !== index ) {
                defInParamStr += `, `;
            }
        });
        defInParamStr += `) : `;
        return defInParamStr;
    }

    var generateReturnOutParamList = function(that) {
        var returnOutParamList = that.getState(STATE_returnOutParamList);
        var returnOutParamStr = ` `;
        returnOutParamList.forEach((defInParam, index ) => {
            returnOutParamStr += `${defInParam}`;
            if (that.getState(STATE_returnOutParamList).length - 1 !== index ) {
                returnOutParamStr += `, `;
            }
        });
        returnOutParamStr += ``;
        return returnOutParamStr;
    }

    var renderMainHeaderDom = function(that) {
        /** 클래스 이름 */
        var className = that.getState(STATE_className);
        /** 클래스 파라미터 */
        var classInParamList = that.getState(STATE_classInParamList);
        var classInParamStr = generateClassInParamList(that);

        /** 함수 이름 */
        var defName = that.getState(STATE_defName);
        /** 함수 파라미터 */
        var defInParamList = that.getState(STATE_defInParamList);
        var defInParamStr = generateDefInParamList(that);

        /** return 파라미터*/
        var returnOutParamList = that.getState(STATE_returnOutParamList);
        var returnOutParamStr = generateReturnOutParamList(that);

        var blockCodeType =  that.getBlockCodeLineType();
        var blockName = that.getName();
        var isBreakOrContinueOrPassOrCode = false;
        if (blockCodeType === BLOCK_CODELINE_TYPE.BREAK || blockCodeType === BLOCK_CODELINE_TYPE.CONTINUE || blockCodeType === BLOCK_CODELINE_TYPE.PASS
            || blockCodeType === BLOCK_CODELINE_TYPE.CODE) {
            isBreakOrContinueOrPassOrCode = true;
        }
        var blockUUID = that.getUUID();
        var mainHeaderDom = $(`<div class='vp-block-header'>
                                ${
                                    isBreakOrContinueOrPassOrCode === true    
                                        ? STR_NULL
                                        :  `<strong class='vp-nodeeditor-style-flex-column-center ${that.getBlockCodeLineType() !== BLOCK_CODELINE_TYPE.HOLDER 
                                                                                                                            ? 'vp-block-name' 
                                                                                                                            : ''}' 
                                                style='margin-right:30px; 
                                                       font-size:12px; 
                                                       color:#252525;'>
                                            ${blockName}
                                            </strong>`
                                }
                                <div class='vp-nodeeditor-codeline-ellipsis 
                                            vp-nodeeditor-codeline-container-box'>
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.CLASS   
                                                ? `<div class='vp-nodeeditor-style-flex-row'>
                                                        <div class='vp-block-header-class-name-${blockUUID}'
                                                            style='font-size:12px;'>
                                                            ${className}
                                                        </div>
                                                        <div class='vp-block-header-class-param-${blockUUID}'
                                                            style='font-size:12px;'>
                                                            ${className.length === 0 
                                                                ? ''
                                                                : classInParamStr}
                                                        </div>
                                                    </div>`
                                                : STR_NULL
                                        }

                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.DEF  
                                                ? `<div class='vp-nodeeditor-style-flex-row'>
                                                        <div class='vp-block-header-def-name-${blockUUID}'
                                                            style='font-size:12px;'>
                                                            ${defName}
                                                        </div>
                                                        <div class='vp-block-header-def-param-${blockUUID}'
                                                                style='font-size:12px;'>
                                                                ${defName.length === 0 
                                                                    ? ''
                                                                    : defInParamStr}
                                                        </div>
                                                    </div>`
                                                : STR_NULL
                                        }
                                            

                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.IF    
                                                ? `<div class='vp-block-header-if-code-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${that.getState(STATE_ifCodeLine)}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.FOR   
                                                ? `<div class='vp-block-header-for-code-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${that.getState(STATE_forCodeLine)}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.WHILE 
                                                ? `<div class='vp-block-header-while-code-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${that.getState(STATE_whileCodeLine)}
                                                    </div>`
                                                : STR_NULL
                                        }   
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.ELIF
                                                ? `<div class='vp-block-header-elif-code-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${that.getState(STATE_elifCodeLine)}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.EXCEPT
                                                ? `<div class='vp-block-header-except-code-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${that.getState(STATE_exceptCodeLine)}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.BREAK  
                                                ? `<div class='vp-block-header-break-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${that.getState('breakCodeLine')}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.CONTINUE  
                                                ? `<div class='vp-block-header-continue-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${that.getState('continueCodeLine')}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.PASS  
                                                ? `<div class='vp-block-header-pass-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${that.getState('passCodeLine')}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.CODE  
                                                ? `<div class='vp-block-header-custom-code-${blockUUID}'
                                                        style='font-size:12px; color:${COLOR_GRAY_input_your_code};'>
                                                        ${that.getState(STATE_customCodeLine) === STR_NULL
                                                            ? STR_INPUT_YOUR_CODE
                                                            : that.getState(STATE_customCodeLine)}
                                                    </div>`
                                                : STR_NULL
                                        }
                                        ${
                                            blockCodeType === BLOCK_CODELINE_TYPE.RETURN    
                                                ? `<div class='vp-block-header-return-param-${blockUUID}'
                                                            style='font-size:12px;'>
                                                        ${returnOutParamList.length === 0 
                                                                ? ''
                                                                : returnOutParamStr}
                                                    </div>`
                                                : STR_NULL
                                        }
                                            
                                        </div>
                                </div>`);
        return mainHeaderDom;
    }

    var renderBottomOptionContainer = function() {
        return $(`<div class='vp-nodeeditor-style-flex-row-center' 
                       style='padding: 0.5rem;'></div>`);
    }

    var renderBottomOptionContainerInner = function() {
        return $(`<div class='vp-nodeeditor-blockoption 
                            vp-nodeeditor-option'
                       style='width: 95%;'>
                  </div>`);
    }

    var renderDomContainer = function() {
        var domContainer = $(`<div class='vp-nodeeditor-option-container'>
                                        <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                            <span class='vp-block-optiontab-name'>code</span>
                                            <div class='vp-nodeeditor-style-flex-row-center'>
                                                <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
                                            </div>
                                        </div>
                                    </div>`);
        return domContainer;
    }

    var renderBottomOptionInnerDom = function() {
        var innerDom = $(`<div class='vp-nodeeditor-option-container'>
                                    <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                        <span class='vp-block-optiontab-name'>name</span>
                                        <div class='vp-nodeeditor-style-flex-row-center'>
                                            <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
                                        </div>
                                    </div>
                                </div>`);
        return innerDom;
    }

    var renderBottomOptionName = function(that, name, blockCodeType, uuid) {
        var classStr = STR_NULL;
        var resetButton = null;

        if (blockCodeType === BLOCK_CODELINE_TYPE.CLASS) {
            classStr = 'vp-nodeeditor-input-class-name';
            
            /** state className에 문자열이 1개도 없을 때 */
            var classNameState = that.getState(STATE_className);
            if (classNameState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += STR_CSS_CLASS_VP_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.DEF) {
            classStr = 'vp-nodeeditor-input-def-name';

            /** state defName에 문자열이 1개도 없을 때 */
            var defNameState = that.getState(STATE_defName);
            if (defNameState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += STR_CSS_CLASS_VP_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.IF) {
            classStr = 'vp-nodeeditor-if-input';

            /** state ifCodeLine에 문자열이 1개도 없을 때 */
            var ifCodeLineState = that.getState(STATE_ifCodeLine);
            if (ifCodeLineState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += STR_CSS_CLASS_VP_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.FOR) {
            classStr = 'vp-nodeeditor-for-input';

            /** state forCodeLine에 문자열이 1개도 없을 때 */
            var forCodeLineState = that.getState(STATE_forCodeLine);
            if (forCodeLineState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += STR_CSS_CLASS_VP_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.WHILE) {
            classStr = 'vp-nodeeditor-while-input';

            /** state whileCodeLine에 문자열이 1개도 없을 때 */
            var whileCodeLineState = that.getState(STATE_whileCodeLine);
            if (whileCodeLineState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += STR_CSS_CLASS_VP_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.CODE) {
            classStr = 'vp-nodeeditor-code-input';

            /** state codeline에 문자열이 1개도 없을 때 */
            var codeLineState = that.getState(STATE_customCodeLine);
            if (codeLineState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += STR_CSS_CLASS_VP_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.BREAK) {
            classStr = 'vp-nodeeditor-break-input';

            /** state break codeline에 문자열이 1개도 없을 때 */
            var codeLineState = that.getState(STATE_breakCodeLine);
            if (codeLineState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += STR_CSS_CLASS_VP_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
            resetButton = $(`<button class='vp-nodeeditor-option-reset-button vp-block-btn'>Reset</button>`);
            $(resetButton).click(function() {
                that.setState({
                    breakCodeLine: STR_BREAK
                });
                that.renderBottomOption();
                $(`.vp-block-header-break-${that.getUUID()}`).html(that.getState(STATE_breakCodeLine));
            });
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.CONTINUE) {
            classStr = 'vp-nodeeditor-continue-input';

            /** state continue codeline에 문자열이 1개도 없을 때 */
            var codeLineState = that.getState(STATE_continueCodeLine);
            if (codeLineState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += STR_CSS_CLASS_VP_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
            resetButton = $(`<button class='vp-nodeeditor-option-reset-button vp-block-btn'>Reset</button>`);
            $(resetButton).click(function() {
                that.setState({
                    continueCodeLine: STR_CONTINUE
                });
                that.renderBottomOption();
                $(`.vp-block-header-continue-${that.getUUID()}`).html(that.getState(STATE_continueCodeLine));
            });
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.PASS) {
            classStr = 'vp-nodeeditor-pass-input';

            /** state pass codeline에 문자열이 1개도 없을 때 */
            var codeLineState = that.getState(STATE_passCodeLine);
            if (codeLineState === STR_NULL) {
                classStr += STR_ONE_SPACE;
                classStr += STR_CSS_CLASS_VP_NODEEDITOR_OPTION_INPUT_REQUIRED;
            }
            resetButton = $(`<button class='vp-nodeeditor-option-reset-button vp-block-btn'>Reset</button>`);
            $(resetButton).click(function() {
                that.setState({
                    passCodeLine: STR_PASS
                });
                that.renderBottomOption();
                $(`.vp-block-header-pass-${that.getUUID()}`).html(that.getState(STATE_passCodeLine));
            });
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.ELIF) {
            classStr = `vp-nodeeditor-elif-input-${uuid}`;
        }

        var nameDom = $(`<div class='vp-block-blockoption 
                                    vp-nodeeditor-blockoption-block 
                                    vp-nodeeditor-blockoption-inner vp-nodeeditor-style-flex-row' 
                                style='position:relative;'>
                            <input class='vp-nodeeditor-blockoption-input ${classStr}' 
                                value='${name}' 
                                placeholder='input code line' ></input>   
                                                                             
                        </div>`);
                        
        if (resetButton !== null) {
            $(nameDom).append(resetButton);
        }
        return nameDom;
    }

    var renderInParamContainer = function(inParamList, blockCodeType) {
        var classStr = STR_NULL;
        if (blockCodeType === BLOCK_CODELINE_TYPE.CLASS) {
            classStr = `vp-nodeeditor-class-inparam-plus-btn`;
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.DEF) {
            classStr = `vp-nodeeditor-def-inparam-plus-btn`;
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.RETURN) {
            classStr = `vp-nodeeditor-return-outparam-plus-btn`;
        }

        var inParamContainer = $(`<div class='vp-nodeeditor-ifoption-container'>
                                            <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                                <span class='vp-block-optiontab-name'>
                                                    in param</span>
                                                <div class='vp-nodeeditor-style-flex-row-center' >
                                                    <span class='vp-nodeeditor-number 
                                                                 vp-nodeeditor-style-flex-column-center'
                                                        style='margin-right:5px;'>
                                                        ${inParamList.length} Param
                                                    </span>
                                                    <button class='vp-block-btn ${classStr}'
                                                            style='margin-right:5px;'>
                                                        + param
                                                    </button>
                                                    <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
                                                </div>
                                            </div>
                                        </div>`);
        return inParamContainer;
    }

    var renderInParamDom = function(inParam, index, blockCodeType, uuid) {
        var classStr = STR_NULL;
        if (blockCodeType === BLOCK_CODELINE_TYPE.CLASS) {
            classStr = `vp-nodeeditor-input-class-inparam-${index}`;
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.DEF) {
            classStr = `vp-nodeeditor-input-def-inparam-${index}'`;
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.RETURN) {
            classStr = `vp-nodeeditor-return-outparam-${index}`;
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.EXCEPT) {
            classStr = `vp-nodeeditor-except-input-${index}`;
        } else if (blockCodeType === BLOCK_CODELINE_TYPE.ELIF) {
            classStr = `vp-nodeeditor-elif-input-${uuid}`;
        }

        var inParamDom = $(`<div class='vp-nodeeditor-style-flex-row'
                                 style='margin-top:5px;'>
                                <div class='vp-nodeeditor-style-flex-column-center'
                                    style='margin:0 0.5rem; '>
                                    ${index+1}
                                </div>
                                <div class='vp-nodeeditor-blockoption-block
                                            vp-nodeeditor-blockoption-inner vp-nodeeditor-style-flex-row' 
                                        style='position:relative; margin-top:0px;'>
                                    <input placeholder='input param' 
                                           class='vp-nodeeditor-blockoption-input ${classStr}' 
                                           value='${inParam}'>                                                        
                                </div>
                            </div>`);
        return inParamDom;
    }

    var renderBottomOptionTitle = function(title) {
        var titleDom = $(`<div class='vp-nodeeditor-option-container'
                            style='margin-top:5px;'>
                                <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                    <span class='vp-block-optiontab-name'>${title}</span>
                                    <div class='vp-nodeeditor-style-flex-row-center'>
                                        <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
                                    </div>
                                </div>
                            </div>`);
        return titleDom;
    }

    var renderElseBlock = function(that, blockCodeType) {
        var state;
        if (blockCodeType === BLOCK_CODELINE_TYPE.IF) {
            state = that.getState(STATE_isIfElse);
        } else {
            state = that.getState(STATE_isForElse);
        }
 
        var uuid = that.getUUID();
        var elseBlock = $(`<div class='vp-nodeeditor-option-container'
                                style='margin-top:5px;'>
                                <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                    <span class='vp-block-optiontab-name'>else</span>
                                    <div class='vp-nodeeditor-style-flex-row-center'>
                                        <div style='display:flex; margin-right: 5px;'>
                                            <div style='margin-top: 2.5px;
                                                        margin-right: 5px;'>yes</div>
                                            <input class='vp-nodeeditor-else-yes-${uuid}'
                                                style='margin-top: 6px;' 
                                                ${state === true 
                                                        ? 'checked'
                                                        : '' }
                                                type='checkbox'/>
                                        </div>
                                        <div style='display:flex; margin-right: 5px;'>
                                            <div style='margin-top: 2.5px;
                                                        margin-right: 5px;'>no</div>
                                            <input class='vp-nodeeditor-else-no-${uuid}'
                                                style='margin-top: 6px;' 
                                                ${state === false 
                                                        ? 'checked'
                                                        : '' }
                                                type='checkbox'/>
                                        </div>
                                        <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
                                    </div>
                                </div>
                            </div>`);
        return elseBlock;
    }

    var renderDefaultOrDetailButton = function(that, uuid, blockCodeType) {
        var defaultOptionTitle = STR_NULL;
        var detailOptionTitle = STR_NULL;
        if (blockCodeType === BLOCK_CODELINE_TYPE.IMPORT) {
            defaultOptionTitle = `Default Import`;
            detailOptionTitle = `Custom Import`;
        } else {
            defaultOptionTitle = `Default Option`;
            detailOptionTitle = `Detail Option`; 
        }

        var isBaseImportPage = that.getState('isBaseImportPage');
        var defaultOrDetailButton = $(`<div class='vp-nodeeditor-style-flex-row-between'>
                                            <button class='vp-nodeeditor-default-option-${uuid} 
                                                           vp-nodeeditor-default-detail-option-btn
                                                           ${isBaseImportPage === true ? 'vp-nodeeditor-option-btn-selected': ''}'>
                                                    ${defaultOptionTitle}
                                            </button>
                                            <button class='vp-nodeeditor-detail-option-${uuid} 
                                                           vp-nodeeditor-default-detail-option-btn
                                                           ${isBaseImportPage === false ? 'vp-nodeeditor-option-btn-selected': ''}'>
                                                    ${detailOptionTitle}
                                            </button>
                                        </div>`);
        return defaultOrDetailButton;
    }

    var renderInputRequiredColor = function(that) {
        if ($(that).val() === STR_NULL) {
            $(that).addClass('vp-nodeeditor-option-input-required')
        } else {
            $(that).removeClass('vp-nodeeditor-option-input-required'); 
        }
    }

    var renderDeleteButton = function() {
        return $(`<button class='vp-block-btn'>x</button>`);
    }

    var renderCustomImportDom = function(customImportData, index) {
        const { isImport, baseImportName, baseAcronyms } = customImportData;
        var customImportDom = $(`<div class='vp-nodeeditor-style-flex-row-between'>
                                    <div class='vp-nodeeditor-style-flex-column-center'>
                                        <input class='vp-nodeeditor-blockoption-custom-import-input
                                                    vp-nodeeditor-blockoption-custom-import-input-${index}' 
                                            
                                            type='checkbox' 
                                            ${isImport === true ? 'checked': ''}>
                                        </input>
                                    </div>
                                    <select class='vp-nodeeditor-select
                                                    vp-nodeeditor-blockoption-custom-import-select
                                                    vp-nodeeditor-blockoption-custom-import-select-${index}'
                                            style='margin-right:5px;'>
                                        <option value='numpy' ${baseImportName === 'numpy' ? STR_SELECTED: ''}>
                                            numpy
                                        </option>
                                        <option value='pandas' ${baseImportName === 'pandas' ? STR_SELECTED: ''}>
                                            pandas
                                        </option>
                                        <option value='matplotlib' ${baseImportName === 'matplotlib' ? STR_SELECTED: ''}>
                                            matplotlib
                                        </option>
                                        <option value='seaborn' ${baseImportName === 'seaborn' ? STR_SELECTED: ''}>
                                            seaborn
                                        </option>
                                        <option value='os' ${baseImportName === 'os' ? STR_SELECTED: ''}>
                                            os
                                        </option>
                                        <option value='sys' ${baseImportName === 'sys' ? STR_SELECTED: ''}>
                                            sys
                                        </option>
                                        <option value='time' ${baseImportName === 'time' ? STR_SELECTED: ''}>
                                            time
                                        </option>
                                        <option value='datetime' ${baseImportName === 'datetime' ? STR_SELECTED: ''}>
                                            datetime
                                        </option>
                                        <option value='random' ${baseImportName === 'random' ? STR_SELECTED: ''}>
                                            random
                                        </option>
                                        <option value='math' ${baseImportName === 'math' ? STR_SELECTED: ''}>
                                            math
                                        </option>
                                    </select>
                                    <div class='vp-nodeeditor-style-flex-column-center'>
                                        <input class='vp-nodeeditor-blockoption-custom-import-textinput
                                                    vp-nodeeditor-blockoption-custom-import-textinput-${index}
                                                    ${baseAcronyms === '' ? 'vp-nodeeditor-option-input-required' : ''}'
                                                style='width: 90%;' 
                                                type='text' 
                                                placeholder='input import'
                                                value='${baseAcronyms}'></input>
                                    </div>
                                </div>`);
        return customImportDom;
    }

    return {
        renderMainDom
        , renderMainInnerDom
        , renderMainHeaderDom
        , renderBottomOptionContainer
        , renderBottomOptionContainerInner
        , renderDomContainer
        , renderBottomOptionInnerDom
        , renderBottomOptionName
        , renderInParamContainer
        , renderInParamDom
        , renderBottomOptionTitle
        , renderElseBlock
        , renderDefaultOrDetailButton

        , renderInputRequiredColor
        , renderDeleteButton
        , renderCustomImportDom 

        , generateClassInParamList
        , generateDefInParamList
        , generateReturnOutParamList
    }
});
