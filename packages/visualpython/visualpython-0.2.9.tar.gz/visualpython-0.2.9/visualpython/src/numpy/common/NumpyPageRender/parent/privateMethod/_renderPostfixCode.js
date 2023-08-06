define ([    
    'nbextensions/visualpython/src/common/vpCommon'
], function( vpCommon ) {

    var _renderPostfixCode = function(numpyPageRendererThis) {
        // var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
        var rootTagSelector = numpyPageRendererThis.getRootTagSelector();
        var postfixCodeDomElement = $(`<div class='vp-numpy-block vp-user-option-box vp-minimize'>
                                            <h4>
                                                <div class='vp-panel-area-vertical-btn vp-arrow-down'>
                                                </div>
                                                <span class='vp-multilang' data-caption-id='TODO:Variable'>
                                                    Postfix Code
                                                </span>
                                            </h4>
                                            <div id='vp_postfixBox'>
                                                <textarea class='vp-numpy-textarea vp-numpy-postfix-textarea' 
                                                        placeholder='postfix code' rows='3' cols='60'></textarea>
                                            </div>
                                        </div>`);
        var mainPage = $(importPackageThis.wrapSelector(rootTagSelector));
        mainPage.append(postfixCodeDomElement);

        mainPage.on('focus', '.vp-numpy-postfix-textarea', function() {
            Jupyter.notebook.keyboard_manager.disable();
        });
        mainPage.on('blur', '.vp-numpy-postfix-textarea', function() {
            Jupyter.notebook.keyboard_manager.enable();
        });

        /** postfix Code */
        $(importPackageThis.wrapSelector(`.vp-numpy-postfix-textarea`)).on('change keyup paste', function() {
            numpyStateGenerator.setState({
                postfixCode: $(this).val()
            });
        });
    }
    return _renderPostfixCode;
});