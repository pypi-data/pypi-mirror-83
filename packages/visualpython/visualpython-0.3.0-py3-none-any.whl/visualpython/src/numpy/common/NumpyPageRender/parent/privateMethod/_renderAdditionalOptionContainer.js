define ([    
    'nbextensions/visualpython/src/common/vpCommon'
], function( vpCommon ) {

    var _renderAdditionalOptionContainer = function(numpyPageRendererThis) {
        // var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        // var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        // var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
     
        var rootTagSelector = numpyPageRendererThis.getRootTagSelector();
        var optionPage = $(numpyPageRendererThis.importPackageThis.wrapSelector(rootTagSelector));
        var additionalOptionDomElement = $(`<div class='vp-numpy-optionPageBlock-view vp-numpy-block vp-minimize'>
                                                <h4>
                                                    <div class='vp-panel-area-vertical-btn vp-arrow-down'></div>
                                                    <span class='vp-multilang' data-caption-id='TODO:Variable'>
                                                        Additional Options
                                                    </span>
                                                </h4>
                                            </div>`);

        optionPage.append(additionalOptionDomElement);

    }
    return _renderAdditionalOptionContainer;
});