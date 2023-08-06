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
     * @class PythonComCommentPageRenderer
     * @constructor
    */
    var PythonComCommentPageRenderer = function(pythonComOptionObj) {
        this.blockViewDom;
    };

    /**
     * PythonComPageRenderer 에서 상속
    */
    PythonComCommentPageRenderer.prototype = Object.create(PythonComPageRenderer.prototype);

    /**
    * PythonComCommentPageRenderer 클래스의 pageRender 메소드 오버라이드
    * @param {string} tagSelector 
    */
    PythonComCommentPageRenderer.prototype.pageRender = function(tagSelector) {
        var uuid = vpCommon.getUUID();
        var pythonComPageRendererThis = this;      
        var pythonComStateGenerator = pythonComPageRendererThis.getStateGenerator();
        var importPackageThis = pythonComPageRendererThis.getImportPackageThis();   
        pythonComPageRendererThis.setRootTagSelector(tagSelector || ".vp-pythonCom-block-view");
        var mRootTagSelector = pythonComPageRendererThis.getRootTagSelector();
        var rootTagDom = $(importPackageThis.wrapSelector(mRootTagSelector));
        rootTagDom.empty();
        
        var comment = pythonComStateGenerator.getState(`comment`);

        var commentInputBlock = pythonComPageRendererThis._renderPythonComBlockAppendToDom(rootTagDom,`Input Comment`);
        var input = $(`<div>
                        <span class="vp-multilang" data-caption-id="name"> Comment : </span>
                        <input id="vp_pythonCom-input-${uuid}" 
                               style="width:80%;"
                               value="${comment}"
                               type="text">
                        </div>`)
        
        commentInputBlock.append(input);

        $(importPackageThis.wrapSelector(`#vp_pythonCom-input-${uuid}`)).val(comment);
        $(importPackageThis.wrapSelector(`#vp_pythonCom-input-${uuid}`)).on("change keyup paste", function() {
            pythonComStateGenerator.setState({
                comment : $(this).val()
            });
        });

    }

    return PythonComCommentPageRenderer;
})