define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpXMLHandler'
    , 'nbextensions/visualpython/src/pandas/fileNavigation/index'
    , 'nbextensions/visualpython/src/common/component/vpTab'
    , 'nbextensions/visualpython/src/common/component/vpIconInputText'
    , 'nbextensions/visualpython/src/common/component/vpAccordionBox'
], function (requirejs, $, vpCommon, sb, vpConst, xmlHandler, fileNavigation, vpTab, vpIconInputText, vpAccordionBox) {
    "use strict";

    /** 전역 변수 영역 시작 */

    let xmlLibraries;
    let libraryLoadComplete = false;
    let loadedFuncJS;
    let apiBlockJS;
    let generatedCode;
    let generatedMetaData;
    let loadedFuncID;
    var events;
    let nodeIndex = 0;

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
    /** 전역 변수 영역 끝 */

    
    /** 컨트롤 초기화 영역 시작 */

    /**
     * 메인 UI init
     */
    var containerInit = function() {
        apiModeInit();
    }

    /**
     * API Mode html initialize
     */
    var apiModeInit = function() {
        // api 탭 생성
        var apiTypeTab = new vpTab.vpTab();
        apiTypeTab.addTabPage(vpConst.API_LIST_CAPTION);
        apiTypeTab.addTabPage(vpConst.API_BLOCK_CAPTION);
        
        $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_MODE_CONTAINER))).append(apiTypeTab.toTagString());

        // api list 페이지 바인딩
        $(apiTypeTab.pageSelector(0)).append(apiListPageInit());
        
        // 라이브러리 바인딩.
        loadLibraries($(apiTypeTab.pageSelector(0)).children(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER)));
        
        // api block 페이지 바인딩
        // $(apiTypeTab.pageSelector(1)).append("TEST PAGE FOR API BLOCK TAB PAGE!")
        $(apiTypeTab.pageSelector(1)).append(apiBlockPageInit());

        // api block load call
        loadApiBlock($(apiTypeTab.pageSelector(1)).children(vpCommon.formatString("#{0}", vpConst.API_BLOCK_CONTAINER)));
    }

    /**
     * API List Mode tab page initialize
     * @returns api list tab page
     */
    var apiListPageInit = function() {
        var sbApiListPage = new sb.StringBuilder();

        // 라이브러리 리스트(네비게이터) 영역
        sbApiListPage.appendFormatLine("<div id='{0}'>", vpConst.API_LIST_LIBRARY_LIST_CONTAINER);

        // 검색 컨트롤 추가
        var searchBox = new vpIconInputText.vpIconInputText();
        searchBox.setIconClass("srch-icon");
        searchBox.setPlaceholder("search");
        sbApiListPage.appendLine(searchBox.toTagString());
        // 검색 아이콘 클릭 이벤트 바인딩
        searchBox.addEvent("click", "icon", function() { searchAPIList($(this).parent().children("input").val()); });

        sbApiListPage.appendLine("</div>");
        
        // 옵션 로드용 임시 영역
        sbApiListPage.appendFormatLine("<div id='{0}'></div>", vpConst.OPTION_GREEN_ROOM.replace("#", ""));

        // 옵션 표시 영역
        sbApiListPage.appendFormatLine("<div id='{0}' style='display:none;'>", vpConst.OPTION_CONTAINER);

        // 옵션 컨트롤 영역
        sbApiListPage.appendFormatLine("<div id='{0}'>", vpConst.OPTION_CONTROL_PANEL);

        // 옵션 네비 인포 영역
        sbApiListPage.appendFormatLine("<div id='{0}'></div>", vpConst.OPTION_NAVIGATOR_INFO_PANEL);
        
        // 로드 옵션 설정창 닫기 버튼
        sbApiListPage.appendFormatLine("<div id='{0}'></div>", vpConst.CLOSE_OPTION_BUTTON);
        
        // 옵션 액션 버튼 컨테이너
        sbApiListPage.appendFormatLine("<div id='{0}'>", vpConst.ACTION_OPTION_BUTTON_PANEL);

        sbApiListPage.appendFormatLine("<span type='button' class='{0} {1}' id='{2}'>Add</span>"
            , vpConst.ACTION_OPTION_BUTTON, vpConst.COLOR_BUTTON_WHITE_ORANGE, vpConst.OPTION_BTN_ADD_CELL);

        sbApiListPage.appendFormatLine("<span type='button' class='{0} {1}' id='{2}'>Run</span>"
            , vpConst.ACTION_OPTION_BUTTON, vpConst.COLOR_BUTTON_ORANGE_WHITE, vpConst.OPTION_BTN_RUN_CELL);

        sbApiListPage.appendFormatLine("<div id={0}></div>", vpConst.OPTION_BTN_SAVE_ON_NOTE);
        
        sbApiListPage.appendLine("</div>");
        
        // 로드된 옵션 위치 영역
        sbApiListPage.appendFormatLine("<div id='{0}'></div>", vpConst.OPTION_LOAD_AREA);
        
        sbApiListPage.appendLine("</div>");

        sbApiListPage.appendLine("</div>");

        return sbApiListPage.toString();
    }

    /**
     * API Block tab page initialize
     * @returns api list tab page
     */
    var apiBlockPageInit = function() {
        var sbApiBlockPage = new sb.StringBuilder();
        // api block wrap 영역
        sbApiBlockPage.appendFormatLine("<div id='{0}'>", vpConst.API_BLOCK_CONTAINER);
        
        // 옵션 액션 버튼 컨테이너
        sbApiBlockPage.appendFormatLine("<div id='{0}{1}'>", vpConst.VP_ID_PREFIX, "BlockActionContainer");

        sbApiBlockPage.appendFormatLine("<span type='button' class='{0} {1}' id='{2}'>Add</span>"
            , vpConst.ACTION_OPTION_BUTTON, vpConst.COLOR_BUTTON_WHITE_ORANGE, "vp_blockAddOnCell");

        sbApiBlockPage.appendFormatLine("<span type='button' class='{0} {1}' id='{2}'>Run</span>"
            , vpConst.ACTION_OPTION_BUTTON, vpConst.COLOR_BUTTON_ORANGE_WHITE, "vp_blockRunCell");
    
        sbApiBlockPage.appendLine("</div>");

        sbApiBlockPage.appendLine("</div>");
        return sbApiBlockPage.toString();
    }

    /**
     * load libraries data
     * @param {Tag} container loaded libray binding container
     */
    var loadLibraries = function(container) {
        var libraryURL = window.location.origin + vpConst.PATH_SEPARATOR + vpConst.BASE_PATH + vpConst.DATA_PATH + vpConst.VP_LIBRARIES_XML_URL;
        xmlLibraries = new xmlHandler.VpXMLHandler(libraryURL);
        xmlLibraries.loadFile(libraryLoadCallback, container);
    }

    /**
     * library load complete callback
     * @param {Tag} container loaded libray binding container
     */
    var libraryLoadCallback = function(container) {
        setLibraryLoadComplete();
        librariesBind($(xmlLibraries.getXML()).children(vpConst.LIBRARY_ITEM_WRAP_NODE), container);
        
        // bindSearchAutoComplete();
    };

    /**
     * 라이브러르 로드 상태 변경 및 변경완료 트리거 발동
     */
    var setLibraryLoadComplete = function() {
        libraryLoadComplete = true;
        events.trigger('library_load_complete.vp');
    }

    /**
     * api list initialize
     * @param {xmlNode} node mother node for binding
     * @param {Tag} container loaded libray binding container
     */
    var librariesBind = function(node, container) {
        
        $(node).children(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_TYPE_ATTR + "=" + vpConst.LIBRARY_ITEM_TYPE_PACKAGE + "]").each(function() {
            var thisNode = $(this);
            var accboxTopGrp;
            if ($(thisNode).attr(vpConst.LIBRARY_ITEM_DEPTH_ATTR) == 0) {
                accboxTopGrp = makeLibraryTopGroupBox($(thisNode));
                
                $(container).append(accboxTopGrp.toTagString());
            }
        });
    }

    /**
     * 최상위 패키지는 아코디언 박스로 생성한다.
     * @param {xmlNode} topGrpNode 최상위 페키지
     */
    var makeLibraryTopGroupBox = function(topGrpNode) {
        var accBox = new vpAccordionBox.vpAccordionBox($(topGrpNode).attr(vpConst.LIBRARY_ITEM_NAME_ATTR), false, true);

        // 속성 부여
        accBox.addAttribute(vpConst.LIBRARY_ITEM_DATA_ID, $(topGrpNode).attr(vpConst.LIBRARY_ITEM_ID_ATTR));

        // 자식 그룹 노드 생성
        accBox.appendContent(makeLibraryListsGroupNode(topGrpNode));
        
        return accBox;
    }

    /**
     * 그룹 노드 리스트 아이템으로 생성
     * @param {xmlNode} grpNode 그룹 노드
     */
    var makeLibraryListsGroupNode = function(grpNode) {
        var sbGrpNode = new sb.StringBuilder();
        
        sbGrpNode.appendLine(makeLibraryListsFunctionNode(grpNode));
        
        sbGrpNode.appendFormatLine("<ul class='{0}' {1}>", vpConst.LIST_ITEM_LIBRARY, $(grpNode).attr(vpConst.LIBRARY_ITEM_DEPTH_ATTR) > 0 ? "style='display:none;'" : "");

        $(grpNode).children(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_TYPE_ATTR + "=" + vpConst.LIBRARY_ITEM_TYPE_PACKAGE + "]").each(function() {
            sbGrpNode.appendFormatLine("<li class='{0}' {1}='{2}'>{3}"
                , vpConst.LIST_ITEM_LIBRARY_GROUP, vpConst.LIBRARY_ITEM_DATA_ID, $(this).attr(vpConst.LIBRARY_ITEM_ID_ATTR), $(this).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
            
            sbGrpNode.appendLine(makeLibraryListsGroupNode($(this)));
            
            sbGrpNode.appendLine("</li>");
        });
        sbGrpNode.appendLine("</ul>");
        
        return sbGrpNode.toString();
    }

    /**
     * 함수 노드 리스트 아이템으로 생성
     * @param {xmlNode} grpNode 그룹 노드
     */
    var makeLibraryListsFunctionNode = function(grpNode) {
        var sbFuncNode = new sb.StringBuilder();

        sbFuncNode.appendFormatLine("<ul class='{0}' {1}>", vpConst.LIST_ITEM_LIBRARY, $(grpNode).attr(vpConst.LIBRARY_ITEM_DEPTH_ATTR) > 0 ? "style='display:none;'" : "");

        $(grpNode).children(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_TYPE_ATTR + "=" + vpConst.LIBRARY_ITEM_TYPE_FUNCTION + "]").each(function() {
            sbFuncNode.appendFormatLine("<li class='{0}' {1}='{2}'>{3}</li>"
                , vpConst.LIST_ITEM_LIBRARY_FUNCTION, vpConst.LIBRARY_ITEM_DATA_ID, $(this).attr(vpConst.LIBRARY_ITEM_ID_ATTR), $(this).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
        });

        sbFuncNode.appendLine("</ul>");

        return sbFuncNode.toString();
    }

    /**
     * load api block
     */
    var loadApiBlock = function() {
        // library 정보 로드 종료되지 않으면 이벤트로 등록
        if (!libraryLoadComplete) {
            events.on('library_load_complete.vp', loadApiBlock);
            return;
        }

        events.off('library_load_complete.vp', loadApiBlock);
        var loadUrl = getOptionPageURL("api_block");
        // 옵션 페이지 url 로딩이 정상처리 된 경우 js 파일 로드
        if (loadUrl !== "") {
            // 옵션 로드
            requirejs([loadUrl], function (loaded) {
                loaded.initOption(apiBlockLoadCallback);
            });
        }
    }

    /** 컨트롤 초기화 영역 끝 */
    
    /** 이벤트 핸들러 영역 시작 */
    
    /**
     * api list library 검색
     * @param {String} keyword 검색어
     */
    var searchAPIList = function(keyword) {
        alert(vpCommon.formatString("search keyword > {0}", keyword));
    }

    /**
     * 공통 컴퍼넌트 탭 체인지
     * @param {object} trigger 이벤트 트리거 객체
     */
    var vpTabPageChange = function(trigger) {
        // 활성화 탭인경우 동작없음
        if ($(trigger).hasClass("active")) return;

        var openPageID = $(trigger).attr("rel");
        
        $(trigger).parent().parent()
            .children(vpCommon.formatString(".{0}{1}", vpConst.VP_CLASS_PREFIX, "tab-content"))
            .children(vpCommon.formatString(".{0}{1}", vpConst.VP_CLASS_PREFIX, "tab-page")).hide();
        $(trigger).parent().parent().find(vpCommon.formatString("#{0}", openPageID)).show();
        $(trigger).parent().children(".active").removeClass("active");
        $(trigger).addClass("active");
    }

    /**
     * 공통 컴퍼넌트 아코디언 박스 내용 표시 토글
     * @param {object} trigger 이벤트 트리거 객체
     */
    var toggleAccordionBoxShow = function(trigger) {
        // 유니크 타입인경우 다른 아코디언 박스를 닫는다.
        if ($(trigger).parent().hasClass("uniqueType")) {
            $(trigger.parent().parent().children(vpCommon.formatString(".{0}", vpConst.ACCORDION_CONTAINER)).not($(trigger).parent()).removeClass("accordion-open"));
        }
        $(trigger).parent().toggleClass("accordion-open");

        // API List library 인 경우 추가 처리.
        if ($(trigger).parent().parent().attr("id") == vpConst.API_LIST_LIBRARY_LIST_CONTAINER) {
            closeSubLibraryGroup();
        }
    }

    /**
     * api list 그룹 하위 표시 토글
     * @param {object} trigger 이벤트 트리거 객체
     */
    var toggleApiListSubGroupShow = function(trigger) {
        $(trigger).parent().children(vpCommon.formatString("li.{0}", vpConst.LIST_ITEM_LIBRARY_GROUP)).not($(trigger)).find(vpCommon.formatString(".{0}", vpConst.LIST_ITEM_LIBRARY)).hide();
        $(trigger).children(vpCommon.formatString(".{0}", vpConst.LIST_ITEM_LIBRARY)).toggle();
    }

    /**
     * api list 그룹 하위 모두 숨기기
     */
    var closeSubLibraryGroup = function() {
        $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER), 
            vpCommon.formatString(".{0}{1}", vpConst.VP_CLASS_PREFIX, "accordion-content"))).children(vpCommon.formatString(".{0}", vpConst.LIST_ITEM_LIBRARY))
                .find(vpCommon.formatString(".{0}", vpConst.LIST_ITEM_LIBRARY)).hide();
    }

    /**
     * 옵션 페이지 로드
     * @param {String} funcID xml 함수 id
     * @param {function} callback 로드 완료시 실행할 함수
     */
    var loadOption = function(funcID, callback) {
        var loadUrl = getOptionPageURL(funcID);
        // 옵션 페이지 url 로딩이 정상처리 된 경우 js 파일 로드
        if (loadUrl !== "") {
            // 옵션 로드
            loadedFuncID = funcID;
            generatedCode = undefined;
            requirejs([loadUrl], function (loaded) {
                loaded.initOption(callback);
            });
        }
    }

    /**
     * 옵션 페이지 로드 완료 callback.
     * @param {funcJS} funcJS 옵션 js 객체
     */
    var optionPageLoadCallback = function(funcJS) {
        $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).children(vpConst.OPTION_PAGE).remove();

        loadedFuncJS = funcJS;

        var naviInfoTag = makeOptionPageNaviInfo($(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_ID_ATTR + "=" + loadedFuncID + "]"));
        // FIXME: funcJS 내부 id libraries.xml 과 매칭 필요
        // var naviInfoTag = makeOptionPageNaviInfo($(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_ID_ATTR + "=" + loadedFuncJS.funcID + "]"));
        $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_NAVIGATOR_INFO_PANEL))).append(naviInfoTag);
        makeUpGreenRoomHTML();
    }

    /**
     * api block 로드 완료 callback
     * @param {funcJS} funcJS 옵션 js 객체
     */
    var apiBlockLoadCallback = function(funcJS) {
        $(vpCommon.wrapSelector(vpConst.OPTION_GREEN_ROOM, vpCommon.formatString(".{0}", vpConst.API_OPTION_PAGE))).each(function() {
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_BLOCK_CONTAINER))).append($(this));
        });
        apiBlockJS = funcJS;
        // var trigger = $(vpCommon.wrapSelector(
        //     vpCommon.formatString(".{0}", vpConst.TAB_CONTAINER)
        //     , vpCommon.formatString(".{0}", vpConst.TAB_HEAD_CONTROL)
        //     , vpCommon.formatString("li[rel={0}{1}", vpConst.VP_ID_PREFIX, vpConst.API_BLOCK_CAPTION.replace(/ /gi, ""))));
        // vpTabPageChange(trigger);
    }
    /**
     * 로드된 함수 경로 바인딩
     * @param {xmlNode} node node for binding
     */
    var makeOptionPageNaviInfo = function(node) {
        var sbNaviInfo = new sb.StringBuilder();
        
        if ($(node).parent().attr(vpConst.LIBRARY_ITEM_DEPTH_ATTR) !== undefined) {
            sbNaviInfo.appendLine(makeOptionPageNaviInfo($(node).parent()));
        }

        sbNaviInfo.appendFormatLine("<span class='{0}' {1}={2}>{3}</span>"
            , vpConst.OPTION_NAVIGATOR_INFO_NODE, vpConst.LIBRARY_ITEM_DATA_ID, $(node).attr(vpConst.LIBRARY_ITEM_ID_ATTR), $(node).attr(vpConst.LIBRARY_ITEM_NAME_ATTR));
            
        return sbNaviInfo.toString();
    }

    /**
     * 로딩된 옵션 페이지 html 처리
     */
    var makeUpGreenRoomHTML = function() {
        $(vpCommon.wrapSelector(vpConst.OPTION_GREEN_ROOM, vpCommon.formatString(".{0}", vpConst.API_OPTION_PAGE))).each(function() {
            $(this).find("h4:eq(0)").hide();
            $(this).find("hr:eq(0)").hide();
            $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_LOAD_AREA))).append($(this));
        });

        openOptionBook();
    }

    /**
     * 옵션 페이지 URL 조회
     * @param {String} funcID xml 함수 id
     * @returns path url
     */
    var getOptionPageURL = function(funcID) {
        var sbURL = new sb.StringBuilder();
        
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

        sbURL.append(filePath);
        return sbURL.toString();
    }

    /**
     * open api option container
     */
    var openOptionBook = function() {
        $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER))).hide();
        $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_CONTAINER))).show();
    }

    /**
     * 로드된 옵션 페이지 닫기
     */
    var closeOptionBook = function() {
        $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER))).show();
        $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_CONTAINER))).hide();
        
        $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_NAVIGATOR_INFO_PANEL),
            vpCommon.formatString(".{0}", vpConst.OPTION_NAVIGATOR_INFO_NODE))).remove();
        $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_LOAD_AREA))).children().remove();
    }

    /**
     * 네비 항목 클릭하여 리스트로 이동
     * @param {object} trigger 이벤트 트리거 객체
     */
    var goListOnNavInfo = function(trigger) {
        console.log($(trigger).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, "")));
        
        var obj = $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER)))
            .children(vpCommon.formatString("div[{0}={1}]", vpConst.LIBRARY_ITEM_DATA_ID, $(trigger).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, ""))));

        // 최상위 그룹클릭인 경우
        if (obj.length > 0) {
            // 유니크 타입인경우 다른 아코디언 박스를 닫는다.
            if ($(obj).hasClass("uniqueType")) {
                $(obj.parent().children(vpCommon.formatString(".{0}", vpConst.ACCORDION_CONTAINER)).not($(obj)).removeClass("accordion-open"));
            }
            $(obj).addClass("accordion-open");
            // 하위 그룹 닫기
            closeSubLibraryGroup();
            closeOptionBook();
        } else {
            closeSubLibraryGroup();
            obj = $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.API_LIST_LIBRARY_LIST_CONTAINER)))
                .find(vpCommon.formatString("[{0}={1}]", vpConst.LIBRARY_ITEM_DATA_ID, $(trigger).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, ""))));
            
            obj.children(vpCommon.formatString(".{0}", vpConst.LIST_ITEM_LIBRARY)).show();
            var objParent = obj.parent();
            for (var loopSafety = 0; loopSafety < 10; loopSafety++) {
                // 부모 리스트 존재하면 표시
                if ($(objParent).hasClass(vpConst.LIST_ITEM_LIBRARY)) {
                    $(objParent).show();
                } else if ($(objParent).hasClass(vpConst.ACCORDION_CONTAINER)) {
                    // 유니크 타입인경우 다른 아코디언 박스를 닫는다.
                    if ($(objParent).hasClass("uniqueType")) {
                        $(objParent.parent().children(vpCommon.formatString(".{0}", vpConst.ACCORDION_CONTAINER)).not($(objParent)).removeClass("accordion-open"));
                    }
                    $(objParent).addClass("accordion-open");
                }
                objParent = $(objParent).parent();
                
                // 부모가 api list contianer 이면 종료
                if ($(objParent).attr("id") == vpConst.API_LIST_LIBRARY_LIST_CONTAINER) {
                    break;
                }
            }
            closeOptionBook();
        }
    }

    /**
     * 제네레이트 코드 셀에 추가. true 인 경우 바로 셀 실행
     * @param {funcJS} funcJS 옵션 js 객체
     * @param {boolean} run 실행여부
     * @param {function} callback 로드 완료시 실행할 함수
     */
    var addLibraryToJupyterCell = function(funcJS, run, callback) {
        // TODO: valitate
        if (!funcJS.optionValidation()) {
            return false;
        }
        // TODO: 타스크 추가
        funcJS.funcID = loadedFuncID;
        funcJS.generateCode(run);
        generatedCode = funcJS.generatedCode;
        generatedMetaData = funcJS.metadata;

        if (generatedCode === "BREAK_RUN") {
            // alert("Error occurred during add task. Request breaked.");
            console.log("[vp] Error occurred during add task. Request breaked.");
            // console.warn("generated code is undefined");
            return false;
        }
        
        // callback 함수가 존재하면 실행.
        if (callback !== undefined) {
            callback();
        }

        // closeOptionBook();
    }

    /**
     * vp note mode on off
     * @param {object} trigger 이벤트 트리거 객체
     */
    var toggleNoteMode = function(trigger) {
        var isOpen = $(trigger).hasClass(vpCommon.formatString("{0}{1}", vpConst.VP_CLASS_PREFIX, "on"));
        if (isOpen) {
            closeNoteArea();
        } else {
            openNoteArea();
        }
        // 버튼 클래스 토글
        // $(trigger).toggleClass(vpCommon.formatString("{0}{1}", vpConst.VP_CLASS_PREFIX, "on")).toggleClass(vpCommon.formatString("{0}{1}", vpConst.VP_CLASS_PREFIX, "off"));
    }

    var openNoteArea = function() {
        var btn = $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", "vp_NoteModeBtn")));
        $(vpCommon.wrapSelector(".vp-note-container")).show();
        $(btn).addClass(vpCommon.formatString("{0}{1}", vpConst.VP_CLASS_PREFIX, "on")).removeClass(vpCommon.formatString("{0}{1}", vpConst.VP_CLASS_PREFIX, "off"));
    }
    var closeNoteArea = function() {
        var btn = $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", "vp_NoteModeBtn")));
        $(vpCommon.wrapSelector(".vp-note-container")).hide();
        $(btn).addClass(vpCommon.formatString("{0}{1}", vpConst.VP_CLASS_PREFIX, "off")).removeClass(vpCommon.formatString("{0}{1}", vpConst.VP_CLASS_PREFIX, "on"));
    }
    /** 이벤트 핸들러 영역 끝 */

    /** 이벤트 바인딩 영역 시작 */
    
    /**
     * 공통 컴퍼넌트 탭 헤더 클릭
     */
    $(document).on("click", vpCommon.wrapSelector(vpCommon.formatString(".{0}", vpConst.TAB_CONTAINER), vpCommon.formatString(".{0}", vpConst.TAB_HEAD_CONTROL), "li"), function() {
        vpTabPageChange($(this));
    });

    /**
     * 모드 셀렉터 클릭
     */
    $(document).on("click", vpCommon.wrapSelector(vpCommon.formatString("#{0}", "vp_NoteModeBtn")), function() {
        toggleNoteMode($(this));
    });

    /**
     * 공통 컴퍼넌트 아코디언 박스 헤더 클릭
     */
    $(document).on("click", vpCommon.wrapSelector(vpCommon.formatString(".{0}", vpConst.ACCORDION_CONTAINER), vpCommon.formatString(".{0}", vpConst.ACCORDION_HEADER)), function() {
        toggleAccordionBoxShow($(this));
    });

    /**
     * api list item 클릭
     */
    $(document).on("click", vpCommon.wrapSelector(vpCommon.formatString(".{0} li", vpConst.LIST_ITEM_LIBRARY)), function(evt) {
        evt.stopPropagation();
        if ($(this).hasClass(vpConst.LIST_ITEM_LIBRARY_GROUP)) {
            toggleApiListSubGroupShow($(this));
        } else if ($(this).hasClass(vpConst.LIST_ITEM_LIBRARY_FUNCTION)) {
            loadOption($(this).data(vpConst.LIBRARY_ITEM_DATA_ID.replace(vpConst.TAG_DATA_PREFIX, "")), optionPageLoadCallback);
        }
    });

    /**
     * api option navi info item 클릭
     */
    $(document).on("click", vpCommon.wrapSelector(vpCommon.formatString(".{0}:not(:last-child)", vpConst.OPTION_NAVIGATOR_INFO_NODE)), function() {
        goListOnNavInfo($(this));
    });

    /**
     * api option add 버튼 클릭
     */
    $(document).on("click", vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_BTN_ADD_CELL)), function() {
        addLibraryToJupyterCell(loadedFuncJS ,false);
    });

    /**
     * api option run 버튼 클릭
     */
    $(document).on("click", vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_BTN_RUN_CELL)), function() {
        addLibraryToJupyterCell(loadedFuncJS, true);
    });

    /** FIXME: 임시 버튼
     * api block add 버튼 클릭
     */
    $(document).on("click", vpCommon.wrapSelector(vpCommon.formatString("#{0}", "vp_blockAddOnCell")), function() {
        addLibraryToJupyterCell(apiBlockJS, false);
    });

    /**
     * api block run 버튼 클릭
     */
    $(document).on("click", vpCommon.wrapSelector(vpCommon.formatString("#{0}", "vp_blockRunCell")), function() {
        addLibraryToJupyterCell(apiBlockJS, true);
    });

    /**
     * 옵션 설정 화면 닫기버튼 클릭
     */
    $(document).on("click", vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.CLOSE_OPTION_BUTTON)), function() {
        closeOptionBook();
    });

    /**
     * 노트에 저장 버튼 클릭
     */
    $(document).on("click", vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_BTN_SAVE_ON_NOTE)), function() {
        addLibraryToJupyterCell(loadedFuncJS, false, addNoteNode);
        openNoteArea();
    });
    

    /** 이벤트 바인딩 영역 끝 */

    /** 임시 이벤트(구버전) TODO: 향후 삭제 예정 */

    /**
     * 수직 최소화 버튼 클릭시 영역 표시 변환
     */
    $(document).on("click", vpCommon.wrapSelector(".vp-panel-area-vertical-btn"), function(evt) {
        evt.stopPropagation();
        toggleVerticalMinimizeArea($(this));
    });
    $(document).on("click", vpCommon.wrapSelector(".vp-minimize", "h4"), function(evt) {
        evt.stopPropagation();
        toggleVerticalMinimizeArea2($(this));
    });
    $(document).on("click", vpCommon.wrapSelector(".vp-spread", "h4"), function(evt) {
        evt.stopPropagation();
        toggleVerticalMinimizeArea2($(this));
    });

    /**
     * 영역 수직 최소화, 복원
     * @param {HTMLtag} btnObj 
     */
    var toggleVerticalMinimizeArea = function(btnObj) {
        $(btnObj).parent().parent().toggleClass("vp-spread").toggleClass("vp-minimize");
        $(btnObj).toggleClass("vp-arrow-up").toggleClass("vp-arrow-down");
    }
    var toggleVerticalMinimizeArea2 = function(obj) {
        $(obj).parent().toggleClass("vp-spread").toggleClass("vp-minimize");
        $(obj).parent().find(".vp-panel-area-vertical-btn").toggleClass("vp-arrow-up").toggleClass("vp-arrow-down");
    }

    /** 노트모드 임시 FIXME: 향후 수정 필요 */

    /**
     * 노트 노드 추가
     * @param {string} gCode generated code
     * @param {string} gMeta generated meta
     */
    var addNoteNode = function(gCode, gMeta) {
        gCode = generatedCode;
        gMeta = generatedMetaData;
        var sbNoteNode = new sb.StringBuilder();
        sbNoteNode.appendFormatLine("<div class='{0}'>", vpConst.NOTE_NODE_CLASS.replace(".", ""));
        sbNoteNode.appendFormatLine("<span class='{0}'>Node {1}</span>", vpConst.NOTE_NODE_INDEX.replace(".", ""), ++nodeIndex);
        sbNoteNode.appendFormat("<select class='{0}'>", vpConst.NOTE_NODE_TYPE.replace(".", ""));
        sbNoteNode.appendFormat("<option value='{0}'>{1}</option>", "list", "API List");
        sbNoteNode.appendFormat("<option value='{0}'>{1}</option>", "mark", "Markdown");
        sbNoteNode.appendFormat("<option value='{0}'>{1}</option>", "block", "API Block");
        sbNoteNode.appendLine("</select>");
        sbNoteNode.appendFormatLine("<span class='{0} {1}'>{2}</span>"
            , vpConst.NOTE_NODE_CODE.replace(".", ""), vpConst.NOTE_NODE_CODE_ELLIPSIS.replace(".", ""), gCode);
        sbNoteNode.appendFormat("<div class='{0}'>", vpConst.NOTE_BTN_CONTAINER.replace(".", ""));
        sbNoteNode.appendFormat("<button class='vp-btn vp-tiny {0}' type='button'><span>{1}</span></button>", "vp-node-open-option", "&lt;");
        sbNoteNode.appendFormat("<button class='vp-btn vp-tiny {0}' type='button'><span>{1}</span></button>", "vp-toggle-ellipsis", "+");
        sbNoteNode.appendFormat("<button class='vp-btn vp-tiny {0}' type='button'><span>{1}</span></button>", "vp-node-moveup", "U");
        sbNoteNode.appendFormat("<button class='vp-btn vp-tiny {0}' type='button'><span>{1}</span></button>", "vp-node-movedown", "D");
        sbNoteNode.appendFormat("<button class='vp-btn vp-tiny {0}' type='button'><span>{1}</span></button>", "vp-node-delete", "X");
        sbNoteNode.appendLine("</div>");
        sbNoteNode.appendFormatLine(`<input type="hidden" class="{0}" value="{1}" />`
            , vpConst.NOTE_NODE_GENE_META.replace(".", ""), encodeURIComponent(JSON.stringify(gMeta)));
        sbNoteNode.appendLine("</div>");

        $(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER)).append(sbNoteNode.toString());
    }

    var noteBrowser = function(obj) {
        // file navigation : state 데이터 목록
        this.state = {
            paramData:{
                encoding: "utf-8" // 인코딩
                , delimiter: ","  // 구분자
            },
            returnVariable:"",    // 반환값
            isReturnVariable: false,
            fileExtension: vpConst.VPNOTE_EXTENSION // 확장자
        }; 
        this.fileResultState = {
            pathInputId : vpCommon.wrapSelector('#noteFilePath')
        };
    }

    /**
     * 노트 모드 오픈
     */
    $(document).on("click", vpCommon.wrapSelector("#vp_openNote"), async function() {
        var loadURLstyle = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH;
        var loadURLhtml = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.SOURCE_PATH + "component/fileNavigation/index.html";
        
        vpCommon.loadCss( loadURLstyle + "component/fileNavigation.css");

        await $(`<div id="vp_fileNavigation"></div>`).load(loadURLhtml, () => {
            $('#vp_fileNavigation').removeClass("hide");
            $('#vp_fileNavigation').addClass("show");
            
            var {vp_init, vp_bindEventFunctions } = fileNavigation;
                
            fileNavigation.vp_init(nbNote);
            fileNavigation.vp_bindEventFunctions();
        }).appendTo("#site");
    });
    /**
     * 노트 저장
     */
    $(document).on("click", vpCommon.wrapSelector("#vp_saveNote"), async function() {
        // saveNoteFile();
        var loadURLstyle = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH;
        var loadURLhtml = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.SOURCE_PATH + "component/fileNavigation/index.html";
        
        vpCommon.loadCss( loadURLstyle + "component/fileNavigation.css");

        await $(`<div id="vp_fileNavigation"></div>`).load(loadURLhtml, () => {
            $('#vp_fileNavigation').removeClass("hide");
            $('#vp_fileNavigation').addClass("show");
            
            var {vp_init, vp_bindEventFunctions } = fileNavigation;
                
            fileNavigation.vp_init(nbNote, "SAVE_FILE");
            fileNavigation.vp_bindEventFunctions();
        }).appendTo("#site");
    });
    var nbNote = new noteBrowser(this);
    $(document).on("click", vpCommon.wrapSelector("#vp_closeNote"), function() {
        clearNoteArea();
        closeNoteArea();
    });
    $(document).on("click", vpCommon.wrapSelector("#vp_newNote"), function() {
        clearNoteArea();
    });
    /**
     * 노트 파일 로드
     */
    $(document).on("fileReadSelected.fileNavigation", function(e) {
        // 선택 파일 확장자가 노트 세이브 파일인 경우만 동작
        if (e.path.substring(e.path.lastIndexOf(".") + 1) === vpConst.VPNOTE_EXTENSION) {
            loadNoteFile();
        }
    });
    
    /**
     * 노트 파일 세이브
     */
    $(document).on("fileSaveSelected.fileNavigation", function(e) {
        // 선택 파일 확장자가 노트 세이브 파일인 경우만 동작
        if (e.path.substring(e.path.lastIndexOf(".") + 1) === vpConst.VPNOTE_EXTENSION) {
            saveNoteFile();
        }
    });
    var clearNoteArea = function() {
        $(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER, vpConst.NOTE_NODE_CLASS)).remove();
        nodeIndex = 0;
        $(vpCommon.wrapSelector(vpConst.VP_ID_PREFIX + "openVPNote")).removeClass("vp-on-btn");
    }
    /**
     * 노트 파일 저장
     */
    var saveNoteFile = function() {
        var noteClone = $(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER)).clone();
        $(noteClone).children().not(vpConst.NOTE_NODE_CLASS).remove();
        
        var sbNoteData = new sb.StringBuilder();
        sbNoteData.appendFormatLine("%%writefile {0}", $(vpCommon.wrapSelector('#noteFilePath')).val());
        sbNoteData.appendLine($(noteClone).html());

        Jupyter.notebook.kernel.execute(sbNoteData.toString());
    }
    /**
     * 노트 로딩
     */
    var loadNoteFile = function() {
        clearNoteArea();
        openNoteArea();

        fetch($(vpCommon.wrapSelector('#noteFilePath')).val())
            .then(data => data.text()).then(html => {
                $(vpCommon.wrapSelector(vpConst.VP_NOTE_CONTAINER)).append(html);
                nodeIndex = 0;
                $(html).find(vpConst.NOTE_NODE_INDEX).each(function() {
                    var tmp = $(this).html().replace("Node", "").trim();
                    if (tmp > nodeIndex) {
                        nodeIndex = tmp;
                    }
                });
            });
    }

    /**
     * 노트 노드 셀에 적용
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.NOTE_BTN_CONTAINER, "." + vpConst.VP_CLASS_PREFIX + "node-open-option"), function() {
        loadNoteNodeOption($(this));
    });
    /**
     * 노드 옵션 로드
     * @param {HTMLtag} btn 
     */
    var loadNoteNodeOption = function(btn) {
        $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_LOAD_AREA))).empty();
        $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_NAVIGATOR_INFO_PANEL),
            vpCommon.formatString(".{0}", vpConst.OPTION_NAVIGATOR_INFO_NODE))).remove();
        var value = decodeURIComponent($(btn).parent().parent().children(vpConst.NOTE_NODE_GENE_META).val());
        generatedMetaData = JSON.parse(value);

        loadOption(generatedMetaData.funcID, optionPageLoadCallbackAndLoad);
    }
    /**
     * 옵션 페이지 로드 완료 callback.
     * @param {funcJS} funcJS 옵션 js 객체
     */
    var optionPageLoadCallbackAndLoad = function(funcJS) {
        $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).children(vpConst.OPTION_PAGE).remove();

        loadedFuncJS = funcJS;

        var naviInfoTag = makeOptionPageNaviInfo($(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_ID_ATTR + "=" + loadedFuncID + "]"));
        loadedFuncJS.loadMeta(loadedFuncJS, generatedMetaData);
        $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_NAVIGATOR_INFO_PANEL))).append(naviInfoTag);
        makeUpGreenRoomHTML();
    }
    /**
     * 노트 노드 확장
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.NOTE_BTN_CONTAINER, "." + vpConst.VP_CLASS_PREFIX + "toggle-ellipsis"), function() {
        nodeToggleEllipsis($(this));
    });
    /**
     * 노드 코드 생략 토글
     * @param {HTMLtag} btn 
     */
    var nodeToggleEllipsis = function(btn) {
        $(btn).parent().parent().children(vpConst.NOTE_NODE_CODE)
            .toggleClass(vpConst.NOTE_NODE_CODE_ELLIPSIS.replace(".", "")).toggleClass(vpConst.NOTE_NODE_CODE_ALL.replace(".", ""));
        if ($(btn).parent().parent().children(vpConst.NOTE_NODE_CODE).hasClass(vpConst.NOTE_NODE_CODE_ALL.replace(".", ""))) {
            $(btn).text("-");
        } else {
            $(btn).text("+");
        }
    }
    /**
     * 노트 노드 위로
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.NOTE_BTN_CONTAINER, "." + vpConst.VP_CLASS_PREFIX + "node-moveup"), function() {
        // console.log(vpCommon.wrapSelector(vpConst.NOTE_BTN_CONTAINER, vpConst.VP_CLASS_PREFIX + "node-moveup"));
        nodeMoveUp($(this));
    });

    /**
     * 노드 위로
     * @param {HTMLtag} btn 
     */
    var nodeMoveUp = function(btn) {
        var thisIndex = $(btn).parent().parent().index(vpConst.NOTE_NODE_CLASS);
        if (thisIndex > 0) {
            $(btn).parent().parent().parent().children(vpConst.NOTE_NODE_CLASS + ":eq(" + (thisIndex - 1) + ")").before($(btn).parent().parent());
        }
    }
    /**
     * 노트 노드 아래로
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.NOTE_BTN_CONTAINER, "." + vpConst.VP_CLASS_PREFIX + "node-movedown"), function() {
        nodeMoveDown($(this))
    });
    /**
     * 노드 아래로
     * @param {HTMLtag} btn 
     */
    var nodeMoveDown = function(btn) {
        var thisIndex = $(btn).parent().parent().index(vpConst.NOTE_NODE_CLASS);

        if (thisIndex + 1 < $(btn).parent().parent().parent().children(vpConst.NOTE_NODE_CLASS).length) {
            $(btn).parent().parent().parent().children(vpConst.NOTE_NODE_CLASS + ":eq(" + (thisIndex + 1) + ")").after($(btn).parent().parent());
        }
    }
    /**
     * 노트 노드 제거
     */
    $(document).on("click", vpCommon.wrapSelector(vpConst.NOTE_BTN_CONTAINER, "." + vpConst.VP_CLASS_PREFIX + "node-delete"), function() {
        nodeDelete($(this))
    });
       /**
     * 노드 제거
     * @param {HTMLtag} btn 
     */
    var nodeDelete = function(btn) {
        $(btn).parent().parent().remove();
    }

    /**
     * TEST: minju: 옵션페이지에 multi code block load
     * @param {funcJS} funcJS 
     */
    var optionPageLoadCallbackWithData = function(funcJS, metadata) {
        $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_LOAD_AREA))).empty();
        $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_NAVIGATOR_INFO_PANEL),
            vpCommon.formatString(".{0}", vpConst.OPTION_NAVIGATOR_INFO_NODE))).remove();
        $(vpCommon.wrapSelector(vpConst.OPTION_CONTAINER)).children(vpConst.OPTION_PAGE).remove();

        loadedFuncJS = funcJS;
        generatedMetaData = metadata; // FIXME:
        
        var naviInfoTag = makeOptionPageNaviInfo($(xmlLibraries.getXML()).find(vpConst.LIBRARY_ITEM_TAG + "[" + vpConst.LIBRARY_ITEM_ID_ATTR + "=" + loadedFuncID + "]"));
        loadedFuncJS.loadMeta(loadedFuncJS, generatedMetaData);
        $(vpCommon.wrapSelector(vpCommon.formatString("#{0}", vpConst.OPTION_NAVIGATOR_INFO_PANEL))).append(naviInfoTag);
        makeUpGreenRoomHTML();
    }

    /** 임시 이벤트 끝 */

    return {
        containerInit: containerInit
        // TEST: minju: 옵션페이지 로드 필요
        , loadOption: loadOption
        , optionPageLoadCallbackWithData: optionPageLoadCallbackWithData
    };
});
