define ([
    // 기본 
    'require'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpCommon'

    // + 추가 component 폴더 패키지 : 이진용 주임
    , 'nbextensions/visualpython/src/component/codeLineArrayEditor/index'
    // + 추가 python common 폴더 패키지 : 이진용 주임
    , 'nbextensions/visualpython/src/pythonCommon/api/pythonComStateApi'
 
    , 'nbextensions/visualpython/src/component/fileNavigation/index'
], function( requirejs, vpConst, vpCommon, 
             codeLineArrayEditor,
             pythonComStateApi,
             fileNavigation ) {
    "use strict";


    var { updateOneArrayIndexValueAndGetNewArray,
          deleteOneArrayIndexValueAndGetNewArray }  = pythonComStateApi;
    /**
     * @class PythonComPageRenderer
     * @constructor
    */

    var PythonComPageRenderer = function() {
        this.importPackageThis;
        this.pythonComStateGenerator;
        this.selectedPaletteIndex = 0;
        this.paletteBodyView;

        this.generateCodeButton;
    }
    /**
    * 자식 클래스에서 반드시! 오버라이드 되는 메소드
    * pyhon common 패키지에서 page를 렌더하는 메소드.
    * @override
    * @param {this} importPackageThis 
    */
    PythonComPageRenderer.prototype.pageRender = function(importPackageThis) {

    }

    /**  페이지에 바인딩된 importPackageThis의 uuid를 가져온다
     */
    PythonComPageRenderer.prototype.getOptionPageUUID = function() {
        var importPackageThis = this.getImportPackageThis();
        return importPackageThis.getUUID();
    }

    /** mapFuncIdToFuncData 함수에서 StateGenerator 인스턴스를 가져오기 위해 실행되는 메소드
     * @override
     * @param {PythonComStateGenerator instance} pythonComStateGenerator 
     */
    PythonComPageRenderer.prototype.setStateGenerator = function(pythonComStateGenerator) {
        this.pythonComStateGenerator = pythonComStateGenerator;
    }

    /** getStateGenerator
     */
    PythonComPageRenderer.prototype.getStateGenerator = function() {
        return this.pythonComStateGenerator;
    }

    /**
    * pageList 폴더의 index.js 파일에서 importPackage 인스턴스의 this를 가져오는 메소드
    * @param {ImportPackage Instance this} importPackageThis 
    */
    PythonComPageRenderer.prototype.setImportPackageThis = function(importPackageThis) {
        this.importPackageThis = importPackageThis;
    }

    /** getImportPackageThis
     */
    PythonComPageRenderer.prototype.getImportPackageThis = function() {
        return this.importPackageThis;
    }

    /**
     * selectedPaletteIndex set하는 메소드
     * @param {ImportPackage Instance this} importPackageThis 
     */
    PythonComPageRenderer.prototype.setSelectedPaletteIndex = function(selectedPaletteIndex) {
        this.selectedPaletteIndex = selectedPaletteIndex;
    }

    /**
    * selectedPaletteIndex를 가져오는 메소드
    */
    PythonComPageRenderer.prototype.getSelectedPaletteIndex = function() {
        return this.selectedPaletteIndex;
    }

    /** paletteBodyView를 set하는 메소드
     * @param {document} paletteBodyView 
     */
    PythonComPageRenderer.prototype.setPaletteBodyView = function(paletteBodyView) {
        this.paletteBodyView = paletteBodyView;
    }

    /** paletteBodyView를 가져오는 메소드
     * @param {document} paletteBodyView 
     */
    PythonComPageRenderer.prototype.getPaletteBodyView = function() {
        return this.paletteBodyView;
    }

    /** pythonComConstData를 set하는 메소드 
     * @param {object} pythonComConstData 
     */
    PythonComPageRenderer.prototype.setPythonComConstData = function(pythonComConstData) {
        this.pythonComConstData = pythonComConstData;
    }

    /** pythonComConstData를 가져오는 메소드 
     */
    PythonComPageRenderer.prototype.getPythonComConstData = function() {
        return this.pythonComConstData
    }

    /** newMapFuncIdToPythonComFuncDataFunction 함수를 가져오는 메소드 
     * newMapFuncIdToPythonComFuncDataFunction는 기존의 PythonCom 패키지에서 
     * 새로운 PythonCom 패키지를 생성하기 위해 필요한 함수
     */
    PythonComPageRenderer.prototype.getNewMapFuncIdToPythonComFuncDataFunction = function() {
        return this.newMapFuncIdToPythonComFuncDataFunction;
    }

    /** newMapFuncIdToPythonComFuncDataFunction 함수를 set하는 가져오는 메소드 
     * newMapFuncIdToPythonComFuncDataFunction는 기존의 PythonCom 패키지에서 
     * 새로운 PythonCom 패키지를 생성하기 위해 필요한 함수
     */
    PythonComPageRenderer.prototype.setNewMapFuncIdToPythonComFuncDataFunction = function(newMapFuncIdToPythonComFuncDataFunction) {
        this.newMapFuncIdToPythonComFuncDataFunction = newMapFuncIdToPythonComFuncDataFunction;
    }

    PythonComPageRenderer.prototype.getRootTagSelector = function() {
        return this.rootTagSelector;
    }
    
    PythonComPageRenderer.prototype.setRootTagSelector = function(rootTagSelector) {
        this.rootTagSelector = rootTagSelector;
    }

    /**
     * Line을 생성하는 버튼을 set하는 메소드
     * @param {document} generateCodeButton 
     * @param {number} currLineNumber 
     * @param {title} currLineNumberCode 
     */
    PythonComPageRenderer.prototype.setGenerateCodeButton = function(generateCodeButton, currLineNumber, currLineNumberCode) {
        this.generateCodeButton = generateCodeButton;
        generateCodeButton.children(`.vp-multilang`).html(`Line ${currLineNumber} 코드 생성`);
        $(generateCodeButton).click(function(){
            vpCommon.renderSuccessMessage(`Line ${currLineNumber} : ${currLineNumberCode || ``}  코드 생성`);
        });
    }

    /**
     *  Line을 생성하는 버튼을 get하는 메소드
     */
    PythonComPageRenderer.prototype.getGenerateCodeButton = function() {
        return this.generateCodeButton;
    }

    /** code Line을 LineArrayView 페이지에 생성하는 버튼을 보여주는 메소드
     */
    PythonComPageRenderer.prototype.showGenerateCodeButton = function() {
        var generateCodeButton = this.getGenerateCodeButton();
        if(generateCodeButton) {
            generateCodeButton.removeClass("hide");
            generateCodeButton.addClass("show");
        }
    
    }

    /** code Line을 LineArrayView 페이지에 생성하는 버튼을 감추는 메소드
     */
    PythonComPageRenderer.prototype.hideGenerateCodeButton = function() {
        if(this.getGenerateCodeButton()) {
            this.generateCodeButton.removeClass("show");
            this.generateCodeButton.addClass("hide");

        }
    }

    /**
     * CodeLineArray 페이지 Line view 블럭 동적 렌더링
     * @param { string } tabTitle 
     * @param { string } uuid 
     */
    PythonComPageRenderer.prototype._renderCodeLineArrayViewBlock = function(tabTitle, uuid) {
        var pythonComPageRendererThis = this;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        var mRootTagSelector = pythonComPageRendererThis.getRootTagSelector();
        var rootTagDom = $(importPackageThis.wrapSelector(mRootTagSelector));
        var largeViewBtn = ``;
        var styleMarginRIght10px = ``;
        var isOpenCodeLineArrayEditorModal = pythonComPageRendererThis.getIsOpenCodeLineArrayEditorModal();
        if(isOpenCodeLineArrayEditorModal === false){
            largeViewBtn = `<button class="vp-pythonCom-func-btn vp-pythonCom-largeView-func-btn"
                                            id="vp_pythonComLargeViewFileNavigationBtn-${uuid}">
                                    <span class="vp-multilang" data-caption-id="save_kor">크게보기</span>
                                 </button>`;
            styleMarginRIght10px = `margin-right:10px;`;
        }

        var viewDom = `<div class="vp-pythonCom-line-view">
                        
                        <div class="vp-pythonCom-style-flex-row-between"
                            style="margin-bottom:10px;">
                            <div class=" vp-pythonCom-style-flex-column-center">
                                <strong class="vp-pythonCom-select-line-number-view">
                                    Select Line :
                                </strong>
                            </div>

                            <div class="vp-pythonCom-style-flex-row-end">
                                <button class="vp-pythonCom-func-btn vp-pythonCom-prevDirectory-func-btn"
                                        style="margin-right:10px;">
                                    <span class="vp-multilang" data-caption-id="prevDirectory">◀</span>
                                </button>
                                <button class="vp-pythonCom-func-btn vp-pythonCom-parentDirectory-func-btn"
                                        style="margin-right:10px;">
                                    <span class="vp-multilang" data-caption-id="parentDirectory">▲</span>
                                </button>
                                <button class="vp-pythonCom-func-btn vp-pythonCom-import-func-btn"
                                        style="margin-right:10px;"
                                        id="vp_pythonComOpenFileNavigationBtn-${uuid}">
                                    <span class="vp-multilang" data-caption-id="import_kor">불러오기</span>
                                </button>
                                <button class="vp-pythonCom-func-btn vp-pythonCom-save-func-btn"
                                        style="${styleMarginRIght10px}"
                                        id="vp_pythonComSaveFileNavigationBtn-${uuid}">
                                    <span class="vp-multilang" data-caption-id="save_kor">저장하기</span>
                                </button>
                                ${largeViewBtn}
                            </div>
                        </div>
                        <div class="vp-pythonCom-line-view-body-${uuid}">

                        </div>
                        <button class="vp-pythonCom-func-btn vp-pythonCom-plus-func-btn">+</button>
                    </div>`;

        var pythonComBlock = $(`<div class="vp-pythonCom-block vp-spread" id="vp_blockArea"></div>`);
        var pythonComBlockTitle = $(`<h4>
                                        <div class="vp-panel-area-vertical-btn vp-arrow-up">
                                        </div>
                                        <span class="vp-multilang" data-caption-id="${tabTitle}">
                                            ${tabTitle}
                                        </span>
                                    </h4>
                                    ${viewDom}`);

        pythonComBlock.append(pythonComBlockTitle);
        rootTagDom.append(pythonComBlock);

        // visualpython파일 불러오기 버튼 클릭
        $(importPackageThis.wrapSelector(`#vp_pythonComOpenFileNavigationBtn-${uuid}`)).click( async function() {
            var loadURLstyle = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH;
            var loadURLhtml = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.SOURCE_PATH + "component/fileNavigation/index.html";
            
            importPackageThis.loadCss( loadURLstyle + "component/fileNavigation.css");

            await $(`<div id="vp_fileNavigation"></div>`)
                    .load(loadURLhtml, () => {

                        $('#vp_fileNavigation').removeClass("hide");
                        $('#vp_fileNavigation').addClass("show");

                        var { vp_init
                              , vp_bindEventFunctions } = fileNavigation;
                    
                        vp_init(importPackageThis, "IMPORT_VisualPython");
                        vp_bindEventFunctions();
                    })
                    .appendTo("#site");
        });

        // visualpython파일 크게보기 버튼 클릭
        $(importPackageThis.wrapSelector(`#vp_pythonComLargeViewFileNavigationBtn-${uuid}`)).click(  function() {
            pythonComPageRendererThis.setTrueIsOpenCodeLineArrayEditorModal();

            var loadURLstyle = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH;
            var loadURLhtml = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.SOURCE_PATH + "component/codeLineArrayEditor/index.html";
            
            importPackageThis.loadCss( loadURLstyle + "component/fileNavigation.css");
            var codeLineArrayEditorDom = $(`<div id="vp_codeLineArrayEditor">
                                            <div class="codeLineArrayEditor-container center-1rem-gray" >
                                                <div class="directoryComponent-closedBtn">X</div>
                                                <div class="codeLineArrayEditor-inner flex-row">
                                                    <div class="directoryComponent-container scrollbar">
                                                    </div>
                                                </div>
                                                <div class="vp-python-com-style-flex-row-center">
                                                    <div class="vp-python-com-style-flex-row">
                                                        <button class="vp-numpy-func_btn vp-pythonCom-codeLineArrayEditor-func-executeCodeBtn" 
                                                                style="width: 100%; padding: 1rem;">
                                                            <span class="vp-multilang" data-caption-id="execute_Code">코드 실행</span>
                                                        </button>
                                                    </div>
                                            
                                                </div>
                                            </div>
                                        </div>`);
            // codeLineArrayEditor
            var mRootTagSelector = pythonComPageRendererThis.getRootTagSelector();
            var rootTagDom = $(importPackageThis.wrapSelector(mRootTagSelector));
            rootTagDom.append(codeLineArrayEditorDom);

            $(importPackageThis.wrapSelector('#vp_codeLineArrayEditor')).removeClass("hide");
            $(importPackageThis.wrapSelector('#vp_codeLineArrayEditor')).addClass("show");

            var { initEditor
                  , bindEventFunctions } = codeLineArrayEditor;
            initEditor(pythonComPageRendererThis);
            bindEventFunctions();
        });
         
        // visualpython파일 저장하기 버튼 클릭
        $(importPackageThis.wrapSelector(`#vp_pythonComSaveFileNavigationBtn-${uuid}`)).click( async function() {
            var loadURLstyle = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH;
            var loadURLhtml = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.SOURCE_PATH + "component/fileNavigation/index.html";
            
            importPackageThis.loadCss( loadURLstyle + "component/fileNavigation.css");
    
            await $(`<div id="vp_fileNavigation"></div>`)
                    .load(loadURLhtml, () => {

                        $('#vp_fileNavigation').removeClass("hide");
                        $('#vp_fileNavigation').addClass("show");

                        var { vp_init
                              , vp_bindEventFunctions} = fileNavigation;
                    
                        vp_init(importPackageThis, "SAVE_VisualPython");
                        vp_bindEventFunctions();
                    })
                    .appendTo("#site");
        });
    }

    /** 새로운 Block을 생성하고 블럭 안의 block view 태그 접근자를 리턴하는 함수
     * @param {string} tabTitle 
     */
    PythonComPageRenderer.prototype._renderPythonComBlockAnGetSelectedViewDom = function(tabTitle) {
        var uuid = vpCommon.getUUID();
        var pythonComPageRendererThis = this;
        var importPackageThis = this.getImportPackageThis();
        var mRootTagSelector = this.getRootTagSelector();
        var rootTagDom = $(importPackageThis.wrapSelector(mRootTagSelector));

        var pythonComBlock = $(`<div class="vp-pythonCom-block vp-spread" id="vp_blockArea"></div>`);
        var pythonComBlockTitle = $(`<h4>
                                        <div class="vp-panel-area-vertical-btn vp-arrow-up">
                                        </div>
                                        <span class="vp-multilang" data-caption-id="${tabTitle}">
                                            ${tabTitle}
                                        </span>
                                    </h4>
                                    <div class="vp-pythonCom-tab-block-element-view-${uuid}
                                        vp-pythonCom-style-flex-column">
                                    </div>`);

        pythonComBlock.append(pythonComBlockTitle);
        rootTagDom.append(pythonComBlock);

        return $(importPackageThis.wrapSelector(`.vp-pythonCom-tab-block-element-view-${uuid}`));
    }

    /** 첫번째 파라미터인 rootTagDom에 새로 생성된 block을 자식태그로 append 시키고
     * 생성된 block안의 block view 태그를 리턴한다
     * @param { document } rootTagDom 
     * @param { string } tabTitle 
     */
    PythonComPageRenderer.prototype._renderPythonComBlockAppendToDom = function(rootTagDom, tabTitle) {
        var uuid = vpCommon.getUUID();

        var pythonComBlock = $(`<div class="vp-pythonCom-block vp-spread" id="vp_blockArea"></div>`);
        var pythonComBlockTitle = $(`<h4>
                                        <div class="vp-panel-area-vertical-btn vp-arrow-up">
                                        </div>
                                        <span class="vp-multilang" data-caption-id="${tabTitle}">
                                            ${tabTitle}
                                        </span>
                                    </h4>
                                    `);
        var pythonComBlockView = $(`<div class="vp-pythonCom-tab-block-element-view-${uuid}
                                        vp-pythonCom-style-flex-column">
                                    </div>`);
        pythonComBlock.append(pythonComBlockTitle)
        pythonComBlock.append(pythonComBlockView);
        rootTagDom.append(pythonComBlock);

        return pythonComBlockView;
    }
    
    /**
     * @param {string}} uuid 
     */
    PythonComPageRenderer.prototype._renderReturnVarBlock = function(uuid) {
        var pythonComPageRendererThis = this;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var rootTagSelector = pythonComPageRendererThis.getRootTagSelector();
        var returnVarBlock  = $(`<div class="vp-numpy-block vp-spread" id="vp_blockArea">
                                    <h4>
                                        <div class="vp-panel-area-vertical-btn vp-arrow-up">
                                        </div>
                                        <span class="vp-multilang" data-caption-id="inputReturnVariable">
                                            Input Return Variable 
                                        </span>
                                    </h4>

                                    <input type="text" class="vp-numpy-return-input" id="vp_numpyReturnVarInput-${uuid}"/>
                                    <div class="vp-numpy-style-flex-row">
                                        <input class="vp-numpy-input-checkbox" id="vp_numpyInputCheckBox-${uuid}" type="checkbox" />
                                        <div class="vp-numpy-input-checkbox-title margin-left-5px">
                                            <span class="vp-multilang" data-caption-id="printReturnVariableMessage">
                                                return 변수 출력
                                            </span>
                                        </div>
                                    </div>
                                </div>`);

        var optionPage = $(importPackageThis.wrapSelector(rootTagSelector));
        optionPage.append(returnVarBlock);

        /** return 변수 입력 */
        $(importPackageThis.wrapSelector(`#vp_numpyReturnVarInput-${uuid}`)).on("change keyup paste", function() {
            pythonComStateGenerator.setState({
                returnVariable: $(this).val()
            });
        });

        /** return 변수 print 여부 선택 */
        $(importPackageThis.wrapSelector(`#vp_numpyInputCheckBox-${uuid}`)).click(function() {
            pythonComStateGenerator.setState({
                isReturnVariable: $(this).is(":checked")
            });
        });                
    }

    /**
    * Select Token 블럭 렌더링 
    * 그리고 Select Token Container와 Token 생성 버튼을 가져온다
    * @param {string} title
    * @param {string} uuid
    */        
    PythonComPageRenderer.prototype._renderSelectCodeLineTokenBlockAndConfirmButton = function(title, uuid) {
        var pythonComPageRendererThis = this;
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        // 배열의 인덱스는 길이보다 1 작다
        var currLineNumber = pythonComStateGenerator.getState(`currLineNumber`);  
        var paletteContainer = $(`<div class="vp-pythonCom-palette-view-body-container-${uuid} 
                                              vp-pythonCom-style-flex-column">
                                    <div class="vp-pythonCom-style-flex-row">
                                        <button class="vp-pythonCom-func-btn 
                                                    vp-pythonCom-func-back-btn 
                                                    vp-pythonCom-func-back-btn-${uuid}">◀</button>
                                        <div class="vp-pythonCom-style-flex-column-center">
                                            <span class="vp-multilang" 
                                                data-caption-id="${title}"
                                                style="font-size: 17px; margin-left:10px;">${title}
                                            </span>
                                        </div>
                                    </div>
                                </div>`);

        var paletteConfirmButton = $(`<button class="vp-pythonCom-func-btn vp-pythonCom-func-confirm-btn-${uuid}" 
                                              style="width:100%;">
                                        <span class="vp-multilang" data-caption-id="confirm"> 
                                            Token 생성
                                        </span>
                                    </button>`);
        return {
            paletteContainer
            , paletteConfirmButton
        }
    }

    /**
     * _renderParamOneArrayEditor
     * 1차원 배열 편진기 렌더링
     * @param {document} oneArrayDom 
     * @param {string} stateParamName 
     */
    PythonComPageRenderer.prototype._renderParamOneArrayEditor = function(oneArrayDom, stateParamName) {
        var pythonComPageRendererThis = this;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();   
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();

        // var oneArrayDom = $(importPackageThis.wrapSelector(tagSelector));
        // 동적 랜더링할 태그에 css flex-column 설정
        oneArrayDom.css("display", "flex");
        oneArrayDom.css("flexDirection", "column");
        // 기존의 렌더링 태그들 리셋하고 아래 로직에서 다시 그림
        oneArrayDom.empty()
        // pythonComPageRendererThis._resetArrayEditor(oneArrayDom);
        // pythonComPageRendererThis._renderParamArrayEditorTitle(oneArrayDom, tagSelector, stateParamName, "JY901");
        // pythonComPageRendererThis._renderEditorModalOpenBtn(oneArrayDom, `vp-numpy-open-oneArray`, "JY901", "row", stateParamName,tagSelector);

        var flexRowDiv = $(`<div class="flex-row"></div>`);
        /**, 
         * pythonComStateGenerator.getState(stateParamName) 배열의 인덱스 갯수만큼 for문 돌아 편집기 생성
         */
        for (var i = 0; i < pythonComStateGenerator.getState(stateParamName).length; i++) {
            (function(j) {
                var oneArrayBlock = $(`<div class="flex-column">
                                            <div class="text-center">${j}</div>
                                            
                                            <input class="vp-numpy-input text-center vp-numpy-array-onearray-${j}-input-${stateParamName}"
                                                value="${pythonComStateGenerator.getState(stateParamName)[j]}" 
                                                style="width:40px;" 
                                                type="text"/>
                                            <button class="vp-numpy-func_btn vp-numpy-array-onearray-${j}-func_deleteBtn-${stateParamName}" 
                                                    style="width:40px;">x</button>
                                        </div>`);
                flexRowDiv.append(oneArrayBlock);
                oneArrayDom.append(flexRowDiv);

                /**
                 *  1차원 배열 값 변경
                 */
                $(importPackageThis.wrapSelector(`.vp-numpy-array-onearray-${j}-input-${stateParamName}`)).on("change keyup paste", function() {
                    var updatedIndexValue = $(importPackageThis.wrapSelector(`.vp-numpy-array-onearray-${j}-input-${stateParamName}`)).val();
                    var updatedParamOneArray = updateOneArrayIndexValueAndGetNewArray(pythonComStateGenerator.getState(stateParamName), j, updatedIndexValue);
    
                    pythonComStateGenerator.setState({
                        [`${stateParamName}`]: updatedParamOneArray
                    });
                });
              
                /**
                 *  1차원 배열 값 삭제
                 */
                $(importPackageThis.wrapSelector(`.vp-numpy-array-onearray-${j}-func_deleteBtn-${stateParamName}`)).click(function() {
                    var deletedParamOneArray = deleteOneArrayIndexValueAndGetNewArray(pythonComStateGenerator.getState(stateParamName),j);
    
                    pythonComStateGenerator.setState({
                        [`${stateParamName}`]: deletedParamOneArray
                    });
    
                    pythonComPageRendererThis._renderParamOneArrayEditor(tagSelector, stateParamName);
       
                });
            })(i);
        }
    
        /**  
         * - 1차원 배열 생성 버튼 삭제 후 다시 추가
         */
        oneArrayDom.parent().find(`.vp-numpy-array-oneArray-func_plusbtn-${stateParamName}`).remove();
        var button = $(`<button class="vp-numpy-func_btn vp-numpy-array-oneArray-func_plusbtn-${stateParamName}" 
                                style="width: 100%; padding: 1rem;">
                                <span  class="vp-multilang" data-caption-id="numpyPlus">+ 추가</span>
                        </button>`);
        oneArrayDom.parent().append(button);
    
        /** - 1차원 배열 생성 클릭 - */
        $(importPackageThis.wrapSelector(`.vp-numpy-array-oneArray-func_plusbtn-${stateParamName}`)).click( function() {
            pythonComStateGenerator.setState({
                [`${stateParamName}`]: [...pythonComStateGenerator.getState(stateParamName), "0"]
            });
            pythonComPageRendererThis._renderParamOneArrayEditor(tagSelector, stateParamName);
        });
    }

    /**
     * @param {document} rootBlockViewDom
     * @param {object} tabObj
     *  tabObj = {
     *      tabTitleArray
     *      , stateParamNameArray
     *  }
     * @param {string} uuid
     */
    PythonComPageRenderer.prototype._renderTabBlock = function(rootBlockViewDom, tabObj, uuid) {
        var pythonComPageRendererThis = this;
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        var rootBlockViewDom = rootBlockViewDom;

        var tabTitleArray = tabObj.tabTitleArray;

        var buttonContainer = $(`<div class="vp-pythonCom-tab vp-pythonCom-style-flex-row" id="vp_pythonComTab"></div>`);
        var tabbuttonContainer = $(`<div class="vp-pythonCom-tab-button vp-pythonCom-style-flex-column" 
                                    id="vp_pythonComTabbutton"></div>`);
        /**
         *  button container 렌더링
         */
        for(var i = 0; i < tabTitleArray.length; i++) {
            (function(j) {
                var viewDom = $(`<div class="vp-pythonCom-tab-button-element-${uuid}-${j+1} vp-pythonCom-tab-button-element-${uuid}" id="vp_numpyTabbutton">
                                        <h4>
                                            <span class="vp-multilang" data-caption-id="${tabTitleArray[j]}">
                                                ${tabTitleArray[j]}
                                            </span>
                                        </h4>
                                        <div class="vp-pythonCom-tab-button-element-${uuid}-${j+1}-view vp-pythonCom-tab-button-element-${uuid}-view">
                                        </div>
                                    </div>`);
                tabbuttonContainer.append(viewDom);                    
            })(i);
        }

        /**
         * button 렌더링
         */
        for(var i = 0; i < tabTitleArray.length; i++) {
            (function(j) {
                var buttonDom = $(`<button class="vp-navi-btn vp-numpyTabBtn-${uuid}-${j+1} black" 
                                            type="button" 
                                            style="display: inline-block;">
                                        <span class="vp-multilang" 
                                                    data-caption-id="${tabTitleArray[j]}">
                                            ${tabTitleArray[j]}
                                        </span>
                                    </button>`);
                buttonDom.click(function(){
                    pythonComStateGenerator.setState({
                        paramOption: `${j+1}`
                    })
                    $(importPackageThis.wrapSelector(`.vp-pythonCom-tab-button-element-${uuid}`)).css("display","none");
                    $(importPackageThis.wrapSelector(`.vp-pythonCom-tab-button-element-${uuid}-${j+1}`)).css("display","block");
                });
                buttonContainer.append(buttonDom);
            })(i);
        }
        rootBlockViewDom.append(buttonContainer);
        rootBlockViewDom.append(tabbuttonContainer);

        // html init render  init HTML 초기 설정
        $(importPackageThis.wrapSelector(`.vp-pythonCom-tab-button-element-${uuid}`)).css("display","none");
        $(importPackageThis.wrapSelector(`.vp-pythonCom-tab-button-element-${uuid}-1`)).css("display","block");
    }

    /** _renderParamEditorToTab
     * @param {object} tabObj
     * tabObj {
     * 
     * } 
     * @param {string} uuid 
     */
    PythonComPageRenderer.prototype._renderParamEditorToTab = function(tabObj, uuid) {
        var pythonComPageRendererThis = this;
        var stateParamNameArray = tabObj.stateParamNameArray
        for(var i = 0; i < stateParamNameArray.length; i++) {
            (function(j) {
                var tabbuttonView = $(`.vp-pythonCom-tab-button-element-${uuid}-${j+1}-view`);
                pythonComPageRendererThis._renderParamInputEditor(tabbuttonView, stateParamNameArray[j]);
            })(i);
        }
    }

    /** 
     * _renderParamInputEditor
     *  @param { document } tabbuttonView 
     *  @param { Array<string> | string } stateParamNameArrayOrStr 
     */ 
    PythonComPageRenderer.prototype._renderParamInputEditor = function(tabbuttonView, stateParamNameArrayOrStr) {
        var pythonComPageRendererThis = this;
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();

        if(Array.isArray(stateParamNameArrayOrStr)){
            for(var i = 0; i < stateParamNameArrayOrStr.length; i++){
                (function(j) {
                    var uuid = vpCommon.getUUID();
                    var inputBlock = $(`<input type="text" class="vp-pythonCom-input" id="vp_${uuid}_input" />`);
            
                    tabbuttonView.append(inputBlock);
            
                    $(importPackageThis.wrapSelector(`#vp_${uuid}_input`)).on("change keyup paste", function() {
                        pythonComStateGenerator.setState({
                            [`${stateParamNameArrayOrStr[j]}`]: $(this).val()
                        });
                    });
                })(i)
            }
        } else {
            var uuid = vpCommon.getUUID();
            var inputBlock = $(`<input type="text" class="vp-pythonCom-input" id="vp_${uuid}input" />`);
            
            tabbuttonView.append(inputBlock);
            $(importPackageThis.wrapSelector(`#vp_${uuid}input`)).on("change keyup paste", function() {
                pythonComStateGenerator.setState({
                    [`${stateParamNameArrayOrStr}`]: $(this).val()
                });
            });
        }
    }

    /** 
     * _renderParamOneArrayIndexValueEditor
     *  @param { document } rootTagDom 
     *  @param { string } stateParamName 
     */
    PythonComPageRenderer.prototype._renderParamOneArrayIndexValueEditor = function(rootTagDom, stateParamName) {
        var pythonComPageRendererThis = this;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();

        rootTagDom.empty();
        /**
         *  배열의 인덱스 갯수만큼 for문 돌아 편집기 생성
         */
        var flexRowBetweenDiv = $(`<div class="flex-row-between"></div>`);
        for (var i = 0; i < pythonComStateGenerator.getState(stateParamName).length; i++) {
            (function(j) {
                var narrayBlock = $(`<div class="flex-row">
                                        <div class="flex-column-center margin-right-5px font-weight-700">
                                            param ${j + 1} : </div> 
                                        <input class="vp-numpy-param-n-${j}-var-input 
                                                      vp-numpy-input" value="${pythonComStateGenerator.getState(stateParamName)[j]}" 
                                                type="text"
                                                placeholder="input param ${j + 1}"/>
                                        <button class="vp-numpy-n-${j}-delete-btn vp-numpy-func_btn">x</button>
                                    </div>`);
                flexRowBetweenDiv.append(narrayBlock);
                rootTagDom.append(flexRowBetweenDiv);

                // 편집기 j번 인덱스의 값 변경
                $(importPackageThis.wrapSelector(`.vp-numpy-param-n-${j}-var-input`)).on("change keyup paste", function() {
                    var updatedIndexValue = $(`.vp-numpy-param-n-${j}-var-input`).val();
                    var updatedParamTwoArray = updateOneArrayIndexValueAndGetNewArray(pythonComStateGenerator.getState(stateParamName), j, updatedIndexValue);
                    pythonComStateGenerator.setState({
                        paletteData: {
                            [`${stateParamName}`]: updatedParamTwoArray
                        }
                    });
                });
                
                // 편집기 j번 인덱스의 값 삭제
                $(importPackageThis.wrapSelector(`.vp-numpy-n-${j}-delete-btn`)).click(function() {
                    pythonComStateGenerator.setState({
                        paramData: {
                            [`${stateParamName}`]: deleteOneArrayIndexValueAndGetNewArray(pythonComStateGenerator.getState(stateParamName),j)
                        }
                    });
                    pythonComPageRendererThis._renderParamOneArrayIndexValueEditor(rootTagDom, stateParamName);
                });
            })(i);
        }
        // +추가 button 생성 
        var button = $(`<button class="vp-numpy-block-empty-shape-n-array-btn 
                                        vp-numpy-func_btn black" 
                                        style="width: 100%; padding: 1rem; margin-top:10px;">
                            <span class="vp-multilang" data-caption-id="numpyPlus">
                                +추가
                            </span>
                        </button>`);

        rootTagDom.append(button);       
 
        // n차원 배열 추가 차원 입력
        $(importPackageThis.wrapSelector(".vp-numpy-block-empty-shape-n-array-btn")).click(function() {
            pythonComStateGenerator.setState({
                paramData:{
                    [`${stateParamName}`]: [...pythonComStateGenerator.getState(stateParamName), ""]
                }
            });
            pythonComPageRendererThis._renderParamOneArrayIndexValueEditor(rootTagDom, stateParamName);
        });
    }

    /** 
     * _renderParamVarBlock
     *  @param { string } title 
     */
    PythonComPageRenderer.prototype._renderParamVarBlock = function(title) {
        var uuid = vpCommon.getUUID();
        var pythonComPageRendererThis = this;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var rootTagSelector = pythonComPageRendererThis.getRootTagSelector();
        var paramVariable = pythonComStateGenerator.getState("paramVariable");
        var paramVarBlock = $(`<div class="vp-numpy-block vp-spread" id ="vp_blockArea">
                                    <h4>
                                        <div class="vp-panel-area-vertical-btn vp-arrow-up">
                                        </div>
                                        <span class="vp-multilang" data-caption-id="InputParameter">
                                            ${`${title || `Input Parameter Variable`}`}
                                        </span>
                                    </h4>

                                    <input type="text" 
                                           value="${paramVariable}"
                                           class="vp-numpy-paramVar-input" 
                                           id="vp_numpyParamVarInput-${uuid}"/>
                                </div>`);

        var optionPage = $(importPackageThis.wrapSelector(rootTagSelector));
        optionPage.append(paramVarBlock);

        // paramVariable 변수 입력
        $(importPackageThis.wrapSelector(`#vp_numpyParamVarInput-${uuid}`)).on("change keyup paste", function() {
            pythonComStateGenerator.setState({
                paramVariable: $(this).val()
            });
        });
    }

    return PythonComPageRenderer;
});
