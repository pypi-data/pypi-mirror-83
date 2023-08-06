define ([
    // 기본 
    'require'
    // + 추가 python common 폴더 패키지 : 이진용 주임
    , 'nbextensions/visualpython/src/pythonCommon/api/pythonComStateApi'
], function( requirejs
             , pythonComStateApi ) {
    "use strict";
    var { updateOneArrayIndexValueAndGetNewArray } = pythonComStateApi;
    
    /** 데이터를 받아 button dom 태그를 동적 렌더링
     * @param {Array<strong>} btnDataArray 
    */
    var makeBtnDomArray = (btnDataArray) => {
        var btnArray = [];
        btnDataArray.forEach((data, index) => {
            var btn = $(`<button class="vp-pythonCom-func-btn vp-pythonCom-palletteBlock-func-btn-${index}"
                            style="padding: 1rem; font-size:17px;"
                            value="${data}">
                        <span class="vp-multilang" data-caption-id="${data}">${data}</span>
                        </button>`);
            btnArray.push(btn);
        })
        return btnArray;
    }
    
    /**  클릭시 Code Line에 코드가 생성되는 함수
     *  @param { pythonComPageRenderer prototype } pythonComPageRendererThis
     *  @param { object } newData
     */
    var clickPaletteConfirmButton = ( pythonComPageRendererThis, newData ) => {
        var pythonComStateGenerator = pythonComPageRendererThis.pythonComStateGenerator;
        var selectedPaletteIndex = pythonComPageRendererThis.selectedPaletteIndex;
        pythonComStateGenerator.setState({
            paramList: updateOneArrayIndexValueAndGetNewArray( pythonComStateGenerator.getState("paramList"),
                                                                selectedPaletteIndex, 
                                                                newData)    
        });   
        var mRootTagSelector = pythonComPageRendererThis.getRootTagSelector();
        pythonComPageRendererThis.pageRender(mRootTagSelector);
        pythonComPageRendererThis.showGenerateCodeButton();
    }

    /** 클릭시 Code Line에 코드가 생성되는 함수를 bind
     */
    var bindClickPaletteConfirmButton = (pythonComPageRendererThis, palleteBlockState, uuid) => {
        var importPackageThis = pythonComPageRendererThis.importPackageThis;
        var pythonComStateGenerator = pythonComPageRendererThis.pythonComStateGenerator;
        var selectedPaletteIndex = pythonComPageRendererThis.selectedPaletteIndex;
        
        /** 새로운 code line의 token을 생성하고 업데이트 */ 
        $(importPackageThis.wrapSelector(`.vp-pythonCom-func-confirm-btn-${uuid}`)).click(function() {
              
            var newData = palleteBlockState.getPalleteBlockState();
            pythonComStateGenerator.setState({
                paramList: updateOneArrayIndexValueAndGetNewArray( pythonComStateGenerator.getState("paramList"),
                                                                    selectedPaletteIndex, 
                                                                    newData)    
            });   

            var mRootTagSelector = pythonComPageRendererThis.getRootTagSelector();
            pythonComPageRendererThis.pageRender(mRootTagSelector);
            /** 새로운 code line의 token을 생성하고 업데이트 */ 
            /** token 생성 버튼을 codeLine 생성 버튼으로 변경 */ 
            pythonComPageRendererThis.showGenerateCodeButton();
        });
    }

    /** bind back button 클릭
     *  @param { pythonComPageRenderer prototype This } pythonComPageRendererThis
     *  @param { string } uuid
     */
    var bindClickBackButton = (pythonComPageRendererThis, uuid) => {
        var importPackageThis = pythonComPageRendererThis.importPackageThis;
        $(importPackageThis.wrapSelector(`.vp-pythonCom-func-back-btn-${uuid}`)).click(function() {
            pythonComPageRendererThis.renderPaletteView();
        });
    }

    return {
        makeBtnDomArray
        , clickPaletteConfirmButton
        , bindClickBackButton
        , bindClickPaletteConfirmButton
    }
});