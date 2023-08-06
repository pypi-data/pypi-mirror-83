define ([    
    'nbextensions/visualpython/src/common/vpCommon'
], function( vpCommon ) {

    /** numpy의 옵션 중 indexValue를 입력하는 블럭을 동적 렌더링하는 메소드
     * numpy의 특정 함수들이 indexValue 옵션을 지정 할 수 도 안할 수도 있다.
     * @param {numpyPageRenderer this} numpyPageRendererThis
     * @param {title} title
     * @param {string || Array<string>} stateParamNameOrArray
    */
    var _renderInputIndexValueBlock = function(numpyPageRendererThis, title, bindFuncData) {
    
        var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var rootTagSelector = numpyPageRendererThis.getRequiredPageSelector();

        var rootPage = $(importPackageThis.wrapSelector(rootTagSelector));
        var indexValueBlock = $(`<div class='vp-numpy-option-block vp-spread' 
                                      id='vp_blockArea'
                                      style='padding-top:10px;'>
                                    <table style='width: 100%;'>
                                        <tr>
                                            <td style='width: 40%;'>
                                                <span>*</span>
                                                <label for='i0' class='vp-multilang' data-caption-id='inputIndex'
                                                    style='margin-bottom: 0px;'> 
                                                    ${title}
                                                </label>
                                            </td>
                                            
                                            <td class='vp-numpy-${uuid}-block'>
                                
                                            </td>
                                        </tr>
                                    </table>
   
                                </div>`);
        rootPage.append(indexValueBlock);

        numpyPageRendererThis.renderParamInputArrayEditor(`.vp-numpy-${uuid}-block`, bindFuncData, false)
    
    }

    return _renderInputIndexValueBlock;
});
