define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpXMLHandler'
], function (requirejs, $, vpCommon, vpConst, xmlHandler) {
    "use strict";
    
    /**
     * FIXME: 개발 임시 로그.
     * @param {String} str 로그 내용
     * @param {boolean} alrt 알림 사용 여부(true : 알림)
     */
    var mylog = function(str, alrt = false) {
        console.log("Log in vp cont >>> " + str);
        if (alrt) {
            alert(str);
        }
    }

    /**
     * FIXME: 임시 테스트. 삭제요망
     */
    var myTest = function(index) {
        
    }

    /**
     * FIXME: 임시 테스트. 삭제요망
     */
    $(document).on("click", vpCommon.wrapSelector("#vp_DevTest"), function() {
        console.log(dynamicFuncJS.length);
        dynamicFuncJS.forEach(function(js) {
            console.log(js);
        });
    });

    /* 전역 변수 영역 */
    // 로드된 Option js.
    let dynamicFuncJS = new Array();
    let tempFuncJS;
    let taskIndex = 0;
    var vpDivisionStyle;
    var events;
    let _CUR_PAGE_INDEX = -1;
    let sb = requirejs(vpConst.BASE_PATH + vpConst.SOURCE_PATH + "common/StringBuilder");
    let xmlLibraries;
    let librarySearchComplete = new Array();
    let sortList;

    try {
        // events 에 대한 예외 발생 가능할 것으로 예상.
        events = requirejs('base/js/events');
    } catch (err) {
        if (window.events === undefined) {
            var Events = function () { };
            window.events = $([new Events()]);
        }
        events = window.events;
    }

    /* 이벤트 영역 */
    /**
     * 컨테이너 사이즈 변경시 division resize
     */
    events.on('resize-container.vp-wrapper', function() {
        // mylog("?");
        calculateDivisionWidth();
    });
    
    /**
     * 변수 추가 이벤트 발생시 (그리드 업데이트)
     */
    events.on('add-variable.vp-wrapper', function(varName, varType) {
        addVariableItem(varName, varType);
    });
    
    /**
     * 커널 사용 가능시 상태 표시
     */
    events.on('kernel_idle.Kernel', function () {
        setKernelIdle();
    });
    
    /**
     * 커널 사용 불가능시 상태 표시
     */
    events.on('kernel_busy.Kernel', function () {
        setKernelBusy();
    });

    /**
     * 검색버튼 클릭 이벤트 바인딩
     */
    $(document).on("click", vpCommon.wrapSelector("#vp_searchLibrary"), function() {
        searchLibrary();
    });

    /**
     * 검색어창 엔터 클릭시 조회
     */
    $(document).on("keydown", vpCommon.wrapSelector("#vp_inpSearchLibrary"), function (key) {
        if(key.keyCode == 13){
            searchLibrary();
        }
    });

    /**
     * 검색결과 클릭시 옵션 로드
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.SEARCH_RESULT_ITEM_CLASS), function() {
        loadOption($(this).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, "")));
    });

    $(document).on("click", vpCommon.wrapSelector(vpConst.NAVIGATOR_PATH_ITEM_CLASS), function() {
        naviPathHandling($(this).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, "")));
        // loadGroupItem($(this).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, "")));
    });

    /**
     * Navigator 영역 버튼 클릭시 하위 추적 또는 옵션 로드
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.NAVIGATOR_BUTTON_CLASS), function() {
        // 버튼 클래스별 동작 구분
        switch ($(this).data(vpConst.NAVIGATOR_BUTTON_LEVEL.replace(vpConst.TAG_DATA_PREFIX, ""))) {
            case vpConst.NAVIGATOR_BUTTON_LEVEL_PREV_GROUP:    // 상위 버튼
                loadParentGroupItem($(this).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, "")));
                break;

            case vpConst.NAVIGATOR_BUTTON_LEVEL_GROUP:     // 그룹 버튼
                loadGroupItem($(this).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, "")));
                break;
                
            case vpConst.NAVIGATOR_BUTTON_LEVEL_FUNCTION:    // 함수 버튼
                loadOption($(this).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, "")));
                break;
        }
    });

    /**
     * blueprint 삭제 버튼 클릭시 blueprint 삭제 및 option tab 제거
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.OPTION_BLUEPRINT_ITEM_CLOSE), function() {
        unloadOptionPage($(this).parent().index());
    });
    
    /**
     * blueprint 함수 클릭시 해당 함수 탭 오픈
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.OPTION_BLUEPRINT_ITEM, "span:first-child"), function() {
        tabPageShow($(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER, vpConst.OPTION_PAGE + "." + dynamicFuncJS[$(this).parent().index()].uuid)).index());
    });

    /**
     * 임시 초기화 버튼 클릭시 로드된 옵션 전부 클리어
     */
    $(document).on("click", vpCommon.wrapSelector("#vp_tmpBtnClearLoad"), function() {
        clearLoadedOptions();
    });

    /**
     * 임시 실행 버튼 클릭시 로드된 옵션 실행
     */
    $(document).on("click", vpCommon.wrapSelector("#vp_tmpBtnExcute"), function() {
        excuteGeneratedCode();
    });

    /**
     * 수직 최소화 버튼 클릭시 영역 표시 변환
     */
    $(document).on("click", vpCommon.wrapSelector(".vp-panel-area-vertical-btn"), function() {
        toggleVerticalMinimizeArea($(this));
    });

    /**
     * 수평 최소화 버튼 클릭시 영역 표시 변환
     */
    $(document).on("click", vpCommon.wrapSelector(".vp-panel-area-horizontal-btn"), function() {
        toggleHorizontalMinimizeArea($(this));
    });

    /**
     * 옵션 탭 버튼 클릭시 해당 페이지 이동.
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.OPTION_TAB_CONTAINER, vpConst.OPTION_TAB_ITEM + ".off"), function() {
        tabPageShow($(this).index());
    });

    /**
     * 정렬 가능한 컬럼 헤더 클릭시 해당 컬럼으로 정렬
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.SORTABLE_COLUMN_CLASS), function() {
        sortGrid($(this));
    });

    /**
     * 타스크 추가 버튼 클릭 이벤트
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.NEW_TASK_BUTTON), function() {
        showNaviTap();
    });

    $(document).on("click", vpCommon.wrapSelector(vpConst.TASK_COMMAND_EXECUTE_BUTTON), function() {
        executeTask(getTaskIndex($(this)));
    });

    $(document).on("click", vpCommon.wrapSelector(vpConst.TASK_COMMAND_STOP_BUTTON), function() {
        mylog("Stop");
        $(vpCommon.wrapSelector(vpConst.TASK_COMMAND_STOP_BUTTON)).attr('disabled', true);
    });

    /**
     * 옵션 이전 페이지 이동 버튼 클릭 이벤트
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.OPTION_PREV_PAGE_BUTTON), function() {
        // 첫 페이지가 아닌경우
        if (_CUR_PAGE_INDEX > 0)
            tabPageShow(_CUR_PAGE_INDEX - 1);
    });

    /**
     * 옵션 이전 페이지 이동 버튼 클릭 이벤트
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.OPTION_NEXT_PAGE_BUTTON), function() {
        // 마지막 페이지가 아닌경우
        if ($(vpCommon.wrapSelector(vpConst.OPTION_TAB_CONTAINER, vpConst.OPTION_TAB_ITEM)).length > _CUR_PAGE_INDEX + 1)
            tabPageShow(_CUR_PAGE_INDEX + 1);
    });
    
    /**
     * 옵션 설정 저장 버튼 클릭 이벤트
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.OPTION_SAVE_BUTTON), function() {
        addFuncToTaskList(false);
    });
    
    /**
     * 옵션 설정 저장 하고 실행 버튼 클릭 이벤트
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.OPTION_SAVE_EXECUTE_BUTTON), function() {
        addFuncToTaskList(true);
    });
    
    /**
     * 옵션 설정 취소 버튼 클릭 이벤트
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.OPTION_CANCEL_BUTTON), function() {
        closeOption();
    });

    /* 함수 영역 */
    /**
     * 레이아웃 기본 설정 로드
     * TODO: xml 파일에서 로드하도록 변경, 메타 정보 저장을 위해 vp.js 에서 처리되도록 할지 여부 고려
     */
    var readDefaultConfig = function() {
        vpDivisionStyle = {
            generateArea: {
                width: '60%'
            }
            , taskArea: {
                height: 500
                , 'min-height': 140
            }
            , optionArea: {
                'min-height': 350
            }
            , optionBook: {
                'min-height': 500
            }
            , blueprintArea: {
                height: 150
            }
            , previewArea: {
                height: 50
            }
            , libraryArea: {
                width: 50
                , 'max-width': 450
            }
            , searchArea: {
                'max-height': 500
            }
            , navigatorArea: {
            }
            , variableArea: {
            }
        };
    }

    /**
     * load libraries data
     */
    var loadLibraries = function() {
        var libraryURL = window.location.origin + vpConst.PATH_SEPARATOR + vpConst.BASE_PATH + vpConst.DATA_PATH + vpConst.VP_LIBRARIES_XML_URL;
        xmlLibraries = new xmlHandler.VpXMLHandler(libraryURL);
        xmlLibraries.loadFile(libraryLoadCallback);
    }

    /**
     * library load complete callback
     */
    var libraryLoadCallback = function() {
        bindNavigatorButtons(xmlLibraries.getXML());
        bindSearchAutoComplete();
    }

    /**
     * add auto complete item
     * @param {String} item library search auto complete item
     */
    var addAutoCompleteItem = function(item) {
        // 이미 등록된 항목은 제외한다.
        if (!librarySearchComplete.includes(item)) {
            librarySearchComplete.push(item);
        }
    }

    var bindSearchAutoComplete = function() {
        $(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_TYPE_ATTR + "=" + vpConst.LIBRARY_ITEM_TYPE_FUNCTION + "]").each(function() {
            addAutoCompleteItem($(this).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
            $(this).attr(vpConst.LIBRARY_ITEM_TAG_ATTR).split(",").forEach(function(tag) {
                addAutoCompleteItem(tag.trim());
            });
        });

        $(vpCommon.wrapSelector("#vp_inpSearchLibrary")).autocomplete({
            source: librarySearchComplete
            , focus: function(event, ui) {
                event.preventDefault();
            }
        });
    }

    /**
     * Navigator area initialize
     * @param {xmlNode} node mother node for binding
     */
    var bindNavigatorButtons = function(node) {
        var level = $(node).attr("level");
        if (level === undefined) {
            level = -1;
        }

        var container = $(vpCommon.wrapSelector(vpConst.NAVIGATOR_BUTTON_CONTAINER));
        $(container).empty();
        // 최상위 레벨이 아닌경우 이전 버튼 추가
        if (++level > 0) {
            // $(container).append(makeNavigatorPrevGroupButton($(node)));
        }

        $(node).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_DEPTH_ATTR + "='" + level + "']").each(function() {
            // 그룹, 함수 버튼 추가
            switch ($(this).attr(vpConst.LIBRARY_ITEM_TYPE_ATTR)) {
                case vpConst.LIBRARY_ITEM_TYPE_PACKAGE:
                    $(container).append(makeNavigatorGroupButton($(this)));
                    break;
                    
                case vpConst.LIBRARY_ITEM_TYPE_FUNCTION:
                    $(container).append(makeNavigatorFunctionButton($(this)));
                    break;

                default:
                    console.log("[vp] Error occurred during create navigator button.");
                    console.warn("Wrong type > " + $(this).attr(vpConst.LIBRARY_ITEM_TYPE_ATTR));
                    break;
            }
        });
        // 로드된 네비 버튼에 드래그 기능 바인딩
        $(vpCommon.wrapSelector(vpConst.NAVIGATOR_BUTTON_CLASS
            + "[" + vpConst.NAVIGATOR_BUTTON_LEVEL + "=" + vpConst.NAVIGATOR_BUTTON_LEVEL_FUNCTION + "]")).draggable({
            
            containment: $(vpCommon.getVPContainer())
            , opacity:"0.6"
            , helper: 'clone'
            , cancel: false
            , scroll: false
        });
    }

    /**
     * create navigator group button
     * @param {xmlNode} node library item for create button
     * @returns html tag string
     */
    var makeNavigatorGroupButton = function(node) {
        var sbGrpBtn = new sb.StringBuilder();
        sbGrpBtn.appendFormatLine("<button class='{0} gray' type='button' {1}='{2}' {3}='{4}' title='{5}'>"
            , vpConst.NAVIGATOR_BUTTON_CLASS.replace(".", ""), vpConst.NAVIGATOR_BUTTON_LEVEL
            , vpConst.NAVIGATOR_BUTTON_LEVEL_GROUP, vpConst.LIBRARY_ITEM_DATA_ID
            , $(node).attr(vpConst.LIBRARY_ITEM_ID_ATTR), $(node).find(vpConst.LIBRARY_ITEM_PATH_NODE + ":eq(0)").text());
        sbGrpBtn.appendFormatLine("<span class='{0}' {1}='{2}'>{3}</span>"
            , vpConst.MULTI_LANGUAGE_CLASS.replace(".", ""), vpConst.LANGUAGE_CAPTION_ID
            , $(node).attr(vpConst.LIBRARY_ITEM_ID_ATTR), $(node).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
        sbGrpBtn.append("</button>");
        return sbGrpBtn.toString();
    }

    /**
     * create navigator group button
     * @param {xmlNode} node library item for create button
     * @returns html tag string
     */
    var makeNavigatorFunctionButton = function(node) {
        var sbFncBtn = new sb.StringBuilder();
        sbFncBtn.appendFormatLine("<button class='{0} black' type='button' {1}='{2}' {3}='{4}' title='{5}'>"
            , vpConst.NAVIGATOR_BUTTON_CLASS.replace(".", ""), vpConst.NAVIGATOR_BUTTON_LEVEL
            , vpConst.NAVIGATOR_BUTTON_LEVEL_FUNCTION, vpConst.LIBRARY_ITEM_DATA_ID
            , $(node).attr(vpConst.LIBRARY_ITEM_ID_ATTR), $(node).find(vpConst.LIBRARY_ITEM_PATH_NODE + ":eq(0)").text());
        sbFncBtn.appendFormatLine("<span class='{0}' {1}='{2}'>{3}</span>"
            , vpConst.MULTI_LANGUAGE_CLASS.replace(".", ""), vpConst.LANGUAGE_CAPTION_ID
            , $(node).attr(vpConst.LIBRARY_ITEM_ID_ATTR), $(node).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
        sbFncBtn.append("</button>");
        return sbFncBtn.toString();
    }

    /**
     * create navigator prev group button
     * @param {xmlNode} node library item for create button
     * @returns html tag string
     */
    var makeNavigatorPrevGroupButton = function(node) {
        var sbPrevBtn = new sb.StringBuilder();
        var titleCaption = $(node).find(vpConst.LIBRARY_ITEM_PATH_NODE + ":eq(0)").text();
        titleCaption = titleCaption.substring(0, titleCaption.lastIndexOf("-") - 1);
        sbPrevBtn.appendFormatLine("<button class='{0} black' type='button' {1}='{2}' {3}='{4}' title='{5}'>"
            , vpConst.NAVIGATOR_BUTTON_CLASS.replace(".", ""), vpConst.NAVIGATOR_BUTTON_LEVEL
            , vpConst.NAVIGATOR_BUTTON_LEVEL_PREV_GROUP, vpConst.LIBRARY_ITEM_DATA_ID
            , $(node).attr(vpConst.LIBRARY_ITEM_ID_ATTR), titleCaption);
        sbPrevBtn.appendFormatLine("<span class='{0}' {1}='{2}'>{3}</span>"
            , vpConst.MULTI_LANGUAGE_CLASS.replace(".", ""), vpConst.LANGUAGE_CAPTION_ID
            , $(node).attr(vpConst.LIBRARY_ITEM_ID_ATTR), "Prev");
        sbPrevBtn.append("</button>");
        return sbPrevBtn.toString();
    }

    /**
     * 메인 UI init
     */
    var containerInit = function() {
        loadLibraries();
        readDefaultConfig();
        calculateDivisionWidth();
        
        // 제네레이트 영역에 드랍 기능 바인딩
        $(vpCommon.wrapSelector(vpConst.AREA_GENERATE_OPTION)).droppable({
            drop: function(event, ui) {
                // 함수인 경우에만 로드.
                if (ui.draggable.data(vpConst.NAVIGATOR_BUTTON_LEVEL.replace(vpConst.TAG_DATA_PREFIX, "")) === vpConst.NAVIGATOR_BUTTON_LEVEL_FUNCTION) {
                    loadOption(ui.draggable.data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, "")));
                }
            }
        });
    }
    
    /**
     * 분할영역 넓이 계산
     */
    var calculateDivisionWidth = function() {
        // 분할영역 height 설정
        adjustAreaStyle(vpDivisionStyle.libraryArea);
        vpDivisionStyle.generateArea.height = $(vpCommon.getVPContainer()).height() - $(vpCommon.wrapSelector(vpConst.AREA_GENERATE)).position().top;
        // option area 활성화인 경우는 영역 변경분을 option Area 에 할당하며, 비활성화 인경우 task area에 할당한다.
        // if ($(vpCommon.wrapSelector(vpConst.AREA_GENERATE_OPTION)).is(":visible")) {
        //     vpDivisionStyle.optionArea.height = vpDivisionStyle.generateArea.height - vpDivisionStyle.taskArea.height - 53;
        //     // option area min-height 보다 작아지는 경우는 taskArea로 할당한다.
        //     if (vpDivisionStyle.optionArea.height < vpDivisionStyle.optionArea['min-height']) {
        //         vpDivisionStyle.taskArea.height = vpDivisionStyle.taskArea.height - vpDivisionStyle.optionArea.height + vpDivisionStyle.optionArea['min-height'];
        //     }
        // } else {
        //     vpDivisionStyle.taskArea.height = vpDivisionStyle.generateArea.height - $(vpCommon.wrapSelector(vpConst.AREA_TASK_MANAGEMENT)).position().top + $(vpCommon.wrapSelector(vpConst.AREA_GENERATE)).position().top - 25;
        // } /* 2020.08.31 타스크 영역 미표시 */
        vpDivisionStyle.optionBook['min-height'] = vpDivisionStyle.generateArea.height - 145;
        vpDivisionStyle.libraryArea.height = $(vpCommon.getVPContainer()).height() - $(vpCommon.wrapSelector(vpConst.AREA_GENERATE)).position().top;
        vpDivisionStyle.generateArea.width = $(vpCommon.wrapSelector(vpConst.AREA_DIVISION_CONTAINER)).innerWidth() - $(vpCommon.wrapSelector(vpConst.AREA_LIBRARY)).outerWidth();

        // 설정 적용
        adjustAreaStyle();
    }

    /**
     * 파라미터 없으면 vpDivisionStyle 하위 전체 설정 적용.
     * 파라미터 존재시 vpDivisionStyle 에 있고 id 맵핑 되는 경우 적용.
     * @param {vpDivisionStyle} style 영역 설정 스타일
     */
    var adjustAreaStyle = function(style = vpDivisionStyle) {
        try {
            // 전체 파라미터인 경우
            if (style === vpDivisionStyle) {
                Object.keys(style).forEach(function (key) {
                    $(vpCommon.getVPContainer()).find(vpConst.VP_ID_PREFIX + key).css(style[key]);
                });
            }
            else {
                Object.keys(vpDivisionStyle).forEach(function (key) {
                    // 요청한 스타일만 적용
                    if (style === vpDivisionStyle[key]) {
                        $(vpCommon.getVPContainer()).find(vpConst.VP_ID_PREFIX + key).css(vpDivisionStyle[key]);
                    }
                });
            }
        } catch (err) {
            console.log("[vp] Error occurred during adjust style. Skip this time.");
            console.warn(err.message);
        }
    }
    
    /**
     * 네비 상위그룹 로드
     * @param {String} prevGrpID xml 상위 그룹 id
     */
    var loadParentGroupItem = function(prevGrpID) {
        bindNavigatorButtons($(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_ID_ATTR + "=" + prevGrpID + "]").parent());
        removeNaviPathItem();
    }

    /**
     * 네비 하위그룹 로드
     * @param {String} grpID xml 그룹 id
     */
    var loadGroupItem = function(grpID) {
        var grpNode = $(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_ID_ATTR + "=" + grpID + "]");
        bindNavigatorButtons(grpNode);
        addNaviPathItem(grpNode);
    }

    var naviPathHandling = function(grpID) {
        // root 클릭인 경우
        if (grpID === undefined) {
            // 현재 표시중인 그룹이 아닌 경우
            if ($(vpCommon.wrapSelector(vpConst.NAVIGATOR_PATH_ITEM_CONTAINER)).children(vpConst.NAVIGATOR_PATH_ITEM_CLASS).length > 1) {
                $(vpCommon.wrapSelector(vpConst.NAVIGATOR_PATH_ITEM_CONTAINER)).children("span:gt(0)").remove();
                bindNavigatorButtons(xmlLibraries.getXML());
            }
        } else {
            // 현재 표시중인 그룹이 아닌 경우
            if ($(vpCommon.wrapSelector(vpConst.NAVIGATOR_BUTTON_CONTAINER)).find(
                "button[" + vpConst.NAVIGATOR_BUTTON_LEVEL + "=" + vpConst.NAVIGATOR_BUTTON_LEVEL_PREV_GROUP + "]")
                .data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, "")) != grpID) {
                    var point = $(vpCommon.wrapSelector(vpConst.NAVIGATOR_PATH_ITEM_CONTAINER))
                        .find("span[" + vpConst.LIBRARY_ITEM_DATA_ID + "=" + grpID + "]").index();
                    $(vpCommon.wrapSelector(vpConst.NAVIGATOR_PATH_ITEM_CONTAINER)).children("span:gt(" + point + ")").remove();
                    var grpNode = $(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_ID_ATTR + "=" + grpID + "]");
                    bindNavigatorButtons(grpNode);
                }
        }
    }

    /**
     * 네비 패스 아이템 추가
     * @param {xmlNode} node mother node for binding
     */
    var addNaviPathItem = function(node) {
        var sbPathItem = new sb.StringBuilder();
        sbPathItem.appendFormatLine("<span class='{0}'></span>", vpConst.NAVIGATOR_PATH_ITEM_DIVIDER.replace(".", ""));
        sbPathItem.appendFormat("<span class='{0}' {1}='{2}'>{3}</span>"
            , vpConst.NAVIGATOR_PATH_ITEM_CLASS.replace(".", ""), vpConst.LIBRARY_ITEM_DATA_ID
            , $(node).attr(vpConst.LIBRARY_ITEM_ID_ATTR), $(node).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
        $(vpCommon.wrapSelector(vpConst.NAVIGATOR_PATH_ITEM_CONTAINER)).append(sbPathItem.toString());
    }

    /**
     * 네비 패스 마지막 아이템 제거
     */
    var removeNaviPathItem = function() {
        $(vpCommon.wrapSelector(vpConst.NAVIGATOR_PATH_ITEM_CONTAINER)).children(vpConst.NAVIGATOR_PATH_ITEM_CLASS + ":last-child").remove();
        $(vpCommon.wrapSelector(vpConst.NAVIGATOR_PATH_ITEM_CONTAINER)).children(vpConst.NAVIGATOR_PATH_ITEM_DIVIDER + ":last-child").remove();
    }

    /**
     * 옵션 페이지 로드
     * @param {String} funcID xml 함수 id
     * @param {funcJS} taskJS saved task
     */
    var loadOption = function(funcID, taskJS) {
        // 옵션 영역이 표시 중 이면 함수 로딩 컨펌하고 미 표시 중 이면 표시한다.
        if ($(vpCommon.wrapSelector(".vp-option-command-btn-container")).is(":visible")) {
            if (!confirm("When you load a new function, all unsaved options are discarded. Would you like to continue?")) {
                return;
            }
        } else {
            // vpDivisionStyle.optionArea.height = vpDivisionStyle.taskArea.height - vpDivisionStyle.taskArea['min-height'];
            // // min-height 보다 작은 경우 min-height로 맞춰준다.
            // if (vpDivisionStyle.optionArea.height < vpDivisionStyle.optionArea['min-height']) {
            //     vpDivisionStyle.optionArea.height = vpDivisionStyle.optionArea['min-height'];
            // }
            // vpDivisionStyle.optionBook['min-height'] = vpDivisionStyle.optionArea.height - 182;
            // vpDivisionStyle.taskArea.height = vpDivisionStyle.taskArea['min-height'];

            // 설정 적용
            adjustAreaStyle();

            // $(vpCommon.wrapSelector(vpConst.AREA_GENERATE_OPTION)).show();
            $("#vp_btnNewTask").hide();
            $(vpCommon.wrapSelector(".vp-option-command-btn-container")).show();
            $(vpCommon.wrapSelector(".vp-option-header")).show();
        }

        // 신규 로드인 경우.
        if (taskJS === undefined) {
            var loadUrl = getOptionPageURL(funcID);
            // 옵션 페이지 url 로딩이 정상처리 된 경우 js 파일 로드
            if (loadUrl !== "") {
                // 옵션 로드
                requirejs([loadUrl], function (loaded) {
                    loaded.initOption(optionPageLoadCallback);
                });
            }
        } else {
            // TODO: 로드 호출.
        }
    }

    /**
     * 옵션 페이지 URL 조회
     * @param {*} funcID xml 함수 id
     * @param {object} taskObj saved task TODO: 현재 미정.
     */
    var getOptionPageURL = function(funcID, taskObj) {
        var sbURL = new sb.StringBuilder();
        sbURL.clear();
        sbURL.append(Jupyter.notebook.base_url);
        sbURL.append(vpConst.BASE_PATH);
        sbURL.append(vpConst.SOURCE_PATH);
        // 함수 경로 바인딩
        var optionData = $(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_ID_ATTR + "=" + funcID + "]");
        var filePath = $(optionData).find(vpConst.LIBRARY_ITEM_FILE_URL_NODE).text();
            
        // 경로가 조회되지 않는 경우
        if (filePath === undefined || filePath === "") {
            alert("Function id not founded!");
            return "";
        }
        
        //FIXME: taskobj 반영
        var taskLabelCaption = taskObj === undefined ? "NEW TASK OPTION" : ("T" + taskObj + " OPTION");

        $(vpCommon.wrapSelector(vpConst.OPTION_TASK_INDEX_LABEL))
            .data(vpConst.OPTION_HEADER_TEMP_CAPTION.replace(vpConst.TAG_DATA_PREFIX, ""), taskLabelCaption);
        $(vpCommon.wrapSelector(vpConst.OPTION_KIND_LABEL))
            .data(vpConst.OPTION_HEADER_TEMP_CAPTION.replace(vpConst.TAG_DATA_PREFIX, ""), $(optionData).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));

        sbURL.append(filePath);
        return sbURL.toString();
    }
    
    /**
     * 옵션 페이지 로드 완료 callback.
     * @param {funcJS} funcJS 옵션 js 객체
     * @param {number} taskIndex task index
     */
    var optionPageLoadCallback = function(funcJS, taskIndex) {
        $(vpCommon.wrapSelector(vpConst.OPTION_TAB_CONTAINER)).empty();
        $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).empty();
        $(vpCommon.wrapSelector(vpConst.AREA_BLUEPRINT, vpConst.OPTION_BLUEPRINT_CONTAINER)).empty();
        _CUR_PAGE_INDEX = -1;
        
        tempFuncJS = funcJS;
        // dynamicFuncJS[dynamicFuncJS.length] = funcJS;
        addOptionTabButton(funcJS);
        addBlueprint(funcJS);
        makeUpGreenRoomHTML();
    }
    
    /**
     * 옵션 페이지 html 처리 및 헤더 바인딩
     */
    var makeUpGreenRoomHTML = function() {
        $(vpCommon.wrapSelector(vpConst.OPTION_TASK_INDEX_LABEL)).html(
            $(vpCommon.wrapSelector(vpConst.OPTION_TASK_INDEX_LABEL)).data(vpConst.OPTION_HEADER_TEMP_CAPTION.replace(vpConst.TAG_DATA_PREFIX, ""))
        );
        $(vpCommon.wrapSelector(vpConst.OPTION_KIND_LABEL)).html(
            $(vpCommon.wrapSelector(vpConst.OPTION_KIND_LABEL)).data(vpConst.OPTION_HEADER_TEMP_CAPTION.replace(vpConst.TAG_DATA_PREFIX, ""))
        );
        $(vpCommon.wrapSelector(vpConst.OPTION_TASK_INDEX_LABEL))
            .data(vpConst.OPTION_HEADER_TEMP_CAPTION.replace(vpConst.TAG_DATA_PREFIX, ""), "");
        $(vpCommon.wrapSelector(vpConst.OPTION_KIND_LABEL))
            .data(vpConst.OPTION_HEADER_TEMP_CAPTION.replace(vpConst.TAG_DATA_PREFIX, ""), "");

        $(vpCommon.wrapSelector(vpConst.OPTION_GREEN_ROOM, vpConst.OPTION_PAGE)).each(function() {
            $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).append($(this).hide());
        });

        // 표시중인 옵션 페이지가 없는 경우 첫 항목 표시
        if (_CUR_PAGE_INDEX < 0) {
            tabPageShow(0);
        }
    }
    
    /**
     * 옵션 탭 헤더 추가
     * @param {funcJS} funcJS 옵션 js 객체
     */
    var addOptionTabButton = function(funcJS) {
        var sbTag = new sb.StringBuilder();
        for (var idx = 0; idx < funcJS.stepCount; idx++) {
            sbTag.appendFormatLine("<div class='{0} {1} {2}'></div>", vpConst.OPTION_TAB_ITEM.replace(".", ""), funcJS.uuid, "off");
        }
        $(vpCommon.wrapSelector(vpConst.OPTION_TAB_CONTAINER)).append(sbTag.toString());
        
        // step이 1개인 경우 페이지 이동 버튼은 표시하지 않는다.
        if (funcJS.stepCount == 1) {
            $(vpCommon.wrapSelector(vpConst.OPTION_TAB_ITEM)).hide();
            $(vpCommon.wrapSelector(vpConst.OPTION_PAGING_BUTTON)).hide();
        } else {
            $(vpCommon.wrapSelector(vpConst.OPTION_TAB_ITEM)).show();
            $(vpCommon.wrapSelector(vpConst.OPTION_PAGING_BUTTON)).show();
        }
    }


    /**
     * 표시 탭 변경
     * @param {number} tabIdx 표시할 탭 인덱스
     */
    var tabPageShow = function(tabIdx) {
        // tabIdx 가 숫자가 아닌경우
        if (typeof(tabIdx) !== 'number') {
            console.log("[vp] Error occurred during option tab index change.");
            console.warn("The requested parameter [" + tabIdx + "] is not number");
            return;
        }

        var totalTabPageCount = $(vpCommon.wrapSelector(vpConst.OPTION_TAB_CONTAINER, vpConst.OPTION_TAB_ITEM)).length;
        // tabIdx 가 탭 수 보다 큰 경우
        if (totalTabPageCount <= tabIdx) {
            console.log("[vp] Error occurred during option tab index change.");
            console.warn("The tab index requested is greater than the total number of tabs.");
            return;
        }

        // 현재 보여지는 페이지가 아니면 페이지 변경
        if (_CUR_PAGE_INDEX !== tabIdx) {
            // On 상태를 Off 로 변경
            $(vpCommon.wrapSelector(vpConst.OPTION_TAB_CONTAINER, vpConst.OPTION_TAB_ITEM + ".on")).toggleClass("on").toggleClass("off");
            // 요청버튼 Off 상태에서 On 으로 변경
            $(vpCommon.wrapSelector(vpConst.OPTION_TAB_CONTAINER, vpConst.OPTION_TAB_ITEM + ":eq(" + tabIdx + ")")).toggleClass("on").toggleClass("off");
    
            // 전체 탭 미표시 처리
            $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER, vpConst.OPTION_PAGE)).hide();
            // 요청 탭 표시
            $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER, vpConst.OPTION_PAGE + ":eq(" + tabIdx + ")")).show();
            _CUR_PAGE_INDEX = tabIdx;

            var curUUID = $(vpCommon.wrapSelector(vpConst.OPTION_TAB_CONTAINER, vpConst.OPTION_TAB_ITEM + ":eq(" + tabIdx + ").on")).attr("class")
                .replace(vpConst.OPTION_TAB_ITEM.replace(".", ""), "").replace("on", "").replace("off", "").trim();

            // 전체 블루프린트 아이템 포커스 제거
            $(vpCommon.wrapSelector(vpConst.AREA_BLUEPRINT, vpConst.OPTION_BLUEPRINT_CONTAINER, vpConst.OPTION_BLUEPRINT_ITEM)).removeClass(vpConst.OPTION_BLUEPRINT_FOCUSED_ITEM);
            // 표시 블루프린트 아이템 포커스 설정
            $(vpCommon.wrapSelector(vpConst.AREA_BLUEPRINT, vpConst.OPTION_BLUEPRINT_CONTAINER, "." + curUUID)).addClass(vpConst.OPTION_BLUEPRINT_FOCUSED_ITEM);
        }
    }

    /**
     * blueprint 영역에 오브젝트 추가
     * @param {funcJS} funcJS 옵션 js 객체
     */
    var addBlueprint = function(funcJS) {
        $(vpCommon.wrapSelector(vpConst.AREA_BLUEPRINT, vpConst.OPTION_BLUEPRINT_CONTAINER)).append(makeBlueprintItem(funcJS));
    }

    /**
     * blueprint 오브젝트 생성
     * @param {funcJS} funcJS 옵션 js 객체
     * @returns {Object} blueprint object
     */
    var makeBlueprintItem = function(funcJS) {
        var sbBPItem = new sb.StringBuilder();
        sbBPItem.appendFormat("<div class='{0} {1}'><span>{2}</span>",
            vpConst.OPTION_BLUEPRINT_ITEM.replace(".", ""), funcJS.uuid, funcJS.funcName);
        sbBPItem.appendFormat("<span class='{0}'>x</span></div>", vpConst.OPTION_BLUEPRINT_ITEM_CLOSE.replace(".", ""));
        return sbBPItem.toString();
    }

    /**
     * 함수 제거
     * @param {number} funcIndex 삭제 옵션 인덱스
     */
    var unloadOptionPage = function(funcIndex) {
        // 제거되는 함수가 표현중인 경우
        if ($(vpCommon.wrapSelector(vpConst.OPTION_TAB_CONTAINER, "." + dynamicFuncJS[funcIndex].uuid + vpConst.OPTION_TAB_ITEM + ".on")).index() > -1) {
            tabPageShow($(vpCommon.wrapSelector(vpConst.OPTION_TAB_CONTAINER, vpConst.OPTION_TAB_ITEM)).not("." + dynamicFuncJS[funcIndex].uuid).first().index());
        }
        // 텝 헤더 제거
        $(vpCommon.wrapSelector(vpConst.OPTION_TAB_CONTAINER, "." + dynamicFuncJS[funcIndex].uuid + vpConst.OPTION_TAB_ITEM)).remove();
        // 텝 페이지 제거
        $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER, "." + dynamicFuncJS[funcIndex].uuid + vpConst.OPTION_PAGE)).remove();
        // 블루프린트 제거
        $(vpCommon.wrapSelector(vpConst.AREA_BLUEPRINT, vpConst.OPTION_BLUEPRINT_CONTAINER, vpConst.OPTION_BLUEPRINT_ITEM + ":eq(" + funcIndex + ")")).remove();
        // load js 제거
        dynamicFuncJS.splice(funcIndex, 1);
    }

    /**
     * 로드된 옵션 전체 제거
     */
    var clearLoadedOptions = function() {
        dynamicFuncJS.splice(0);
        $(vpCommon.wrapSelector(vpConst.OPTION_TAB_CONTAINER)).empty();
        $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).empty();
        $(vpCommon.wrapSelector(vpConst.OPTION_GREEN_ROOM)).empty();
        $(vpCommon.wrapSelector(vpConst.AREA_BLUEPRINT, vpConst.OPTION_BLUEPRINT_CONTAINER)).empty();
        _CUR_PAGE_INDEX = -1;
    }

    /**
     * 타스크 추가. 파라미터 true 인 경우 바로 셀 실행
     * @param {boolean} run 실행여부
     */
    var addFuncToTaskList = function(run) {
        // TODO: valitate
        if (!tempFuncJS.optionValidation()) {
            return false;
        }
        // TODO: 타스크 추가
        var generatedCode = tempFuncJS.generateCode(run);
        if (generatedCode === "BREAK_RUN") {
            // alert("Error occurred during add task. Request breaked.");
            console.log("[vp] Error occurred during add task. Request breaked.");
            // console.warn("generated code is undefined");
            return false;
        }
        // dynamicFuncJS[dynamicFuncJS.length] = tempFuncJS;
        
        // // 바로 실행인경이 실행한다.
        // if (run) 
        //     tempFuncJS.generateCode(true);

        // $(vpCommon.wrapSelector(vpConst.TASK_ADD_CMD)).before(makeTaskHTML(generatedCode));
        closeOption();
    }

    /**
     * task list item generate
     * @param {string} code generated code
     * @returns task list item html
     */
    var makeTaskHTML = function(code) {
        code = code.replace(/\'/g, "&apos;");

        var sbTaskItem = new sb.StringBuilder();
        sbTaskItem.appendFormatLine("<tr class='{0}'>", vpConst.TASK_LIST_ROW.replace(".", ""));
        
        sbTaskItem.appendFormat("<td class='{0}'>", vpConst.TASK_INDEX_CELL.replace(".", ""));
        sbTaskItem.appendFormat("<button class='{0}' type='button'><span>{1}{2}</span></button>"
            , vpConst.TASK_BUTTON.replace(".", ""), vpConst.TASK_INDEX_PREFIX, ++taskIndex);
        sbTaskItem.appendLine("</td>");
        
        sbTaskItem.append("<td>");
        sbTaskItem.appendFormat("<span class='{0}' title='{1}'>{2}</span>", vpConst.TASK_LABEL_CONTROL.replace(".", ""), code, code);
        sbTaskItem.appendLine("</td>");
        
        sbTaskItem.appendFormat("<td class='{0}'>", vpConst.TASK_COMMAND_CELL.replace(".", ""));
        sbTaskItem.appendFormat("<button class='{0} {1} {2} green' {4} type='button'><span>{3}</span></button>"
            , vpConst.TASK_BUTTON.replace(".", ""), vpConst.TASK_COMMAND_BUTTON.replace(".", "")
            , vpConst.TASK_COMMAND_EXECUTE_BUTTON.replace(".", ""), "Run"
            , Jupyter.notebook.kernel_busy ? "disabled='disabled'" : "");
        sbTaskItem.appendFormat("<button class='{0} {1} {2} red' disabled='disabled' type='button'><span>{3}</span></button>"
            , vpConst.TASK_BUTTON.replace(".", ""), vpConst.TASK_COMMAND_BUTTON.replace(".", "")
            , vpConst.TASK_COMMAND_STOP_BUTTON.replace(".", ""), "Stop");
        sbTaskItem.appendLine("</td>");
        
        sbTaskItem.appendLine("</tr>");
        
        return sbTaskItem.toString();
    }

    /**
     * 옵션 설정 페이지 취소
     */
    var closeOption = function() {
        tempFuncJS = null;
        // $(vpCommon.wrapSelector(vpConst.AREA_GENERATE_OPTION)).hide();
        $(vpCommon.wrapSelector(".vp-option-command-btn-container")).hide();
        $(vpCommon.wrapSelector(".vp-option-header")).hide();
        $(vpCommon.wrapSelector(vpConst.OPTION_TAB_CONTAINER)).empty();
        $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).empty();
        $(vpCommon.wrapSelector(vpConst.OPTION_GREEN_ROOM)).empty();
        $(vpCommon.wrapSelector(vpConst.AREA_BLUEPRINT, vpConst.OPTION_BLUEPRINT_CONTAINER)).empty();
        _CUR_PAGE_INDEX = -1;
        $("#vp_btnNewTask").show();
        calculateDivisionWidth();
    }

    /**
     * search library and bind grid
     */
    var searchLibrary = function() {
        var container = $(vpCommon.wrapSelector(vpConst.SEARCH_RESULT_CONTAINER));
        var gridHeader = $(container).find(vpConst.LIST_GRID_HEADER);

        $(container).empty();
        $(container).append(gridHeader);

        var searchText = $(vpCommon.wrapSelector("#vp_inpSearchLibrary")).val().toUpperCase();
        // 검색어 입력이 없는 경우 전체 조회한다.
        if (searchText === "") {
            $(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_TYPE_ATTR + "=" + vpConst.LIBRARY_ITEM_TYPE_FUNCTION + "]").each(function() {
                $(container).append(makeSearchResultItem($(this)));
            });
        } else {
            $(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_NAME_ATTR + "*='" + searchText + "']"
                + "," + vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_TAG_ATTR + "*='" + searchText + "']")
                .each(function() {

                $(container).append(makeSearchResultItem($(this)));
            });
        }
        // 로드된 검색결과에 드래그 기능 바인딩
        $(container).find(vpConst.SEARCH_RESULT_ITEM_CLASS
            + "[" + vpConst.NAVIGATOR_BUTTON_LEVEL + "=" + vpConst.NAVIGATOR_BUTTON_LEVEL_FUNCTION + "]").draggable({
            
            containment: $(vpCommon.getVPContainer())
            , opacity:"0.6"
            , helper: 'clone'
            , cancel: false
            , scroll: false
        });
    }

    /**
     * create search result grid row
     * @param {xmlNode} node library item for row
     * @returns html tag string
     */
    var makeSearchResultItem = function(node) {
        var sbSrcGridItem = new sb.StringBuilder();
        sbSrcGridItem.appendLine("<tr>");
        sbSrcGridItem.appendFormatLine("<td><span class='{0} {1}' {2}='{3}' {4}='{5}' title='{6}'>{7}</span></td>"
            , vpConst.SEARCH_RESULT_ITEM_CLASS.replace(".", ""), vpConst.SORT_VALUE_WRAP_CLASS.replace(".", "")
            , vpConst.NAVIGATOR_BUTTON_LEVEL, vpConst.NAVIGATOR_BUTTON_LEVEL_FUNCTION
            , vpConst.LIBRARY_ITEM_DATA_ID, $(node).attr(vpConst.LIBRARY_ITEM_ID_ATTR)
            , $(node).find(vpConst.LIBRARY_ITEM_PATH_NODE + ":eq(0)").text(), $(node).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
        sbSrcGridItem.appendFormatLine("<td><span class='{0}' title='{1}'>{2}</span></td>"
            , vpConst.SORT_VALUE_WRAP_CLASS.replace(".", ""), $(node).find(vpConst.LIBRARY_ITEM_DESCRIPTION_NODE + ":eq(0)").text()
            , $(node).attr(vpConst.LIBRARY_ITEM_TAG_ATTR));
        sbSrcGridItem.appendLine("</tr>");
        return sbSrcGridItem.toString();
    }

    /**
     * add variable grid row
     * @param {string} varName variable name
     * @param {string} varType variable type
     */
    var addVariableItem = function(varName, varType) {
        var container = $(vpCommon.wrapSelector(vpConst.VARIABLE_LIST_CONTAINER));

        $(container).append(makeVariableItem(varName, varType));
    }

    /**
     * variable grid row
     * @param {string} varName variable name
     * @param {string} varType variable type
     * @returns html tag string
     */
    var makeVariableItem = function(varName, varType) {
        var sbVarGridItem = new sb.StringBuilder();
        sbVarGridItem.appendLine("<tr>");
        sbVarGridItem.appendFormatLine("<td><span class='{0} {1}'>{3}</span></td>"
            ,vpConst.VARIABLE_LIST_ITEM_CLASS.replace(".", "") , vpConst.SORT_VALUE_WRAP_CLASS.replace(".", ""), varName);
        sbVarGridItem.appendFormatLine("<td><span class='{0}'>{1}</span></td>"
            ,vpConst.VARIABLE_LIST_ITEM_CLASS.replace(".", ""), varType);
        sbVarGridItem.appendLine("</tr>");
        return sbVarGridItem.toString();
    }

    /**
     * sort grid
     * @param {HTMLtag} colObj event obj(for sort column head)
     */
    var sortGrid = function(colObj) {
        var sortColIndex = getSortHeaderIndex(colObj);
        // if not found sort index then break
        if(sortColIndex < 0) return false;

        var sortTable = getSortTable(colObj);
        // if not found sort table then break
        if (sortTable === undefined) return false;

        var sortData = $(sortTable).find("tr:not(" + vpConst.LIST_GRID_HEADER + ")");
        // if sort table has no data then break
        if (sortData.length < 1) return false;
        sortList = Array.prototype.sort.bind(sortData);
        
        // ascending 인 경우 descending 정렬, descending 이나 non sort 인 경우 ascending 정렬
        var ascending = $(colObj).parent().find(vpConst.ARROW_UP_CLASS).length > 0 ? false : true;

        sortList(function(itemA, itemB) {
            var valA = $(itemA).find("td:eq(" + sortColIndex + ")").find(vpConst.SORT_VALUE_WRAP_CLASS).html();
            var valB = $(itemB).find("td:eq(" + sortColIndex + ")").find(vpConst.SORT_VALUE_WRAP_CLASS).html();

            if (valA < valB) {
                return ascending ? -1 : 1;
            } else if (valA > valB) {
                return ascending ? 1 : -1;
            } else {
                return 0;
            }
        });

        $(sortTable).find(vpConst.ARROW_UP_CLASS).remove();
        $(sortTable).find(vpConst.ARROW_DOWN_CLASS).remove();
        $(sortTable).find(vpConst.LIST_GRID_HEADER).find("th:eq(" + sortColIndex + ")").append(
            "<span class='" + (ascending ? vpConst.ARROW_UP_CLASS.replace(".", "") : vpConst.ARROW_DOWN_CLASS.replace(".", "")) + "'></span>"
        );
        sortTable.append(sortData);
    }
    
    /**
     * find reqested sort column index.
     * sort column have to in TH tag. If not retrun -1
     * @param {HTMLtag} chkObj 
     * @returns index of requested th column index
     */
    var getSortHeaderIndex = function(chkObj) {
        var parentObj = $(chkObj).parent();
        // if parent is wrapper return -1. means not found
        if ($(parentObj).attr("ID") === vpConst.VP_CONTAINER_ID) {
            return -1;
        }
        // if parent is TH return parent's index
        if ($(parentObj).prop('tagName') === "TH") {
            return $(parentObj).index();
        }
        // find upper depth
        return getSortHeaderIndex(parentObj);
    }

    /**
     * find reqested sort table. If not retrun undefined
     * @param {HTMLtag} chkObj 
     * @returns HTMLtag sort table
     */
    var getSortTable = function(chkObj) {
        var parentObj = $(chkObj).parent();
        // if parent is wrapper return undefined. means not found
        if ($(parentObj).attr("ID") === vpConst.VP_CONTAINER_ID) {
            return undefined;
        }
        // if parent is sortable table return that
        if ($(parentObj).hasClass(vpConst.SORTABLE_TABLE_CLASS.replace(".", ""))) {
            return parentObj;
        }
        // find upper depth
        return getSortTable(parentObj);
    }

    /**
     * 커널 대기중으로 변경시 처리
     */
    var setKernelIdle = function() {
        $(vpCommon.wrapSelector(vpConst.TASK_COMMAND_EXECUTE_BUTTON)).attr('disabled', false);
    }

    /**
     * 커널 실행중으로 변경시 처리
     */
    var setKernelBusy = function() {
        $(vpCommon.wrapSelector(vpConst.TASK_COMMAND_EXECUTE_BUTTON)).attr('disabled', true);
        // TODO: 장기간 커널 사용중인 경우 처리
    }

    /**
     * get request tesk command index
     * @param {htmlTag} tag taskCmdLineTag
     */
    var getTaskIndex = function(tag) {
        if ($(tag).hasClass(vpConst.TASK_LIST_ROW.replace(".", ""))) {
            return $(tag).index();
        } else {
            return  getTaskIndex(tag.parent());
        }
    }

    /**
     * execute task on ne
     * @param {number} exeIndex executeTaskIndex
     */
    var executeTask = function(exeIndex) {
        dynamicFuncJS[exeIndex].executeGenerated();
    }

    /**
     * 영역 수직 최소화, 복원
     * @param {HTMLtag} btnObj 
     */
    var toggleVerticalMinimizeArea = function(btnObj) {
        $(btnObj).parent().parent().toggleClass(vpConst.OPENED_AREA_CLASS).toggleClass(vpConst.CLOSED_AREA_CLASS);
        $(btnObj).toggleClass(vpConst.AREA_BTN_UP).toggleClass(vpConst.AREA_BTN_DOWN);
        // toggleMinimizeArea($(this));
    }

    /**
     * 영역 수평 최소화, 복원
     * @param {HTMLtag} btnObj 
     */
    var toggleHorizontalMinimizeArea = function(btnObj) {
        // 오른쪽 버튼인 경우
        if ($(btnObj).hasClass(vpConst.AREA_BTN_RIGHT)) {
            // 영역 최소화
            $(btnObj).parent().parent().find(vpConst.LIBRARY_SUB_CONTAINER).hide();
            vpDivisionStyle.libraryArea.width = "50px";
            $(btnObj).parent().parent().data("spread-width", $(btnObj).parent().parent().css("width"));
            $(btnObj).parent().parent().find(".header").toggleClass(vpConst.VERTICAL_TEXT_CLASS);
        } else {
            // 영역 복원
            var spreadWidth = $(btnObj).parent().parent().data("spread-width") === undefined ? '40%' : $(btnObj).parent().parent().data("spread-width");
            vpDivisionStyle.libraryArea.width = spreadWidth;
            $(btnObj).parent().parent().find(vpConst.LIBRARY_SUB_CONTAINER).show();
            $(btnObj).parent().parent().find(".header").toggleClass(vpConst.VERTICAL_TEXT_CLASS);
        }
        $(btnObj).parent().parent().toggleClass(vpConst.OPENED_AREA_CLASS).toggleClass(vpConst.CLOSED_AREA_CLASS);
        $(btnObj).toggleClass(vpConst.AREA_BTN_RIGHT).toggleClass(vpConst.AREA_BTN_LEFT);

        calculateDivisionWidth();
    }

    // TODO: 네비게이션 탭 표시
    var showNaviTap = function() {
        // console.warn("Need dev. Now library area is none tab design");
        if ($(vpCommon.wrapSelector(vpConst.AREA_LIBRARY)).hasClass(vpConst.CLOSED_AREA_CLASS)) {
            toggleHorizontalMinimizeArea($(vpCommon.wrapSelector(vpConst.AREA_LIBRARY
                , ".vp-panel-area-horizontal-btn.vp-arrow-left")));
        }
    }

    /**
     * 코드 실행
     * @param {boolean} excute excute code, default : true
     */
    var excuteGeneratedCode = function(excute = true) {
        // 로드된 함수가 없는경우 실행하지 않는다.
        if (_CUR_PAGE_INDEX >= 0)
            dynamicFuncJS[$(vpCommon.wrapSelector(vpConst.AREA_BLUEPRINT, vpConst.OPTION_BLUEPRINT_ITEM + "." + vpConst.OPTION_BLUEPRINT_FOCUSED_ITEM)).index()].generateCode(excute);
    }

    return { containerInit: containerInit
    // TEST: 김민주 코드 추가 : 다른 옵션페이지로 넘어가는 함수 필요 (matplotlib/figure.js)
    , tabPageShow: tabPageShow};
});
