

define ([
    // 기본 
    'require'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpCommon'
    // + numpy 폴더 패키지
    , 'nbextensions/visualpython/src/common/constant_numpy'
    , 'nbextensions/visualpython/src/common/constant_pythonCommon'
    , 'nbextensions/visualpython/src/numpy/api/numpyRouteMapApi'
    
    // + 추가 python common 폴더 패키지 : 이진용 주임
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComPageRenderer/parent/PythonComPageRenderer'
    , 'nbextensions/visualpython/src/pythonCommon/api/pythonComStateApi'
    , '../palleteBlock/index'
    , '../palleteButton/index'
], function( requirejs, vpConst, vpCommon
         , vpNumpyConst,vpPythonCommonConst, numpyRouteMapApi
         , PythonComPageRenderer, pythonComStateApi, palleteBlockList, palleteButtonList ) {
    "use strict";

    var { renderAssignOperatorPaletteButton, renderLeftBracketPaletteButton, renderRightBracketPaletteButton,
        renderConditionOperatorPalleteButton, renderCalculationOperatorPaletteButton, renderInputVarPaletteButton,
        renderNumpyPaletteButton } = palleteButtonList;
   
    /**
     * @class PythonComCodeLinePageRenderer
     * @constructor
    */
    var PythonComCodeLinePageRenderer = function(pythonComOptionObj) {
        // this.tokenConfirmButton;
        // this.generateCodeButton;
        // this.generateCodeButton;
        PythonComPageRenderer.call(this);
    };

    /**
     * PythonComPageRenderer 에서 상속
    */
    PythonComCodeLinePageRenderer.prototype = Object.create(PythonComPageRenderer.prototype);

    PythonComCodeLinePageRenderer.prototype.setRootBlockTitle = function(title) {
        this.title = title;
    }
    PythonComCodeLinePageRenderer.prototype.getRootBlockTitle = function() {
        return this.title;
    }
    /**
    * PythonComPageRenderer 클래스의 pageRender 메소드 오버라이드
    * @param {string} tagSelector 
    * @param {string} title
    */
    PythonComCodeLinePageRenderer.prototype.pageRender = function(tagSelector, title) {
        var uuid = vpCommon.getUUID();
        var pythonComPageRendererThis = this;
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();   

        pythonComPageRendererThis.setRootTagSelector(tagSelector || ".vp-pythonCom-block-view");
        var mRootTagSelector = pythonComPageRendererThis.getRootTagSelector();
        pythonComPageRendererThis.setRootBlockTitle(title);

        var mRootBlockTitle = pythonComPageRendererThis.getRootBlockTitle();

        var rootTagDom = $(importPackageThis.wrapSelector(mRootTagSelector));
        rootTagDom.empty();

        var firstBlockView = pythonComPageRendererThis._renderPythonComBlockAnGetSelectedViewDom(mRootBlockTitle || `Edit Code Line`);
        // firstBlockView.addClass("scrollbar");
        var selectTokenBlockView = pythonComPageRendererThis._renderPythonComBlockAnGetSelectedViewDom(`Select Token`);
        pythonComPageRendererThis.setPaletteBodyView(selectTokenBlockView);

        var flexRow = $(`<div class="scrollbar vp-pythonCom-style-flex-row"
                                     style="overflow-x: auto;"></div>`);

        for(var i = 0; i < pythonComStateGenerator.getState("paramList").length; i++) {
            (function(j){
                var palleteData = pythonComStateGenerator.getState("paramList")[j];
                pythonComPageRendererThis._renderMapPalleteTypeToSelectPalleteDom(palleteData, flexRow, firstBlockView, j);
            })(i);
        }

        var button = $(`<button class="vp-pythonCom-func-btn vp-pythonCom-plus-func-btn">
                            <span>+추가</span>
                        </button>`);
        firstBlockView.append(button);

        // code Line Token 추가
        $(button).click(function(){
            pythonComStateGenerator.setState({
                paramList: [...pythonComStateGenerator.getState("paramList"), {type:"UNDEFINED", data:"UN"}]
            });
            var mRootBlockTitle = pythonComPageRendererThis.getRootBlockTitle();
            pythonComPageRendererThis.pageRender(mRootTagSelector, mRootBlockTitle);

            // 최신 token number를 가져오고 Select Token PaletteView를 렌더링함
            var lastTokenNumber = pythonComStateGenerator.getState("paramList").length - 1;
            pythonComPageRendererThis.setSelectedPaletteIndex(lastTokenNumber);
            pythonComPageRendererThis.renderPaletteView();
        });
    }

    PythonComCodeLinePageRenderer.prototype._renderMapPalleteTypeToSelectPalleteDom = function(palleteData, flexRow, blockView, index) {
        var pythonComPageRendererThis = this;
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();
        var uuid = vpCommon.getUUID();

        var type = palleteData.type;
        var data = ``;
        var style = ``;

        var btnName = `change`;
        switch(type){
            // 처음 생성하고 아무값도 입력하지 않았을 때
            case "UNDEFINED" :{
                style = "color:white;";
                btnName = `Select`;
                data = ``;
                break;
            }
            // 타입이 있을 경우
            default: {
                data = palleteData.data;
                break;
            }
        }

        var tokenIndexDataDom = $(`<div class="vp-pythonCom-style-flex-column">
                                        <span class="vp-multilang vp-pythonCom-style-flex-row-center" 
                                            style="font-size:15px; white-space: nowrap; ${style}"
                                            data-caption-id="${palleteData.data}">${palleteData.data}</span>
                                        <button class="vp-pythonCom-func-btn vp-pythonCom-changePallete-func-btn-${uuid}-${index + 1}"
                                                style="font-size:10px;">
                                            <span class="vp-multilang" data-caption-id="${index + 1}">${index + 1}</span>
                                        </button>
                                        <button class="vp-pythonCom-func-btn vp-pythonCom-deletePallete-func-btn-${uuid}-${index + 1}"
                                                style="font-size:10px;">
                                            <span class="vp-multilang" data-caption-id="X">X</span>
                                        </button>
                                    </div>`);
        flexRow.append(tokenIndexDataDom);
        blockView.append(flexRow);

        /**code line Token index j번째 changeToken 클릭  view 렌더링  */ 
        $(importPackageThis.wrapSelector(`.vp-pythonCom-changePallete-func-btn-${uuid}-${index + 1}`)).click(function() {
            pythonComPageRendererThis.setSelectedPaletteIndex(index);
            pythonComPageRendererThis.renderPaletteView();
        });

        /** code line Token index j번째 값 제거 */ 
        $(importPackageThis.wrapSelector(`.vp-pythonCom-deletePallete-func-btn-${uuid}-${index + 1}`)).click(function() {
            pythonComStateGenerator.setState({
                paramList: [ ...pythonComStateGenerator.getState("paramList").slice(0, index),
                            ...pythonComStateGenerator.getState("paramList").slice(index+1, pythonComStateGenerator.getState("paramList").length)]
            });
            var mRootBlockTitle = pythonComPageRendererThis.getRootBlockTitle();
            var mRootTagSelector = pythonComPageRendererThis.getRootTagSelector();
            pythonComPageRendererThis.pageRender(mRootTagSelector, mRootBlockTitle);
        });        
    }

    PythonComCodeLinePageRenderer.prototype.renderPaletteView = function() {
        var pythonComPageRendererThis = this;
        var pythonComConstData = pythonComPageRendererThis.getPythonComConstData();
        
        pythonComPageRendererThis.hideGenerateCodeButton();

        
        const { PYTHON_COMMON_GENERATE_CODE_MAKE_VARIABLE_ENUM } = pythonComConstData;
        const { ASSIGN_OPERATOR_TYPE, LEFT_BRACKET_TYPE, RIGHT_BRACKET_TYPE, 
                DATA_VARIABLE_TYPE, DATA_NUMBER_TYPE, DATA_STRING_TYPE,
                DATA_LIST_TYPE, DATA_DICTIONARY_TYPE, DATA_TUPLE_TYPE, DATA_SET_TYPE , NUMPY_FUNCTION_TYPE, NUMPY_INSTANCE_FUNCTION_TYPE,
                CONDITION_OPERATOR_TYPE, CALCULATION_OPERATOR_TYPE } = PYTHON_COMMON_GENERATE_CODE_MAKE_VARIABLE_ENUM;

        var selectedPaletteIndex = pythonComPageRendererThis.getSelectedPaletteIndex();
        var paletteBodyView = pythonComPageRendererThis.getPaletteBodyView();
        paletteBodyView.empty();

        var paletteContainer = $(`<div>
                                    <div class="vp-pythonCom-style-flex-column">
                                        <span class="vp-multilang" data-caption-id="Select_Line">
                                            <strong>Select Token</strong> : ${selectedPaletteIndex + 1}
                                        </span>

                                    </div>
                                </div>`);

        var flexRowDiv = $(`<div class="vp-pythonCom-style-flex-row-evenly"
                                style="margin:10px 0;"></div>`);

        var conditionOperatorButton = renderConditionOperatorPalleteButton(pythonComPageRendererThis);
        var calculationOperatorButton = renderCalculationOperatorPaletteButton(pythonComPageRendererThis);
        var assignOperatorButton = renderAssignOperatorPaletteButton(pythonComPageRendererThis);
        var leftBracketButton = renderLeftBracketPaletteButton(pythonComPageRendererThis);
        var rightBracketButton = renderRightBracketPaletteButton(pythonComPageRendererThis);

        var flexRowDiv2 = $(`<div class="vp-pythonCom-style-flex-row-evenly"
                                style="margin:10px 0;"></div>`);
        var inputVarButton = renderInputVarPaletteButton(pythonComPageRendererThis, DATA_VARIABLE_TYPE);
        var inputNumberButton = renderInputVarPaletteButton(pythonComPageRendererThis, DATA_NUMBER_TYPE);
        var inputStringButton = renderInputVarPaletteButton(pythonComPageRendererThis, DATA_STRING_TYPE);
        var inputListButton = renderInputVarPaletteButton(pythonComPageRendererThis, DATA_LIST_TYPE);

        var flexRowDiv3 = $(`<div class="vp-pythonCom-style-flex-row-evenly"
                                style="margin:10px 0;"></div>`);
        var inputDictionaryButton = renderInputVarPaletteButton(pythonComPageRendererThis, DATA_DICTIONARY_TYPE);
        var inputTupleButton = renderInputVarPaletteButton(pythonComPageRendererThis, DATA_TUPLE_TYPE);
        var inputSetButton = renderInputVarPaletteButton(pythonComPageRendererThis, DATA_SET_TYPE);

        var flexRowDiv4 = $(`<div class="vp-pythonCom-style-flex-row-evenly"
                                    style="margin:10px 0;"></div>`);  

        renderNumpyPaletteButton(pythonComPageRendererThis, flexRowDiv4, NUMPY_FUNCTION_TYPE);


        flexRowDiv.append(conditionOperatorButton);
        flexRowDiv.append(calculationOperatorButton);
        flexRowDiv.append(assignOperatorButton);
        flexRowDiv.append(leftBracketButton);
        flexRowDiv.append(rightBracketButton);

        flexRowDiv2.append(inputVarButton);
        flexRowDiv2.append(inputNumberButton);
        flexRowDiv2.append(inputStringButton);
        flexRowDiv2.append(inputListButton);

        flexRowDiv3.append(inputDictionaryButton);
        flexRowDiv3.append(inputTupleButton);
        flexRowDiv3.append(inputSetButton);

        paletteContainer.append(flexRowDiv);       
        paletteContainer.append(flexRowDiv2);    
        paletteContainer.append(flexRowDiv3);         
        paletteContainer.append(flexRowDiv4);    
        paletteBodyView.append(paletteContainer);
    }

    return PythonComCodeLinePageRenderer;
});
