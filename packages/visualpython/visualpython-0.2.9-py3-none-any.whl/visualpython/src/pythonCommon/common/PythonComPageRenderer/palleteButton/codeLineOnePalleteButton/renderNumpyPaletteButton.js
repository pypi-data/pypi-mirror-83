
define ([
    // 기본 
    'require'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpCommon'
    // + 추가 python common 폴더 패키지 : 이진용 주임
    , 'nbextensions/visualpython/src/common/constant_numpy'
    , 'nbextensions/visualpython/src/numpy/api/numpyRouteMapApi'
    , 'nbextensions/visualpython/src/pythonCommon/api/pythonComStateApi'
], function (requirejs, vpConst, vpCommon,
              vpNumpyConst, numpyRouteMapApi,
             pythonComStateApi ) {

    var { updateOneArrayIndexValueAndGetNewArray } = pythonComStateApi;

   
    
    "use strict";
    var renderNumpyPaletteButton = function(pythonComPageRendererThis, flexRowDiv, typeEnum) {
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var selectedPaletteIndex = pythonComPageRendererThis.getSelectedPaletteIndex();
        vpNumpyConst.NUMPY_FUNCTION_BLUEPRINT_LIST.forEach(npFuncData => {
            var npBtn = $(`<button class="vp-pythonCom-func-btn"
                                        style="padding: 1rem; font-size:12px;">
                                        <span class="vp-multilang" data-caption-id="${npFuncData.funcName}">${npFuncData.funcName}</span>
                                </button>`);
        
            const { newMapFuncIdToNumpyFuncData } = numpyRouteMapApi;                    
            const { numpyCodeGenerator
                , numpyCodeValidator
                , numpyPageRender } = newMapFuncIdToNumpyFuncData(`${npFuncData.funcId}`);

            npBtn.click(function() {
                var uuid = vpCommon.getUUID();
             
                const { paletteContainer
                        , paletteConfirmButton } = pythonComPageRendererThis._renderSelectCodeLineTokenBlockAndConfirmButton(`${npFuncData.funcName}`, uuid);
            
                var paletteBodyView = pythonComPageRendererThis.getPaletteBodyView();
                paletteBodyView.empty();
                paletteBodyView.append(paletteContainer);
                paletteBodyView.append(paletteConfirmButton);
    
                numpyPageRender.setImportPackageThis(importPackageThis);
                numpyPageRender.setPaletteConfirmButton(paletteConfirmButton);
                numpyPageRender.pageRender(`.vp-pythonCom-palette-view-body-container-${uuid}`);

                $(paletteConfirmButton).click(function() {
    
                    var state = numpyPageRender.numpyStateGenerator.getStateAll();
                    if (! numpyCodeValidator.validate(state)) return;
                    numpyCodeGenerator.makeCode();

                    var newData = {
                        type: "NUMPY_FUNCTION"
                        , data: numpyCodeGenerator.getCodeAndClear()
                    }
                    pythonComStateGenerator.setState({
                        paramList: updateOneArrayIndexValueAndGetNewArray( pythonComStateGenerator.getState("paramList"),
                                                                            selectedPaletteIndex, 
                                                                            newData)    
                    });   
                    
                    var mRootTagSelector = pythonComPageRendererThis.getRootTagSelector();
                    var mRootBlockTitle = pythonComPageRendererThis.getRootBlockTitle();
                    pythonComPageRendererThis.pageRender(mRootTagSelector, mRootBlockTitle);
                    pythonComPageRendererThis.showGenerateCodeButton();
                });
                // back 버튼 클릭
                $(importPackageThis.wrapSelector(`.vp-pythonCom-func-back-btn-${uuid}`)).click(function() {
                    pythonComPageRendererThis.renderPaletteView();
                });
            });
                
            flexRowDiv.append(npBtn);
        });
    }
    return renderNumpyPaletteButton;
});
