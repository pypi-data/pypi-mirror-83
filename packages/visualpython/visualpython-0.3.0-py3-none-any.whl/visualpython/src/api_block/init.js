define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'

    , './api.js'
    , './constData.js'
    , './blockContainer.js'
    , './createBlockBtn.js'
], function ( $,vpCommon, vpConst, api,constData, blockContainer, createBlockBtn) {
    //FIXME: 추후 소스 전체 리펙토링
    // const { changeOldToNewState
    //     , findStateValue
    //     , mapTypeToName } = api;
    const {BLOCK_CODELINE_BTN_TYPE } = constData;
    const BlockContainer = blockContainer;
    const CreateBlockBtn = createBlockBtn;
    
    var init = function(){
        $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).children(vpConst.OPTION_PAGE).remove();

        var blockContainer = new BlockContainer();
            
        var createBlockBtnArray = Object.values(BLOCK_CODELINE_BTN_TYPE);
        new CreateBlockBtn(blockContainer, BLOCK_CODELINE_BTN_TYPE.CODE);
        createBlockBtnArray.forEach(enumData => {
            if (enumData === BLOCK_CODELINE_BTN_TYPE.API || enumData === BLOCK_CODELINE_BTN_TYPE.CODE) {
                return;
            }
            new CreateBlockBtn(blockContainer, enumData);
        });


        var controlToggleInput = function() {
            $(`.vp-nodeeditor-body`).on("focus", "input", function() {
                Jupyter.notebook.keyboard_manager.disable();
            });
            $(`.vp-nodeeditor-body`).on("blur", "input", function() {
                Jupyter.notebook.keyboard_manager.enable();
            });
        }
        controlToggleInput();
        return blockContainer;
    }

    return init;
});
