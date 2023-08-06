define ([
    'require'
], function(requirejs) {
    "use strict";

    /**
     * path separator
     */
    const PATH_SEPARATOR = "/";

    /**
     * base path
     */
    const BASE_PATH = "nbextensions" + PATH_SEPARATOR + "visualpython" + PATH_SEPARATOR;

    /**
     * source path
     */
    const SOURCE_PATH = "src" + PATH_SEPARATOR;

    /**
     * resource path
     */
    const RESOURCE_PATH = "resource" + PATH_SEPARATOR;

    /**
     * style sheet path
     */
    const STYLE_PATH = "css" + PATH_SEPARATOR;

    /**
     * data path
     */
    const DATA_PATH = "data" + PATH_SEPARATOR;

    /**
     * main style path
     */
    const MAIN_CSS_URL = "main.css";

    /**
     * libraries data path
     */
    const VP_LIBRARIES_XML_URL = "libraries.xml";
    // const VP_LIBRARIES_XML_URL = "libraries_dev.xml";

    /**
     * toolbar btn properties
     */
    const TOOLBAR_BTN_INFO = {
        HELP: "Visual Python 0.3.0"
        , ICON: "fa-angellist"
        , ID: "vpBtnToggle"
        , NAME: "toggle-vp"
        , PREFIX: "vp"
        , ICON_CONTAINER: ""
    }

    /**
     * VisualPython position metadata name
     */
    const VP_POSITION_META_NAME = "vpPosition";

    /**
     * VisualPython container id
     */
    const VP_CONTAINER_ID = "vp-wrapper";

    /**
     * container html path
     */
    const VP_CONTAINER_PAGE_URL = "container" + PATH_SEPARATOR + "vpContainer.html";

    /**
     * VisualPython tag id prefix
     */
    const VP_ID_PREFIX = "vp_";
    
    /**
     * VisualPython tag class prefix
     */
    const VP_CLASS_PREFIX = "vp-";
    const VP_CLASS_PREFIX_OLD = ".vp-";

    /**
     * html tag data attribute prefix
     */
    const TAG_DATA_PREFIX = "data-";

    /**
     * API Mode container id
     */
    const API_MODE_CONTAINER = VP_ID_PREFIX + "apiContainer";

    /**
     * API List caption
     */
    const API_LIST_CAPTION = "API List";

    /**
     * API Block caption
     */
    const API_BLOCK_CAPTION = "API Block";

    /**
     * tab control class
     */
    const TAB_CONTAINER = VP_CLASS_PREFIX + "tab-wrap";

    /**
     * tab header control class
     */
    const TAB_HEAD_CONTROL = VP_CLASS_PREFIX + "tab-header";

    /**
     * icon input text class name
     */
    const ICON_INPUT_TEXT = VP_CLASS_PREFIX + "icon-input-text"

    /**
     * Accordion continer class name
     */
    const ACCORDION_CONTAINER = VP_CLASS_PREFIX + "accordion-container";

    /**
     * Accordion head class name
     */
    const ACCORDION_HEADER = VP_CLASS_PREFIX + "accordion-header"
    
    /**
     * library item mother wrap node
     */
    const LIBRARY_ITEM_WRAP_NODE = "library";

    /**
     * library item type : package
     */
    const LIBRARY_ITEM_TYPE_PACKAGE = "package";

    /**
     * library item type : fucntion
     */
    const LIBRARY_ITEM_TYPE_FUNCTION = "function";

    /**
     * library xml item node name
     */
    const LIBRARY_ITEM_TAG = "item";

    /**
     * library xml item depth attribute
     */
    const LIBRARY_ITEM_DEPTH_ATTR = "level";

    /**
     * library xml item id attribute
     */
    const LIBRARY_ITEM_ID_ATTR = "id";

    /**
     * library xml item type attribute
     */
    const LIBRARY_ITEM_TYPE_ATTR = "type";

    /**
     * library xml item name attribute
     */
    const LIBRARY_ITEM_NAME_ATTR = "name";

    /**
     * library xml item tag attribute
     */
    const LIBRARY_ITEM_TAG_ATTR = "tag";

    /**
     * library xml item file url node
     */
    const LIBRARY_ITEM_FILE_URL_NODE = "file";

    /**
     * library xml item path url node
     */
    const LIBRARY_ITEM_PATH_NODE = "path";

    /**
     * library xml item desc url node
     */
    const LIBRARY_ITEM_DESCRIPTION_NODE = "desc";

    /**
     * attribute for library item content for html tag
     */
    const LIBRARY_ITEM_DATA_ID = TAG_DATA_PREFIX + "item-id";

    /**
     * api library list control class for group node
     */
    const LIST_ITEM_LIBRARY = VP_CLASS_PREFIX + "libraries-list";

    /**
     * api library list item class for group node
     */
    const LIST_ITEM_LIBRARY_GROUP = VP_CLASS_PREFIX + "libraries-group";

    /**
     * api library list item class for function node
     */
    const LIST_ITEM_LIBRARY_FUNCTION = VP_CLASS_PREFIX + "libraries-items";

    /**
     * api list library list container id
     */
    const API_LIST_LIBRARY_LIST_CONTAINER = VP_ID_PREFIX + "apiListLibContainer";

    /**
     * api block main container id
     */
    const API_BLOCK_CONTAINER = VP_ID_PREFIX + "apiBlockMainContainer";

    /**
     * temporary area for load option FIXME: 선택자 수정 필요
     */
    const OPTION_GREEN_ROOM = "#" + VP_ID_PREFIX + "optionGreenRoom";
    /**
     * FIXME: 항목 삭제 필요
     */
    const OPTION_PAGE = "." + VP_CLASS_PREFIX + "option-page";
    /**
     * container for loaded option
     */
    const OPTION_CONTAINER = VP_ID_PREFIX + "optionBook";

    /**
     * option control button panel
     */
    const OPTION_CONTROL_PANEL = VP_ID_PREFIX + "optionBookControl";

    /**
     * loaded option navigator info panel
     */
    const OPTION_NAVIGATOR_INFO_PANEL = VP_ID_PREFIX + "optionNaviInfo";

    /**
     * loaded option navigator info panel node
     */
    const OPTION_NAVIGATOR_INFO_NODE = VP_CLASS_PREFIX + "navi-node";

    /**
     * loaded option close button
     */
    const CLOSE_OPTION_BUTTON = VP_ID_PREFIX + "OptionBookClose";

    /**
     * loaded option action button container
     */
    const ACTION_OPTION_BUTTON_PANEL = VP_ID_PREFIX + "OptionActionContainer";

    /**
     * loaded option action button
     */
    const ACTION_OPTION_BUTTON = VP_CLASS_PREFIX + "opt-action-btn";

    /**
     * white box orange font color button class
     */
    const COLOR_BUTTON_WHITE_ORANGE = VP_CLASS_PREFIX + "cbtn-white-orange";

    /**
     * orange box white font color button class
     */
    const COLOR_BUTTON_ORANGE_WHITE = VP_CLASS_PREFIX + "cbtn-orange-white";

    /**
     * loaded option add on cell btn
     */
    const OPTION_BTN_ADD_CELL = VP_ID_PREFIX + "addOnCell";
    
    /**
     * loaded option add on cell and run btn
     */
    const OPTION_BTN_RUN_CELL = VP_ID_PREFIX + "runCell";
    
    /**
     * loaded option save on note btn
     */
    const OPTION_BTN_SAVE_ON_NOTE = VP_ID_PREFIX + "saveOnNote";

    /**
     * loaded option container
     */
    const OPTION_LOAD_AREA = VP_ID_PREFIX + "optionLoadArea";

    /**
     * option per tab page
     */
    const API_OPTION_PAGE = VP_CLASS_PREFIX + "option-page";

    
/**
 * note save file extension
 */
const VPNOTE_EXTENSION = "vp";
// FIXME: 이하 버림

const vpClassPrefix = ".vp-"
const vpIDPrefix = "#vp_";
const tagDataPrefix = "data-";
    /**
     * container style path
     */
    const vpContainerCssURL = "container" + PATH_SEPARATOR + "vpContainer.css";

    /**
     * VisualPython tag class prefix (private)
     */
    const vpClassPrefixNotSelector = "vp-";

    /**
     * main container header text
     */
    const vpHeaderText = vpClassPrefix + "header";

    /**
     * main container header buttons
     */
    const vpHeaderButtons = vpClassPrefix + "header-buttons";

    /**
     * arrow style change btn shape class
     */
    const arrowBtnUp = vpClassPrefixNotSelector + "arrow-up";

    /**
     * arrow style change btn shape class
     */
    const arrowBtnDown = vpClassPrefixNotSelector + "arrow-down";

    /**
     * arrow style change btn shape class
     */
    const arrowBtnLeft = vpClassPrefixNotSelector + "arrow-left";

    /**
     * arrow style change btn shape class
     */
    const arrowBtnRight = vpClassPrefixNotSelector + "arrow-right";
    
// TODO:

    /**
     * main container
     */
    const vpMainContainer = vpClassPrefix + "main-container";

    /**
     * body container
     */
    const vpBodyContainer = vpClassPrefix + "body-container";

    /**
     * body container
     */
    const vpNoteContainer = vpClassPrefix + "note-container";

    /**
     * home btn id
     */
    const btnModeSelector = vpIDPrefix + "goModeSelector";

    /**
     * mode selector page
     */
    const pageModeSelector = vpIDPrefix + "modeSelector";

    /**
     * api browser page
     */
    const pageAPIBrowser = vpIDPrefix + "APIBrowser";

    /**
     * api browser page
     */
    const pageWorkflow = vpIDPrefix + "workflow";

    /**
     * api group box
     */
    const apiGroupBox = vpClassPrefix + "api-group";

    /**
     * page header class
     */
    const pageHeader = vpClassPrefix + "page-header";

    /**
     * api browser function button class
     */
    const naviFuncionButton = vpClassPrefix + "navi-func-btn";
    
    /**
     * api browser function span class
     */
    const naviFunctionSpan = vpClassPrefix + "span-func";

    /**
     * api browser group span class
     */
    const naviGroupSpan = vpClassPrefix + "span-group";

    /**
     * api browser group hidden class
     */
    const naviGroupHidden = "vp-hidden";

    /**
     * api browser group show class
     */
    const naviGroupShow = "vp-show";

    /**
     * api browser group show toggle btn class
     */
    const naviGroupToggle = vpClassPrefix + "navi-group-toggle";

    /**
     * open note button
     */
    const loadNoteBtn = vpIDPrefix + "openNote";

    /**
     * note node button container
     */
    const noteNodeClass = vpClassPrefix + "note-node";
    
    /**
     * note node index class
     */
    const noteNodeIndex = vpClassPrefix + "node-index";
    
    /**
     * note node type selector class
     */
    const noteNodeType = vpClassPrefix + "node-type";

    /**
     * note node button container
     */
    const noteBtnContainer = vpClassPrefix + "note-node-btns";

    /**
     * note node of generated code
     */
    const noteNodeCode = vpClassPrefix + "node-gene-code";

    /**
     * note node of generated code ellipsis
     */
    const noteNodeCodeEllipsis = vpClassPrefix + "node-ellipsis";

    /**
     * note node of generated code ellipsis
     */
    const noteNodeCodeAll = vpClassPrefix + "node-all";

    /**
     * note node genereted meta
     */
    const noteNodeGeneMeta = vpClassPrefix + "gene-meta";

/**
 * area division container
 */
const areaDivContainer = vpIDPrefix + "divisionContainer";

/**
 * top container of task area
 */
const areaTaskManage = vpIDPrefix + "taskArea";

/**
 * top container of option area
 */
const areaGeneOption = vpIDPrefix + "optionArea";

/**
 * top container of blueprint area
 */
const areaBP = vpIDPrefix + "blueprintArea";

/**
 * top container of generate area
 */
const areaGene = vpIDPrefix + "generateArea";

/**
 * top container of library area
 */
const areaLib = vpIDPrefix + "libraryArea";

/**
 * library area child container
 */
const libSubContainer = vpClassPrefix + "library-sub";

/**
 * search result continer
 */
const srchRsltContainer = vpIDPrefix + "searchResults";

/**
 * user define variable list container
 */
const variableList = vpIDPrefix + "variableList";

/**
 * list grid header
 */
const listGridHeader = vpClassPrefix + "grid-header";

/**
 * search result item class
 */
const srchRsltItemClass = vpClassPrefix + "search-func";

/**
 * variable list item class
 */
const varListItemClass = vpClassPrefix + "var-list-item";

/**
 * naviagtor path item container
 */
const naviPathContainer = vpIDPrefix + "navigatorPath";

/**
 * naviagtor path item
 */
const naviPathItemClass = vpClassPrefix + "navi-path-item";

/**
 * naviagtor path item
 */
const naviPathItemDividerClass = vpClassPrefix + "navi-path-item-divider";

/**
 * navigator buttons container
 */
const naviBtnContainer = vpIDPrefix + "navigatorButtons";

/**
 * navigator button class
 */
const naviBtnClass = vpClassPrefix + "navi-btn";

/**
 * attribute for navi button content level
 */
const naviItemLevel = tagDataPrefix + "nav-class";

/**
 * attribute type navi button group content level
 */
const naviItemLevelGrp = "grp";

/**
 * attribute type navi button function content level
 */
const naviItemLevelFunc = "func";

/**
 * attribute type navi button prev group content level
 */
const naviItemLevelPrev = "prev";

/**
 * option tab header 
 */
const optTabItem = vpClassPrefix + "option-tab-page";

/**
 * container for loaded option tab header
 */
const optTabContainer = vpIDPrefix + "optionTab";

/**
 * container for loaded option blueprint
 */
const optBPContainer = vpClassPrefix + "blueprint-container";

/**
 * option blueprint item
 */
const optBPItem = vpClassPrefix + "blueprint-item";

/**
 * option blueprint item destroy
 */
const optBPItemClose = vpClassPrefix + "blueprint-item-destroy";

/**
 * showing loaded item style
 */
const optBPFocusedItem = vpClassPrefixNotSelector + "focused";

/**
 * task index label
 */
const optTaskIdxLabel = vpIDPrefix + "lblOptIdx";

/**
 * option kind label
 */
const optKindLabel = vpIDPrefix + "lblOptKind";

/**
 * temp cation for load new option
 */
const optHeaderTempCaption = tagDataPrefix + "temp-caption";

/**
 * option paging btn class
 */
const optPagingBtn = vpClassPrefix + "option-paging-btn";

/**
 * option save button id
 */
const optSaveBtn = vpIDPrefix + "optSave";

/**
 * option save and execute button id
 */
const optSaveExeBtn = vpIDPrefix + "optSaveExe";

/**
 * option cancel button id
 */
const optCancelBtn = vpIDPrefix + "optCancel";

/**
 * option page prev button id
 */
const optPrevPageBtn = vpIDPrefix + "optPrevPage";

/**
 * option page next button id
 */
const optNextPageBtn = vpIDPrefix + "optNextPage";

/**
 * opened area style class
 */
const openedAreaClass = vpClassPrefixNotSelector + "spread";

/**
 * closed area style class
 */
const closedAreaClass = vpClassPrefixNotSelector + "minimize";

/**
 * vertical text style
 */
const verticalTextClass = vpClassPrefixNotSelector + "vertical";

/**
 * multi language tag class
 */
const multiLangTagClass = vpClassPrefix + "multilang";

/**
 * tag attribute for multi language id
 */
const multiLangCaptionID = tagDataPrefix + "caption-id";

/**
 * sortable table class
 */
const sortableTableClass = vpClassPrefix + "tbl-sortable";

/**
 * sortable column class
 */
const sortableColumnClass = vpClassPrefix + "sortable-column";

/**
 * sort value wrapper class
 */
const sortValueWrapClass = vpClassPrefix + "sort-value";

/**
 * arrow up shape class
 */
const arrowUpClass = vpClassPrefix + "arrow-up";

/**
 * arrow down shape class
 */
const arrowDownClass = vpClassPrefix + "arrow-down";

/**
 * new task btn id
 */
const newTaskBtn = vpIDPrefix + "btnNewTask";

/**
 * task index cell class
 */
const taskIndexCell = vpClassPrefix + "task-index";

/**
 * task button class
 */
const taskBtn = vpClassPrefix + "task-btn";

/**
 * task index caption prefix
 */
const taskIndexPrefix = "T";

/**
 * task label class
 */
const taskLabelClass = vpClassPrefix + "task-src-view";

/**
 * task list class
 */
const taskListTable = vpClassPrefix + "task-tbl";

/**
 * task list item class
 */
const taskListRow = vpClassPrefix + "task-row";

/**
 * task command cell class
 */
const taskCmdCell = vpClassPrefix + "task-command-cell";

/**
 * task command btn class
 */
const taskCmdBtn = vpClassPrefix + "task-command";

/**
 * task command run btn class
 */
const taskCmdExeBtn = vpClassPrefix + "task-execute";

/**
 * task command stop btn class
 */
const taskCmdStopBtn = vpClassPrefix + "task-stop";

/**
 * task add line class
 */
const taskAddCmd = vpClassPrefix + "add-task";

    return {
        PATH_SEPARATOR: PATH_SEPARATOR
        , BASE_PATH: BASE_PATH
        , SOURCE_PATH: SOURCE_PATH
        , RESOURCE_PATH: RESOURCE_PATH
        , STYLE_PATH: STYLE_PATH
        , DATA_PATH: DATA_PATH
        , MAIN_CSS_URL: MAIN_CSS_URL
        , VP_LIBRARIES_XML_URL: VP_LIBRARIES_XML_URL
        , TOOLBAR_BTN_INFO: TOOLBAR_BTN_INFO
        , VP_POSITION_META_NAME: VP_POSITION_META_NAME
        , VP_CONTAINER_ID: VP_CONTAINER_ID
        , VP_CONTAINER_PAGE_URL: VP_CONTAINER_PAGE_URL
        , VP_ID_PREFIX: VP_ID_PREFIX
        , VP_CLASS_PREFIX: VP_CLASS_PREFIX
		, VP_CLASS_PREFIX_OLD: VP_CLASS_PREFIX_OLD
        , TAG_DATA_PREFIX: TAG_DATA_PREFIX
        , API_MODE_CONTAINER: API_MODE_CONTAINER
        , API_LIST_CAPTION: API_LIST_CAPTION
        , API_BLOCK_CAPTION: API_BLOCK_CAPTION
        , TAB_CONTAINER: TAB_CONTAINER
        , TAB_HEAD_CONTROL: TAB_HEAD_CONTROL
        , ICON_INPUT_TEXT: ICON_INPUT_TEXT
        , ACCORDION_CONTAINER: ACCORDION_CONTAINER
        , ACCORDION_HEADER: ACCORDION_HEADER
        , LIBRARY_ITEM_WRAP_NODE: LIBRARY_ITEM_WRAP_NODE
        , LIBRARY_ITEM_TYPE_PACKAGE: LIBRARY_ITEM_TYPE_PACKAGE
        , LIBRARY_ITEM_TYPE_FUNCTION: LIBRARY_ITEM_TYPE_FUNCTION
        , LIBRARY_ITEM_TAG: LIBRARY_ITEM_TAG
        , LIBRARY_ITEM_DEPTH_ATTR: LIBRARY_ITEM_DEPTH_ATTR
        , LIBRARY_ITEM_ID_ATTR: LIBRARY_ITEM_ID_ATTR
        , LIBRARY_ITEM_TYPE_ATTR: LIBRARY_ITEM_TYPE_ATTR
        , LIBRARY_ITEM_NAME_ATTR: LIBRARY_ITEM_NAME_ATTR
        , LIBRARY_ITEM_TAG_ATTR: LIBRARY_ITEM_TAG_ATTR
        , LIBRARY_ITEM_FILE_URL_NODE: LIBRARY_ITEM_FILE_URL_NODE
        , LIBRARY_ITEM_PATH_NODE: LIBRARY_ITEM_PATH_NODE
        , LIBRARY_ITEM_DESCRIPTION_NODE: LIBRARY_ITEM_DESCRIPTION_NODE
        , LIBRARY_ITEM_DATA_ID: LIBRARY_ITEM_DATA_ID
        , LIST_ITEM_LIBRARY: LIST_ITEM_LIBRARY
        , LIST_ITEM_LIBRARY_GROUP: LIST_ITEM_LIBRARY_GROUP
        , LIST_ITEM_LIBRARY_FUNCTION: LIST_ITEM_LIBRARY_FUNCTION
        , API_LIST_LIBRARY_LIST_CONTAINER: API_LIST_LIBRARY_LIST_CONTAINER
        , API_BLOCK_CONTAINER: API_BLOCK_CONTAINER
        , OPTION_GREEN_ROOM: OPTION_GREEN_ROOM
        , OPTION_PAGE: OPTION_PAGE
        , OPTION_CONTAINER: OPTION_CONTAINER
        , OPTION_CONTROL_PANEL: OPTION_CONTROL_PANEL
        , OPTION_NAVIGATOR_INFO_PANEL: OPTION_NAVIGATOR_INFO_PANEL
        , OPTION_NAVIGATOR_INFO_NODE: OPTION_NAVIGATOR_INFO_NODE
        , CLOSE_OPTION_BUTTON: CLOSE_OPTION_BUTTON
        , ACTION_OPTION_BUTTON_PANEL: ACTION_OPTION_BUTTON_PANEL
        , ACTION_OPTION_BUTTON: ACTION_OPTION_BUTTON
        , COLOR_BUTTON_WHITE_ORANGE: COLOR_BUTTON_WHITE_ORANGE
        , COLOR_BUTTON_ORANGE_WHITE: COLOR_BUTTON_ORANGE_WHITE
        , OPTION_BTN_ADD_CELL: OPTION_BTN_ADD_CELL
        , OPTION_BTN_RUN_CELL: OPTION_BTN_RUN_CELL
        , OPTION_BTN_SAVE_ON_NOTE: OPTION_BTN_SAVE_ON_NOTE
        , OPTION_LOAD_AREA: OPTION_LOAD_AREA
        , API_OPTION_PAGE: API_OPTION_PAGE
        
, VPNOTE_EXTENSION: VPNOTE_EXTENSION
    // }
    // return {
        , VP_CONTAINER_CSS_URL: vpContainerCssURL
        // , VP_LIBRARIES_XML_URL: vpLibrariesURL

        , VP_HEADER_TEXT: vpHeaderText
        , VP_HEADER_BUTTONS: vpHeaderButtons
        , ARROW_BTN_UP: arrowBtnUp
        , ARROW_BTN_DOWN: arrowBtnDown
        , ARROW_BTN_LEFT: arrowBtnLeft
        , ARROW_BTN_RIGHT: arrowBtnRight

        , VP_MAIN_CONTAINER: vpMainContainer
        , VP_BODY_CONTAINER: vpBodyContainer
        , VP_NOTE_CONTAINER: vpNoteContainer
        , BTN_MODE_SELECTOR: btnModeSelector
        , PAGE_MODE_SELECTOR: pageModeSelector
        , PAGE_API_BROWSER: pageAPIBrowser
        , PAGE_WORKFLOW: pageWorkflow
        , API_GROUP_BOX: apiGroupBox
        , VP_PAGE_HEADER: pageHeader
        , NAVI_FUNCION_BUTTON: naviFuncionButton
        , NAVI_FUNCTION_SPAN: naviFunctionSpan
        , NAVI_GROUP_SPAN: naviGroupSpan
        , NAVI_GROUP_HIDDEN: naviGroupHidden
        , NAVI_GROUP_SHOW: naviGroupShow
        , NAVI_GROUP_TOGGLE: naviGroupToggle
        , LOAD_NOTE_BTN: loadNoteBtn
        , NOTE_NODE_CLASS: noteNodeClass
        , NOTE_NODE_INDEX: noteNodeIndex
        , NOTE_NODE_TYPE: noteNodeType
        , NOTE_BTN_CONTAINER: noteBtnContainer
        , NOTE_NODE_CODE: noteNodeCode
        , NOTE_NODE_CODE_ELLIPSIS: noteNodeCodeEllipsis
        , NOTE_NODE_CODE_ALL: noteNodeCodeAll
        , NOTE_NODE_GENE_META: noteNodeGeneMeta

    , AREA_DIVISION_CONTAINER: areaDivContainer
    , AREA_TASK_MANAGEMENT: areaTaskManage
    , AREA_GENERATE_OPTION: areaGeneOption
    , AREA_BLUEPRINT: areaBP
    , AREA_GENERATE: areaGene
    , AREA_LIBRARY: areaLib
    , LIBRARY_SUB_CONTAINER: libSubContainer
    , SEARCH_RESULT_CONTAINER: srchRsltContainer
    , VARIABLE_LIST_CONTAINER: variableList
    , LIST_GRID_HEADER: listGridHeader
    , SEARCH_RESULT_ITEM_CLASS: srchRsltItemClass
    , VARIABLE_LIST_ITEM_CLASS: varListItemClass
    , NAVIGATOR_PATH_ITEM_CONTAINER: naviPathContainer
    , NAVIGATOR_PATH_ITEM_CLASS: naviPathItemClass
    , NAVIGATOR_PATH_ITEM_DIVIDER: naviPathItemDividerClass
    , NAVIGATOR_BUTTON_CONTAINER: naviBtnContainer
    , NAVIGATOR_BUTTON_CLASS: naviBtnClass
    , NAVIGATOR_BUTTON_LEVEL: naviItemLevel
    , NAVIGATOR_BUTTON_LEVEL_GROUP: naviItemLevelGrp
    , NAVIGATOR_BUTTON_LEVEL_FUNCTION: naviItemLevelFunc
    , NAVIGATOR_BUTTON_LEVEL_PREV_GROUP: naviItemLevelPrev
    , OPTION_TAB_ITEM: optTabItem
    , OPTION_TAB_CONTAINER: optTabContainer
    , OPTION_BLUEPRINT_CONTAINER: optBPContainer
    , OPTION_BLUEPRINT_ITEM: optBPItem
    , OPTION_BLUEPRINT_ITEM_CLOSE: optBPItemClose
    , OPTION_BLUEPRINT_FOCUSED_ITEM: optBPFocusedItem
    , OPTION_TASK_INDEX_LABEL: optTaskIdxLabel
    , OPTION_KIND_LABEL: optKindLabel
    , OPTION_HEADER_TEMP_CAPTION: optHeaderTempCaption
    , OPTION_PAGING_BUTTON: optPagingBtn
    , OPTION_SAVE_BUTTON: optSaveBtn
    , OPTION_SAVE_EXECUTE_BUTTON: optSaveExeBtn
    , OPTION_CANCEL_BUTTON: optCancelBtn
    , OPTION_PREV_PAGE_BUTTON: optPrevPageBtn
    , OPTION_NEXT_PAGE_BUTTON: optNextPageBtn
    , OPENED_AREA_CLASS: openedAreaClass
    , CLOSED_AREA_CLASS: closedAreaClass
    , VERTICAL_TEXT_CLASS: verticalTextClass
    , MULTI_LANGUAGE_CLASS: multiLangTagClass
    , LANGUAGE_CAPTION_ID: multiLangCaptionID
    , SORTABLE_TABLE_CLASS: sortableTableClass
    , SORTABLE_COLUMN_CLASS: sortableColumnClass
    , SORT_VALUE_WRAP_CLASS: sortValueWrapClass
    , ARROW_UP_CLASS: arrowUpClass
    , ARROW_DOWN_CLASS: arrowDownClass
    , NEW_TASK_BUTTON: newTaskBtn
    , TASK_INDEX_CELL: taskIndexCell
    , TASK_BUTTON: taskBtn
    , TASK_INDEX_PREFIX: taskIndexPrefix
    , TASK_LABEL_CONTROL: taskLabelClass
    , TASK_LIST_TABLE: taskListTable
    , TASK_LIST_ROW: taskListRow
    , TASK_COMMAND_CELL: taskCmdCell
    , TASK_COMMAND_BUTTON: taskCmdBtn
    , TASK_COMMAND_EXECUTE_BUTTON: taskCmdExeBtn
    , TASK_COMMAND_STOP_BUTTON: taskCmdStopBtn
    , TASK_ADD_CMD: taskAddCmd
    };
});
