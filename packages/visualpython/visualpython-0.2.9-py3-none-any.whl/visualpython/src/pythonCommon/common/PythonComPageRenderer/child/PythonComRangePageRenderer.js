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
     * @class PythonComRangePageRenderer
     * @constructor
    */
    var PythonComRangePageRenderer = function(pythonComOptionObj) {
        this.blockViewDom;
    };

    /**
     * PythonComPageRenderer 에서 상속
    */
    PythonComRangePageRenderer.prototype = Object.create(PythonComPageRenderer.prototype);

    /**
    * PythonComRangePageRenderer 클래스의 pageRender 메소드 오버라이드
    * @param {string} tagSelector 
    */
    PythonComRangePageRenderer.prototype.pageRender = function(tagSelector) {
        var uuid = vpCommon.getUUID();
        var pythonComPageRendererThis = this;
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();   
        pythonComPageRendererThis.setRootTagSelector(tagSelector || ".vp-pythonCom-block-view");
        var mRootTagSelector = pythonComPageRendererThis.getRootTagSelector();
        var rootTagDom = $(importPackageThis.wrapSelector(mRootTagSelector));
        rootTagDom.empty();
    
        var firstBlockView = pythonComPageRendererThis._renderPythonComBlockAnGetSelectedViewDom(`Input Range Parameter`);
        var tabTitleArray = ["start", "start, stop", "start, stop, step"];
        var stateParamNameArray = ["param1Start", ["param2Start","param2Stop"], ["param3Start", "param3Stop", "param3Step"]] ;
        
        var tabObj = {
            tabTitleArray
            , stateParamNameArray
        }
        pythonComPageRendererThis._renderTabBlock(firstBlockView, tabObj, uuid);
        pythonComPageRendererThis._renderParamEditorToTab(tabObj, uuid);

        pythonComPageRendererThis._renderReturnVarBlock(uuid);      
 
    }

    return PythonComRangePageRenderer;
})