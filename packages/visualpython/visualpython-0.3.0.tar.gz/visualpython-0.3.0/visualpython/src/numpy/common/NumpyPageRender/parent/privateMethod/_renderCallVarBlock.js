define ([    
    'nbextensions/visualpython/src/common/vpCommon'
], function( vpCommon ) {

    /** CALL(호출) 변수를 입력하는 <div> 블럭 동적 렌더링
     * @param {numpyPageRenderer this} numpyPageRendererThis 
     */
    var _renderCallVarBlock = function(numpyPageRendererThis) {
        var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        var callVarBlock  = $(`<div class='vp-numpy-option-block vp-spread'
                                    style='padding-top: 10px;' id ='vp_blockArea'>                  
                                        <table style='width: 100%;'>
                                            <tr>
                                                <td style='width: 40%;'>
                                                    
                                                    <label for='i0' class='vp-multilang' data-caption-id='InputCallVariable'
                                                           style='margin-bottom: 0px;'> 
                                                        * Input Call Variable
                                                    </label>
                                                </td>
                                                <td>
                                                <input type='text' class='vp-numpy-input 
                                                                vp-numpy-callVar-input' 
                                                        id='vp_numpyCallVarInput-${uuid}'
                                                        placeholder='변수 입력'/>
                                                </td>
                                            </tr>
                                        </table>
                                </div>`);
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();

        var rootTagSelector = numpyPageRendererThis.getRequiredPageSelector();
        var optionPage = $(importPackageThis.wrapSelector(rootTagSelector));
        optionPage.append(callVarBlock);

        /** call 변수 입력 */
        $(importPackageThis.wrapSelector(`#vp_numpyCallVarInput-${uuid}`)).on('change keyup paste', function() {
            numpyStateGenerator.setState({
                callVariable: $(this).val()
            });
        });
    }

    return _renderCallVarBlock;
});