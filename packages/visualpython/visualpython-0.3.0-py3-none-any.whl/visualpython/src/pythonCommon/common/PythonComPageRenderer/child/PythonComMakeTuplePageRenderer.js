define ([
    'require'
    , 'nbextensions/visualpython/src/common/vpCommon'
    // numpy 패키지를 위한 라이브러리import 
    , 'nbextensions/visualpython/src/common/constant_pythonCommon'
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComPageRenderer/parent/PythonComPageRenderer'
], function( requirejs, vpCommon, 
             vpPythonCommonConst, PythonComPageRenderer ) {
    "use strict";

    /**
     * @class PythonComMakeTuplePageRenderer
     * @constructor
    */
    var PythonComMakeTuplePageRenderer = function(pythonComOptionObj) {

    };

    /**
     * PythonComPageRenderer 에서 상속
    */
    PythonComMakeTuplePageRenderer.prototype = Object.create(PythonComPageRenderer.prototype);

    /**
    * PythonComPageRenderer 클래스의 pageRender 메소드 오버라이드
    * @param {string} tagSelector 
    */
    PythonComMakeTuplePageRenderer.prototype.pageRender = function(tagSelector) {
        var uuid = vpCommon.getUUID();
        var pythonComPageRendererThis = this;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();   
        pythonComPageRendererThis.setRootTagSelector(tagSelector || ".vp-pythonCom-block-view");
        
        var blockView = pythonComPageRendererThis._renderPythonComBlockAnGetSelectedViewDom(`Make Tuple`);    
        
        pythonComPageRendererThis._renderReturnVarBlock(uuid);      
    }

    return PythonComMakeTuplePageRenderer;
})