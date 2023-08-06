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
    var PythonComMakeListPageRenderer = function(pythonComOptionObj) {

    };

    /**
     * PythonComPageRenderer 에서 상속
    */
    PythonComMakeListPageRenderer.prototype = Object.create(PythonComPageRenderer.prototype);

    /**
    * PythonComPageRenderer 클래스의 pageRender 메소드 오버라이드
    * @param {string} tagSelector 
    */
    PythonComMakeListPageRenderer.prototype.pageRender = function(tagSelector) {
        var uuid = vpCommon.getUUID();
        var pythonComPageRendererThis = this;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();   
        pythonComPageRendererThis.setRootTagSelector(tagSelector || ".vp-pythonCom-block-view");

        var firstBlockView = pythonComPageRendererThis._renderPythonComBlockAnGetSelectedViewDom( `Make List`, uuid); 

        pythonComPageRendererThis._renderParamOneArrayEditor(firstBlockView, `paramList`);
        pythonComPageRendererThis._renderReturnVarBlock(uuid);       
    }
    

    return PythonComMakeListPageRenderer;
});
