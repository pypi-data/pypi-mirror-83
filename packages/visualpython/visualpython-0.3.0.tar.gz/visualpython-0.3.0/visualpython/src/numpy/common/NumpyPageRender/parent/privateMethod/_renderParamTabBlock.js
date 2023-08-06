define ([    
    'nbextensions/visualpython/src/common/vpCommon'
], function( vpCommon ){

    /**
     * @param {Object} tabDataObj 
     *      value1 {string} tabTitle ,
     *      value2 {Array<object>} tabBlockArray
     */
    var renderParamTitle = function(tabDataObj) {
        var tabTitle = tabDataObj.tabTitle;
        var numpyBlock = $(`<div class='vp-numpy-option-block vp-spread' 
                                 id='vp_blockArea'></div`);
        var numpyBlockTitle = $(`<h4>
                                    <span class='vp-multilang' data-caption-id='${tabTitle}'>
                                    * ${tabTitle}
                                    </span>
                                </h4>`);
        numpyBlock.append(numpyBlockTitle);
        return numpyBlock;
    }

    /**
     * @param {Document} numpyBlock 
     * @param {Object} tabDataObj 
     *      value1 {string} tabTitle ,
     *      value2 {Array<object>} tabBlockArray
     * @param {string} uuid 
     */
    var renderParamTabButtonBlock = function( numpyBlock, tabDataObj, uuid) {
        var buttonContainer = $(`<div class='vp-numpy-tab vp-numpy-style-flex-row-around' 
                                      id='vp_numpyTab'></div>`);
        var tabBlockArray = tabDataObj.tabBlockArray;
        for(var i = 0; i < tabBlockArray.length; i++) {
            (function(j) {
                const { btnText } = tabBlockArray[j];
                var buttonDom = $(`<button class='vp-numpy-func_btn vp-numpy-padding-1rem 
                                                  vp-numpyTabBtn-${uuid}-${j+1} black' 
                                    type='button' 
                                    style='display: inline-block;'>
                                        <span class='vp-multilang' 
                                                    data-caption-id='${btnText}'>
                                            ${btnText}
                                        </span>
                                    </button>`);
                buttonContainer.append(buttonDom);
            })(i);
        }
        numpyBlock.append(buttonContainer);
    }

    /**
     * @param {Document} numpyBlock 
     * @param {Object} tabDataObj 
     *      value1 {string} tabTitle ,
     *      value2 {Array<object>} tabBlockArray
     * @param {string} uuid 
     */
    var renderParamTabViewBlock = function(numpyBlock, tabDataObj, uuid) {
        var viewContainer = $(`<div class='vp-numpy-tab' id='vp_numpyTab'>`);
        var tabBlockArray = tabDataObj.tabBlockArray;
        for(var i = 0; i < tabBlockArray.length; i++) {
            (function(j) {
                const { btnText } = tabBlockArray[j];
                var viewDom = $(`<div class='vp-numpy-tab-block-element-${uuid}-${j+1} vp-numpy-tab-block-element-${uuid}' 
                                      id='vp_numpyTabBlock'>
                                        <h4 style='text-align:center;'>
                                            <span class='vp-multilang' data-caption-id='${btnText}'>${btnText}</span>
                                        </h4>
                                        <div class='vp-numpy-tab-block-element-${uuid}-${j+1}-view'>
                                        </div>
                                    </div>`);
                viewContainer.append(viewDom);                    
            })(i);
        }
        numpyBlock.append(viewContainer);
    }

    /**
     * 
     * @param {numpyPageRender this} numpyPageRenderThis 
     * @param {Object} tabDataObj 
     *      value1 {string} tabTitle ,
     *      value2 {Array<object>} tabBlockArray
     * @param {string} uuid 
     */
    var bindParamEditorFunc = function( numpyPageRenderThis, tabDataObj, uuid ) {
        var _mapNumpyPageRenderFunc = function(tagSelector, tabBlockArray) {
            const { bindFuncData } = tabBlockArray;
            const { numpyPageRenderThis, numpyPageRenderFuncType, stateParamNameStrOrStrArray } = bindFuncData;
            const { PARAM_ONE_ARRAY_EDITOR_TYPE, PARAM_TWO_ARRAY_EDITOR_TYPE,
                    PARAM_THREE_ARRAY_EDITOR_TYPE, PARAM_INPUT_EDITOR_TYPE, PARAM_ONE_ARRAY_INDEX_N_EDITOR_TYPE } 
                    = numpyPageRenderThis.numpyEnumRenderEditorFuncType;
     
            switch(numpyPageRenderFuncType){
                case PARAM_ONE_ARRAY_EDITOR_TYPE: {
                    numpyPageRenderThis.renderParamOneArrayEditor(tagSelector, stateParamNameStrOrStrArray);
                    break;
                }
                case PARAM_TWO_ARRAY_EDITOR_TYPE: {
                    numpyPageRenderThis.renderParamTwoArrayEditor(tagSelector, stateParamNameStrOrStrArray);
                    break;
                }
                case PARAM_THREE_ARRAY_EDITOR_TYPE: {
                    numpyPageRenderThis.renderParamThreeArrayEditor(tagSelector, stateParamNameStrOrStrArray);
                    break;
                }
                case PARAM_INPUT_EDITOR_TYPE: {
                    numpyPageRenderThis.renderParamInputArrayEditor(tagSelector, bindFuncData);
                    break;
                }
                case PARAM_ONE_ARRAY_INDEX_N_EDITOR_TYPE: {
                    numpyPageRenderThis.renderParamOneArrayIndexValueEditor(tagSelector, stateParamNameStrOrStrArray);
                    break;
                }

                // case PARAM_INDEXING_EDITOR_TYPE: {
                    // numpyPageRenderThis.renderIndexingEditor(tagSelector, stateParamNameStrOrStrArray);
                    // break;
                // }
            }
        }
        
        var numpyPageRenderThis = numpyPageRenderThis;
        var importPackageThis = numpyPageRenderThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRenderThis.getStateGenerator();
        var tabBlockArray = tabDataObj.tabBlockArray;
        var stateParamOptionName = tabDataObj.stateParamOptionName || 'paramOption';

        for(var i = 0; i < tabBlockArray.length; i++) {
            ( function(j) {
                $(importPackageThis.wrapSelector(`.vp-numpyTabBtn-${uuid}-${j+1}`)).click( function() {
            
                    $(importPackageThis.wrapSelector(`.vp-numpy-tab-block-element-${uuid}`)).css('display','none');
                    $(importPackageThis.wrapSelector(`.vp-numpy-tab-block-element-${uuid}-${j+1}`)).css('display','block');
    
                    $(this).removeClass('vp-numpy-selected');
                    if ($(this).hasClass('vp-numpy-selected')){
                        $(this).removeClass('vp-numpy-selected');
                    } else {
                        $(this).addClass('vp-numpy-selected');
                    }
                    var tagSelector = `.vp-numpy-tab-block-element-${uuid}-${j+1}-view`;
                    _mapNumpyPageRenderFunc(tagSelector, tabBlockArray[j]);

                    numpyStateGenerator.setState({
                        [`${stateParamOptionName}`]: `${j+1}`
                    });
    
                });
            })(i);
        }

        _mapNumpyPageRenderFunc(`.vp-numpy-tab-block-element-${uuid}-1-view`, tabBlockArray[0]);
       
        // html init render  init HTML 초기 설정
        $(importPackageThis.wrapSelector(`.vp-numpy-tab-block-element-${uuid}`)).css('display','none');
        $(importPackageThis.wrapSelector(`.vp-numpy-tab-block-element-${uuid}-1`)).css('display','block');
    }

    /**
     * 
     * @param {numpyPageRender this} numpyPageRenderThis 
     * @param {Object} tabDataObj 
     *      value1 {string} tabTitle ,
     *      value2 {Array<object>} tabBlockArray
     */
    var renderParamTabBlock = function(numpyPageRenderThis, tabDataObj) {
        var uuid = vpCommon.getUUID();
        var numpyPageRenderThis = numpyPageRenderThis
        var importPackageThis = numpyPageRenderThis.getImportPackageThis();
        var rootTagSelector = numpyPageRenderThis.getRequiredPageSelector();
        var mainPage = $(importPackageThis.wrapSelector(rootTagSelector));
    
        var numpyBlock = renderParamTitle(tabDataObj);

        renderParamTabButtonBlock(numpyBlock, tabDataObj, uuid);
        renderParamTabViewBlock(numpyBlock, tabDataObj, uuid);

        mainPage.append(numpyBlock);

        bindParamEditorFunc(numpyPageRenderThis, tabDataObj, uuid);
    }

    return renderParamTabBlock;
});