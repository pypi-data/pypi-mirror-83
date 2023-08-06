define ([    
    'nbextensions/visualpython/src/common/vpCommon'
    ,'nbextensions/visualpython/src/numpy/api/numpyStateApi' 
], function( vpCommon, numpyStateApi ) {
    var { deleteOneArrayIndexValueAndGetNewArray } = numpyStateApi;

    var _renderUserOption = function(numpyPageRendererThis) {
        var uuid = vpCommon.getUUID();
        var numpyPageRendererThis = numpyPageRendererThis;
        var importPackageThis = numpyPageRendererThis.getImportPackageThis();
        var numpyStateGenerator = numpyPageRendererThis.getStateGenerator();

        var rootTagSelector = numpyPageRendererThis.getRootTagSelector();
        var mainPage = $(importPackageThis.wrapSelector(rootTagSelector));

        var userOptionDom = $(`<div class='vp-numpy-block vp-numpy-useroption vp-minimize'>
                                    <h4>
                                        <div class='vp-panel-area-vertical-btn vp-arrow-down'></div>
                                        <span class='vp-multilang' data-caption-id='TODO:Variable'>
                                            User Option
                                        </span>
                                    </h4>
                                    <div id='vp_userOption' class='vp-list-container'>
                                        <table class='vp-tbl-search-result vp-numpy-useroption-table'
                                               style='width:100%;'>
                               
                                        </table>
                                    </div>
                                </div>`);

    
        mainPage.append(userOptionDom);    
        var userOptionTable = $('.vp-numpy-useroption-table');

        var renderUserOptionList = () => {
            $(userOptionTable).empty();

            var colgroup = $(`<colgroup><col width='40%'/><col width='*'/><col width='10%'/></colgroup>`);
            var userOptionTableHeader = $(`<tr>
                                                <th>옵션 키</th>
                                                <th>옵션 값</th>
                                                <th>X</th>
                                            </tr>`);

            userOptionTable.append(colgroup);     
            userOptionTable.append(userOptionTableHeader);     
            for (var i = 0; i < numpyStateGenerator.getState('userOptionList').length; i++) {
                (function(j) {
                    var userOptionBlock = $(` <tr class='vp-numpy-useroption-element-${j}-${uuid}'>
                                            
                                                <td>
                                                    <input class='vp-numpy-input vp-numpy-useroption-key-${j}-${uuid}' 
                                                           style='width: 100%;'
                                                           value='${numpyStateGenerator.getState('userOptionList')[j].optionKey}' type='text'>
                                                </td>
                                                <td>
                                                    <input class='vp-numpy-input vp-numpy-useroption-value-${j}-${uuid}'
                                                           style='width: 100%;'
                                                           value='${numpyStateGenerator.getState('userOptionList')[j].optionValue}' type='text'>
                                                </td>
                                                <td>
                                                    <input class='vp-numpy-useroption-deleteBtn-${j}-${uuid} vp-numpy-func_btn' type='button' value='X'>
                                                </td>
                                            </tr>`);
                    userOptionTable.append(userOptionBlock);
    
    
                    /**
                     *   값 변경
                     */
                    $(importPackageThis.wrapSelector(`.vp-numpy-useroption-key-${j}-${uuid}`)).on('change keyup paste', function() {
                        var updatedIndexValue = $(importPackageThis.wrapSelector(`.vp-numpy-useroption-key-${j}-${uuid}`)).val();
                        numpyStateGenerator.getState('userOptionList')[j].optionKey = updatedIndexValue;
                    });
    
                    $(importPackageThis.wrapSelector(`.vp-numpy-useroption-value-${j}-${uuid}`)).on('change keyup paste', function() {
                        var updatedIndexValue = $(importPackageThis.wrapSelector(`.vp-numpy-useroption-value-${j}-${uuid}`)).val();
                        numpyStateGenerator.getState('userOptionList')[j].optionValue = updatedIndexValue;
                    });
    
                    /**
                     *  값 삭제
                     */
                    $(importPackageThis.wrapSelector(`.vp-numpy-useroption-deleteBtn-${j}-${uuid}`)).click(function() {
                        var deletedParamOneArray = deleteOneArrayIndexValueAndGetNewArray(numpyStateGenerator.getState('userOptionList'),j);
        
                        numpyStateGenerator.setState({
                            userOptionList: deletedParamOneArray
                        });
        
                        renderUserOptionList();
                    });
                })(i);;
            }

            var button = $(`<tr>
                            <td colspan='3'>
                                <input type='button' 
                                        id='vp_addOption' 
                                        class='vp-numpy-useroption-plus-btn vp-numpy-func_btn vp-numpy-padding-1rem'
                                        style='width:100%;' value='옵션 추가'>
                                </td>
                            </tr>`);
            userOptionTable.append(button);

            /** 값 생성*/
            $('.vp-numpy-useroption-plus-btn').click(function() {
                var newData = {
                    optionKey: ''
                    , optionValue: ''
                }
                numpyStateGenerator.setState({
                    userOptionList: [...numpyStateGenerator.getState('userOptionList'), newData]
                });

                renderUserOptionList();    
            });
        }
        renderUserOptionList();
    }

    return _renderUserOption;
});
