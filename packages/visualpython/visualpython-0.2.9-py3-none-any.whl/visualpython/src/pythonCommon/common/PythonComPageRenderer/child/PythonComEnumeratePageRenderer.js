define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    // numpy 패키지를 위한 라이브러리import 
    , 'nbextensions/visualpython/src/common/constant_pythonCommon'
    // python Common 패키지를 위한 import 
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComPageRenderer/parent/PythonComPageRenderer'
    , 'nbextensions/visualpython/src/pythonCommon/api/pythonComStateApi'

], function( requirejs, vpCommon, 
             vpPythonCommonConst, PythonComPageRenderer, pythonComStateApi ) {

    var { updateOneArrayIndexValueAndGetNewArray
          , deleteOneArrayIndexValueAndGetNewArray } = pythonComStateApi;
    /**
     * @class PythonComMakeVariablePageRenderer
     * @constructor
    */
    var PythonComEnumeratePageRenderer = function(pythonComOptionObj) {

    };

    /**
     * PythonComPageRenderer 에서 상속
    */
    PythonComEnumeratePageRenderer.prototype = Object.create(PythonComPageRenderer.prototype);

    /**
    * PythonComPageRenderer 클래스의 pageRender 메소드 오버라이드
    * @param {string} tagSelector 
    */
    PythonComEnumeratePageRenderer.prototype.pageRender = function(tagSelector) {
        // 렌더링에 필요한 기본 데이터 get
        var uuid = vpCommon.getUUID();
        var pythonComPageRendererThis = this;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();   
        pythonComPageRendererThis.setRootTagSelector(tagSelector || ".vp-pythonCom-block-view");
        var mRootTagSelector = pythonComPageRendererThis.getRootTagSelector();
        var rootTagDom = $(importPackageThis.wrapSelector(mRootTagSelector));
        rootTagDom.empty();

        // 첫번째 block 렌더링
        var firstBlockView = pythonComPageRendererThis._renderPythonComBlockAnGetSelectedViewDom( `Input enumerate()`,uuid);    
        pythonComPageRendererThis._renderParamOneArrayEditor(firstBlockView, `paramList`);
        // 두번째 block 렌더링
        var secondBlockView = pythonComPageRendererThis._renderPythonComBlockAnGetSelectedViewDom(`Select Data Type`);    
        var tabTitleArray = ["Basic", "To List", "To Tuple"];
        var tabObj = {
            tabTitleArray
        }
        pythonComPageRendererThis._renderTabBlock(secondBlockView, tabObj, uuid);

        // 세번째 block 렌더링
        pythonComPageRendererThis._renderReturnVarBlock(uuid);   

    }
    
    return PythonComEnumeratePageRenderer;
});
