define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'

    , './constData.js'
    , './init.js'

], function (requirejs, $, vpCommon, vpConst, sb, vpFuncJS, apiBlockConstData, init) {

    const { NUM_DELETE_KEY_EVENT_NUMBER
            , STR_IS_SELECTED
            , STR_MSG_BLOCK_DELETED } = apiBlockConstData;
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "api_block"
        , funcID : "JY1000"  // TODO: ID 규칙 생성 필요
    }

    /**
     * html load 콜백. 고유 id 생성하여 부과하며 js 객체 클래스 생성하여 컨테이너로 전달
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
    var optionLoadCallback = function(callback) {

        // document.getElementsByTagName("head")[0].appendChild(link);
        // 컨테이너에서 전달된 callback 함수가 존재하면 실행.
        if (typeof(callback) === 'function') {
            var uuid = vpCommon.getUUID();
            // 최대 10회 중복되지 않도록 체크
            for (var idx = 0; idx < 10; idx++) {
                // 이미 사용중인 uuid 인 경우 다시 생성
                if ($(vpConst.VP_CONTAINER_ID).find("." + uuid).length > 0) {
                    uuid = vpCommon.getUUID();
                }
            }
            $(vpCommon.wrapSelector(vpConst.OPTION_GREEN_ROOM)).find(vpConst.OPTION_PAGE).addClass(uuid);
            // 옵션 객체 생성
            var ipImport = new ImportPackage(uuid);
            // 옵션 속성 할당.
            ipImport.setOptionProp(funcOptProp);
            // html 설정.
            ipImport.initHtml();
            callback(ipImport);  // 공통 객체를 callback 인자로 전달
        }
    }
    /**
     * html 로드. 
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
    */
    var initOption = function(callback) {
        var htmlUrlPath  = "api_block/index.html";
        vpCommon.loadHtml(vpCommon.wrapSelector(vpConst.OPTION_GREEN_ROOM), htmlUrlPath, optionLoadCallback, callback);
    }

    /**
     * 본 옵션 처리 위한 클래스
     * @param {String} uuid 고유 id
     */
    var ImportPackage = function(uuid) {
        this.uuid = uuid; // Load html 영역의 uuid.
        this.blockContainer = null;
    }
    /**
     * vpFuncJS 에서 상속
    */
    ImportPackage.prototype = Object.create(vpFuncJS.VpFuncJS.prototype);

    /**
     * 유효성 검사
     * @returns 유효성 검사 결과. 적합시 true
    */
    ImportPackage.prototype.optionValidation = function() {
        return true;
    }

    /**
     * html 내부 binding 처리
     */
    ImportPackage.prototype.initHtml = function() {
        var that = this;
        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "api_block/index.css");
        this.blockContainer = init();
    
        // import load css
 
        $('.vp-nodeeditor-tab-click').click( 
            function(event) {
                event.preventDefault();
                $('.vp-nodeeditor-left').css('width','100%');
                $('.vp-nodeeditor-right').animate({width:'toggle'});
            }
        );

        $(`.vp-nodeeditor-panel-area-vertical-btn`).click(function() {
            if ($(this).hasClass(`vp-nodeeditor-arrow-down`)) {
                $(this).removeClass(`vp-nodeeditor-arrow-down`);
                $(this).addClass(`vp-nodeeditor-arrow-up`);
                $(this).html(`▲`);
                $(this).parent().parent().removeClass(`vp-nodeeditor-minimize`);
            } else {
                $(this).removeClass(`vp-nodeeditor-arrow-up`);
                $(this).addClass(`vp-nodeeditor-arrow-down`);
                $(this).html(`▼`);
                $(this).parent().parent().addClass(`vp-nodeeditor-minimize`);
            }
        });

        $(`.vp-nodeeditor-bottom-tab-close-btn`).click(function() {
            $('.vp-nodeeditor-bottom-tab').animate({
                height: '0px'
            });
        });

        $(document).keyup(function(e) {
            var keycode =  e.keyCode 
                                ? e.keyCode 
                                : e.which;
            if(keycode === NUM_DELETE_KEY_EVENT_NUMBER){
                var blockList = that.blockContainer.getBlockList();
                blockList.some(block => {
                    var isSelected = block.getState(STR_IS_SELECTED);
                    if ( isSelected === true ) {
                        // vpCommon.renderSuccessMessage(STR_MSG_BLOCK_DELETED);
                        block.deleteBlockScope();
                        block.renderResetBottomOption();
                        return true;
                    }
                });
            } 
        });
    }

    /**
     *  페이지에 생성된 uuid를 가져온다
     */
    ImportPackage.prototype.getUUID = function() {
        return this.uuid;
    }

    /**
     * 코드 생성
     * @param {boolean} exec 실행여부
     */
    ImportPackage.prototype.generateCode = function(exec) {
        // console.log('generate code');
        // validate code 
        // if (!this.optionValidation()) return;

        // make code

        var result = this.blockContainer.makeCode();
        if (result == null) return "BREAK_RUN"; // 코드 생성 중 오류 발생
        // execute code
        this.cellExecute(result, exec);
    }

    return {
        initOption: initOption
    };
});
