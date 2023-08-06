define ([    
    'nbextensions/visualpython/src/common/vpCommon'
], function( vpCommon ) {
    /** 
     * return 변수를 편집하는 html태그를 동적 렌더링
     * @param {numpyPageRenderer this} numpyPageRendererThis 
     */
    var _renderReturnVarBlock = function(numpyPageRendererThis) {
        var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;

        /**
         * return 변수 동적 태그 블럭
         */
 
        var returnVarBlock  = $(`<div class='vp-numpy-option-block vp-spread' id='vp_blockArea'
                                      style='padding-top: 10px;'>
                                    <table style='width: 100%;'>
                                    <tr>
                                        <td style='width: 40%;'>
                                            <label class='vp-multilang' data-caption-id='inputReturnVariable'
                                                   style='margin-bottom: 0px;'> 
                                                Input Return Variable
                                            </label>
                                        </td>
                                        
                                        <td>
                                            <input type='text' class='vp-numpy-input vp-numpy-return-input' 
                                                    id='vp_numpyReturnVarInput-${uuid}'
                                                    placeholder='변수 입력'/>
                                        </td>
                                    </tr>
                                </table>
                                </div>`);
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();
       
        var optionPageSelector = numpyPageRendererThis.getOptionPageSelector();
        var optionPage = $(importPackageThis.wrapSelector(optionPageSelector));
        optionPage.append(returnVarBlock);

        /** return 변수 입력 */
        $(importPackageThis.wrapSelector(`#vp_numpyReturnVarInput-${uuid}`)).on('change keyup paste', function() {
            numpyStateGenerator.setState({
                returnVariable: $(this).val()
            });
        });

        // return 변수 print 여부 선택
        $(importPackageThis.wrapSelector(`#vp_numpyInputCheckBox-${uuid}`)).click(function() {
            numpyStateGenerator.setState({
                isReturnVariable: $(this).is(':checked')
            });
        });                
    }

    return _renderReturnVarBlock;
});