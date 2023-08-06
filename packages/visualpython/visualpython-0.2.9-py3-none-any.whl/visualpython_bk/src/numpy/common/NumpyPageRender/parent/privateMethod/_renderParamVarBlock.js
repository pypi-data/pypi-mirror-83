define ([    
    'nbextensions/visualpython/src/common/vpCommon'
], function( vpCommon ) {
    /** paramVariable 변수 입력 <div> 블록을 동적 렌더링하는 메소드
     * @param {numpyPageRenderer this} numpyPageRendererThis 
     */
    var _renderParamVarBlock = function(numpyPageRendererThis, title) {
        var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
        var rootTagSelector = numpyPageRendererThis.getRequiredPageSelector();
        var paramVarBlock = $(`<div class='vp-numpy-option-block vp-spread' id='vp_blockArea'
                                    style='padding-top:10px;'>

                                    <table style='width: 100%;'>
                                        <tr>
                                            <td style='width: 40%;'>
                                  
                                                <label class='vp-multilang' data-caption-id='InputParameter'
                                                    style='margin-bottom: 0px;'> * ${title || `Input Parameter Variable`}
                                                </label>
                                            </td>
                                            
                                            <td>
                                                <input type='text' class='vp-numpy-input vp-numpy-paramVar-input' 
                                                    id='vp_numpyParamVarInput-${uuid}'
                                                    placeholder='변수 입력'/>
                                            </td>
                                        </tr>
                                    </table>
                                    
                                </div>`);

        var optionPage = $(importPackageThis.wrapSelector(rootTagSelector));
        optionPage.append(paramVarBlock);

        /** paramVariable 변수 입력 */
        $(importPackageThis.wrapSelector(`#vp_numpyParamVarInput-${uuid}`)).on('change keyup paste', function() {
            numpyStateGenerator.setState({
                paramVariable: $(this).val()
            });
        });
    }

    return _renderParamVarBlock;
});
