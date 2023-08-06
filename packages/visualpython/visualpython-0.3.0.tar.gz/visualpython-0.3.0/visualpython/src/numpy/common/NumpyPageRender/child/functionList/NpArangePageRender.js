define ([
    'nbextensions/visualpython/src/numpy/common/NumpyPageRender/parent/NumpyPageRender'
], function(  NumpyPageRender ) {

    'use strict';
    /**
     * @class NpArangePageRender
     * @constructor
    */
    var NpArangePageRender = function(numpyOptionObj) {
        const { numpyDtypeArray, numpyEnumRenderEditorFuncType } = numpyOptionObj;
        this.numpyDtypeArray = numpyDtypeArray;
        this.numpyEnumRenderEditorFuncType = numpyEnumRenderEditorFuncType;

        NumpyPageRender.call(this);
    };

    /**
     * NumpyPageRender 에서 상속
    */
    NpArangePageRender.prototype = Object.create(NumpyPageRender.prototype);

    /**
    * NumpyPageRender 클래스의 pageRender 메소드 오버라이드
    * @param {this} importPackageThis 
    */
    NpArangePageRender.prototype.pageRender = function(tagSelector) {
        this.rootTagSelector = tagSelector || this.getMainPageSelector();
        var numpyPageRenderThis = this;
        var numpyStateGenerator = this.numpyStateGenerator;
        const { PARAM_INPUT_EDITOR_TYPE } = this.numpyEnumRenderEditorFuncType;
        // state의 paramData 객체의 키값을 string 배열로 리턴
        var stateParamNameStrArray = Object.keys(numpyStateGenerator.getState('paramData'));
        var tabTitle = 'Input Parameter';
        var tabBlockArray = [
            {
                tabNumber: 1
                , btnText: 'start'
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
                    , stateParamNameStrOrStrArray: [stateParamNameStrArray[0]]
                    , paramNameStrArray: ['start']
                    , placeHolderArray: ['숫자 입력']
                }
            },
            {
                tabNumber: 2
                , btnText: 'Start, Stop'
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
                    , stateParamNameStrOrStrArray: [ stateParamNameStrArray[1], stateParamNameStrArray[2]]
                    , paramNameStrArray: ['start', 'stop']
                    , placeHolderArray: ['숫자 입력', '숫자 입력']
                }
           
            },
            {
                tabNumber: 3
                , btnText: 'Start, Stop, Step'
                , bindFuncData: {
                    numpyPageRenderThis: numpyPageRenderThis
                    , numpyPageRenderFuncType: PARAM_INPUT_EDITOR_TYPE
                    , stateParamNameStrOrStrArray:  [ stateParamNameStrArray[3], stateParamNameStrArray[4], stateParamNameStrArray[5]]
                    , paramNameStrArray: ['start', 'stop', 'step']
                    , placeHolderArray: ['숫자 입력', '숫자 입력', '숫자 입력']
                }
            
            }
        ];
        var tabDataObj = {
            tabTitle,
            tabBlockArray
        }

        this.renderPrefixCode();

        this.renderRequiredInputOutputContainer();
        this.renderParamTabBlock(tabDataObj);

        this.renderAdditionalOptionContainer();
        this.renderDtypeBlock();
        this.renderReturnVarBlock();

        /** userOption 창 */
        this.renderUserOption();

        this.renderPostfixCode();
    }

    return NpArangePageRender;
});
