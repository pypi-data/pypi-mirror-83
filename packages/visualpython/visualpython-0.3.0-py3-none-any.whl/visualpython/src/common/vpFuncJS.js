define([
    'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/metaDataHandler'
], function($, vpCommon, md) {
    "use strict";

    /**
     * @class VpFuncJS
     * @constructor
     * @param {funcOptProp} props 기본 속성
     * @param {String} uuid 고유 id
     */
    var VpFuncJS = function(props, uuid) {
        this.setOptionProp(props);
        this.uuid = uuid;
        this.generatedCode = "";
    };

    /**
     @param {funcOptProp} props 기본 속성
     */
    VpFuncJS.prototype.setOptionProp = function(props) {
        this.stepCount = props.stepCount;
        this.funcName = props.funcName;
        this.funcID = props.funcID;
    }

    /**
     * Task Index 셋팅
     * @param {number} idx task sequential index
     */
    VpFuncJS.prototype.setTaskIndex = function(idx) {
        this.taskIdx = idx;
    }

    /**
     * Task Index 확인
     * @returns {number} task sequential index
     */
    VpFuncJS.prototype.getTaskIndex = function() {
        return this.taskIdx;
    }
    
    /**
     * 유효성 검사
     * @param {*} args 
     * @returns {boolean} 유효성 체크
     */
    VpFuncJS.prototype.optionValidation = function(args) {
        console.log("[vpFuncJS.optionValidation] Not developed yet. Need override on child.");
        return false;
    }
    
    /**
     * Python 코드 실행 후 반환 값 전달해 콜백함수 호출
     * @param {String} command 실행할 코드
     * @param {function} callback 실행 완료 후 호출될 callback
     * @param {boolean} isSilent 커널에 실행위한 신호 전달 여부 기본 false
     * @param {boolean} isStoreHistory 커널에 히스토리 채우도록 신호 기본 !isSilent
     * @param {boolean} isStopOnError 실행큐에 예외 발생시 중지 여부 기본 true
     */
    VpFuncJS.prototype.kernelExecute = function(command, callback, isSilent = false, isStoreHistory = !isSilent, isStopOnError = true) {
        Jupyter.notebook.kernel.execute(
            command,
            {
                iopub: {
                    output: function(msg) {
                        var result = String(msg.content["text"]);
                        callback(result);
                    }
                }
            },
            { silent: isSilent, store_history: isStoreHistory, stop_on_error: isStopOnError }
        );
    }

    /**
     * 셀에 소스 추가하고 실행.
     * @param {String} command 실행할 코드
     * @param {boolean} exec 실행여부 기본 false
     */
    VpFuncJS.prototype.cellExecute = function(command, exec) {
        // TODO: Validate 거칠것
        this.generatedCode = command;
        Jupyter.notebook.insert_cell_below('code').set_text(command);
        Jupyter.notebook.select_next();
        this.metaSave();
        if (exec) {
            Jupyter.notebook.execute_cell();

            /**
             * 추가 + 이진용 주임
             * 2020 10 22 한글('코드가 실행되었습니다') -> 영어로 변경('Your code has been executed)
             */
            vpCommon.renderSuccessMessage("Your code has been executed");
        }
    }

    /**
     * 선택자 범위 uuid 안으로 감싸기
     * @param {String} selector 제한할 대상 선택자. 복수 매개 시 uuid 아래로 순서대로 제한됨
     * @returns 감싸진 선택자
     */
    VpFuncJS.prototype.wrapSelector = function(selector) {
        var args = Array.prototype.slice.call(arguments);
        args.unshift("." + this.uuid);
        return vpCommon.wrapSelector.apply(this, args);
    }

    /**
     * append css on option
     * @param {String} url style sheet url
     */
    VpFuncJS.prototype.loadCss = function(url) {
        try {
            var link = document.createElement("link");
            link.type = "text/css";
            link.rel = "stylesheet";
            link.href = requirejs.toUrl(url);
            document.getElementsByClassName(this.uuid)[0].appendChild(link);
        } catch (err) {
            console.log("[vp] Error occurred during load style sheet. Skip this time.");
            console.warn(err.message);
        }
    }

    /**
     * 미리 생성된 코드 실행
     */
    VpFuncJS.prototype.executeGenerated = function() {
        if (this.generatedCode !== "")
            this.cellExecute(this.generatedCode, true);
    }

    
    /**  추가 + 이진용 주임
    * 파일 네비게이션에 이 코드를 사용
     * @param {String} command 실행할 코드
     * @param {function} callback 실행 완료 후 호출될 callback
     * @param {boolean} isSilent 커널에 실행위한 신호 전달 여부 기본 false
     * @param {boolean} isStoreHistory 커널에 히스토리 채우도록 신호 기본 !isSilent
     * @param {boolean} isStopOnError 실행큐에 예외 발생시 중지 여부 기본 true
    */
    VpFuncJS.prototype.kernelExecuteV2 = function(command, callback, isSilent = false, isStoreHistory = !isSilent, isStopOnError = true) {
        Jupyter.notebook.kernel.execute(
            command,
            {
                iopub: {
                    output: function(msg) {
                        var result = msg.content.data['text/plain']; // <- 이 부분을 개선한 kernelExecute 버전2 코드 
                        callback(result);
                    }
                }
            },
            { silent: isSilent, store_history: isStoreHistory, stop_on_error: isStopOnError }
        );
    }

    /**
     * 메타데이터 핸들러 초기화
     */
    VpFuncJS.prototype.initMetaHandler = function() {
        if (this.mdHandler === undefined)
            this.mdHandler = new md.MdHandler(this.funcID);
        return this.mdHandler;
    }

    /**
     * 메타데이터 세이브
     */
    VpFuncJS.prototype.metaSave = function() {
        if (this.package === undefined) return;
        var inputIdList = this.package.input.map(x => x.name);
        // inputIdList = inputIdList.concat(this.package.output.map(x => x.name));
        // inputIdList = inputIdList.concat(this.package.variable.map(x => x.name));
        // FIXME: minju : not existing object mapping error fixed
        if (this.package.output) inputIdList = inputIdList.concat(this.package.output.map(x => x.name));
        if (this.package.variable) inputIdList = inputIdList.concat(this.package.variable.map(x => x.name));
        // generate & save metadata
        this.initMetaHandler();
        
        this.metadata = this.mdHandler.generateMetadata(this, inputIdList);
        this.mdHandler.saveMetadata();
    }

    /**
     * 메타데이터 로드
     * @param {JSON} meta 
     */
    VpFuncJS.prototype.loadMeta = function(funcJS, meta) {
        this.initMetaHandler();

        this.mdHandler.metadata = meta;
        this.mdHandler.loadDirectMdAsTag(funcJS, meta);
    }

    return {'VpFuncJS': VpFuncJS};
});