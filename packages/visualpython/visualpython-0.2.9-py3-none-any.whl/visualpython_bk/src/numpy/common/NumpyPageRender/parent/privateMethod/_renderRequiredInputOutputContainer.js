define ([    
    'nbextensions/visualpython/src/common/vpCommon'
], function( vpCommon ) {

    var _renderRequiredInputOutputContainer = function(numpyPageRendererThis) {
        // var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        // var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        // var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
     
        var rootTagSelector = numpyPageRendererThis.getRootTagSelector();
        var optionPage = $(numpyPageRendererThis.importPackageThis.wrapSelector(rootTagSelector));
        var additionalOptionDomElement = $(`<div class='vp-numpy-requiredPageBlock-view 
                                                        vp-numpy-block '>
                                                <h4>
                                                    <div class='vp-panel-area-vertical-btn vp-arrow-up'></div>
                                                    <span class='vp-multilang' data-caption-id='TODO:Variable'>
                                                        Required Input &amp; Output
                                                    </span>
                                                </h4>
                                            </div>`);

        optionPage.append(additionalOptionDomElement);

    }
    return _renderRequiredInputOutputContainer;
});