define([
    'nbextensions/visualpython/src/common/constant'
], function ( vpConstant ) {
    const { VP_CLASS_PREFIX_OLD, VP_CLASS_PREFIX } = vpConstant;

    /** ---------------------------------------- API block에서 쓰이는 ENUM TYPE ------------------------------------------ */
    const BLOCK_CODELINE_BTN_TYPE = {
        CLASS: 1
        , DEF: 2
        , IF: 3
        , FOR: 4
        , WHILE: 5
        , IMPORT: 6
        , API: 7
        , TRY: 8
    
        , RETURN: 9
        , BREAK: 10
        , CONTINUE: 11
        , PASS: 12
        , PROPERTY: 13

        , CODE: 999
    }
    
    const BLOCK_CODELINE_TYPE = {
        CLASS: 1
        , DEF: 2
        , IF: 3
        , FOR: 4
        , WHILE: 5
        , IMPORT: 6
        , API: 7
        , TRY: 8
        , RETURN: 9
        , BREAK: 10
        , CONTINUE: 11
        , PASS: 12
        , PROPERTY: 13
        
        , ELIF: 100
        , ELSE: 200
        , FOR_ELSE: 201
        , INIT: 300
        , DEL: 400
        , EXCEPT: 500
        , FINALLY: 600
        , CODE: 999
        , HOLDER: 1000
        , NULL: 10000
    }
    
    const BLOCK_DIRECTION  = {
        ROOT: -1
        , DOWN: 1
        , INDENT: 2
        , BOTTOM_DOWN: 3
    }
    
    const BLOCK_TYPE = {
        BLOCK: 1
        , SHADOW_BLOCK: 2
        , MOVE_BLOCK: 3
    }
    
    const MAKE_CHILD_BLOCK = {
        MOVE: 1
        , SHADOW: 2
    }

    const DEFAULT_VARIABLE_ARRAY_LIST = ['a', 'b', 'c', 'd', 'e', 'f', 'g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'
                                            , 'vp', '_num', 'var'];
    const IMPORT_LIBRARY_LIST = {
        0: { value: 'numpy', text: 'numpy' }
        , 1: { value: 'pandas', text: 'pandas' }
        , 2: { value: 'matplotlib', text: 'matplotlib' }
        , 3: { value: 'seaborn', text: 'seaborn'}
        , 4: { value: 'os', text: 'os'}
        , 5: { value: 'sys', text: 'sys'}
        , 6: { value: 'time', text: 'time'}
        , 7: { value: 'datetime', text: 'datetime'}
        , 8: { value: 'random', text: 'random'}
        , 9: { value: 'math', text: 'math'}
    }

    /** ---------------------------------------- const Number ------------------------------------------ */
    const NUM_INDENT_DEPTH_PX = 20;
    const NUM_BLOCK_HEIGHT_PX = 24;

    const NUM_MAX_ITERATION = 1000;

    const NUM_NULL = -1;
    const NUM_ZERO = 0;
    const NUM_HUNDREAD = 100;
    const NUM_THOUSAND = 1000;
    const NUM_DELETE_KEY_EVENT_NUMBER = 46;
    const NUM_DEFAULT_POS_X = 15;
    const NUM_DEFAULT_POS_Y = 0;
    const NUM_DEFAULT_BLOCK_LEFT_HOLDER_HEIGHT = 42;
    const NUM_BLOCK_BOTTOM_HOLDER_HEIGHT = 10;

    /** ---------------------------------------- const String ------------------------------------------ */
    const STR_NULL = '';
    const STR_ONE_SPACE = ' ';
    const STR_ONE_INDENT = '    ';
    const STR_DIV = 'div';
    const STR_BORDER = 'border';
    const STR_TOP = 'top';
    const STR_LEFT = 'left';
    const STR_PX = 'px';
    const STR_OPACITY = 'opacity';
    const STR_MARGIN_TOP = 'margin-top';
    const STR_MARGIN_LEFT = 'margin-left';
    const STR_DISPLAY = 'display';
    const STR_BACKGROUND_COLOR = 'background-color';
    const STR_WIDTH = 'width';
    const STR_HEIGHT = 'height';
    const STR_INHERIT = 'inherit';
    const STR_YES = 'yes';
    const STR_NO = 'no';
    const STR_DATA_NUM_ID = 'data-num-id';
    const STR_DATA_DEPTH_ID = 'data-depth-id';
    const STR_NONE = 'none';
    const STR_BLOCK = 'block';
    const STR_SELECTED = 'selected';
    const STR_COLON_SELECTED = ':selected';
    const STR_POSITION = 'position';
    const STR_STATIC = 'static';
    const STR_RELATIVE = 'relative';
    const STR_ABSOLUTE = 'absolute';
    const STR_COLOR = 'color';

    const STR_CLASS = 'class';
    const STR_DEF = 'def';
    const STR_IF = 'if';
    const STR_FOR = 'for';
    const STR_WHILE = 'while';
    const STR_IMPORT = 'import';
    const STR_API = 'api';
    const STR_TRY = 'try';
    const STR_RETURN = 'return';
    const STR_BREAK = 'break';
    const STR_CONTINUE = 'continue';
    const STR_PASS = 'pass';
    const STR_CODE = 'code';
    const STR_ELIF = 'elif';
    const STR_PROPERTY = 'property';

    const STR_IS_SELECTED = 'isSelected';


    const STR_ICON_ARROW_UP = `▲`;
    const STR_ICON_ARROW_DOWN = `▼`;

    const STR_DOT = '.';
    /** ---------------------------------------- const CSS class String ------------------------------------------ */
    // const VP_CLASS_PREFIX = "vp-";
    // const VP_CLASS_PREFIX_OLD = ".vp-";
    const STR_CSS_CLASS_VP_BLOCK_CONTAINER = `${VP_CLASS_PREFIX}block-container`;
    const STR_CSS_CLASS_VP_BLOCK_NULLBLOCK = `${VP_CLASS_PREFIX}block-nullblock`;

    const STR_CSS_CLASS_VP_NODEEDITOR_MINIMIZE = `${VP_CLASS_PREFIX}nodeeditor-minimize`;
    const STR_CSS_CLASS_VP_NODEEDITOR_ARROW_UP = `${VP_CLASS_PREFIX}nodeeditor-arrow-up`;
    const STR_CSS_CLASS_VP_NODEEDITOR_ARROW_DOWN = `${VP_CLASS_PREFIX}nodeeditor-arrow-down`;
    const STR_CSS_CLASS_VP_BLOCK_BOTTOM_HOLDER = `${VP_CLASS_PREFIX}block-bottom-holder`;
    const STR_CSS_CLASS_VP_NODEEDITOR_OPTION_INPUT_REQUIRED = `${VP_CLASS_PREFIX}nodeeditor-option-input-required`;

    const STR_CSS_CLASS_VP_BLOCK_SHADOWBLOCK = `${VP_CLASS_PREFIX_OLD}block-shadowblock`;
    const STR_CSS_CLASS_VP_BLOCK_OPTION_BTN = `${VP_CLASS_PREFIX_OLD}block-option-btn`;
    const STR_CSS_CLASS_VP_BLOCK_DELETE_BTN = `${VP_CLASS_PREFIX_OLD}block-delete-btn`;
    const STR_CSS_CLASS_VP_NODEEDITOR_LEFT = `${VP_CLASS_PREFIX_OLD}nodeeditor-left`;
    const STR_CSS_CLASS_VP_NODEEDITOR_BOTTOM_TAB_VIEW = `${VP_CLASS_PREFIX_OLD}nodeeditor-bottom-tab-view`;
    const STR_CSS_CLASS_VP_BLOCK_LEFT_HOLDER = `${VP_CLASS_PREFIX_OLD}block-left-holder`;

    const STR_CSS_CLASS_VP_BLOCK_DEPTH_INFO = `${VP_CLASS_PREFIX_OLD}block-depth-info`;
    const STR_CSS_CLASS_VP_NODEEDITOR_TAB_NAVIGATION_NODE_OPTION_TITLE_SAPN = `${VP_CLASS_PREFIX_OLD}nodeeditor-tab-navigation-node-option-title span`;
    const STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK = 'selected-shadowblock';

    /** ---------------------------------------- const Message String --------------------------------------------- */
    const STR_MSG_BLOCK_DELETED = 'Block deleted!';

    const STR_INPUT_YOUR_CODE = 'input your code';
    const STR_CHANGE_KEYUP_PASTE = 'change keyup paste';
    /** ---------------------------------------- const Image Url String ------------------------------------------- */
    const PNG_VP_APIBLOCK_OPTION_ICON = 'vp-apiblock-option-icon.png';
    const PNG_VP_APIBLOCK_DELETE_ICON = 'vp-apiblock-delete-icon.png';
    /** ---------------------------------------- const State Name String ------------------------------------------ */
    const STATE_classInParamList = 'classInParamList';
    const STATE_className = 'className';
    
    const STATE_defName = 'defName';
    const STATE_defInParamList = 'defInParamList';
    
    const STATE_ifCodeLine = 'ifCodeLine';
    const STATE_isIfElse = 'isIfElse';
    const STATE_isForElse = 'isForElse';
    const STATE_elifCodeLine = 'elifCodeLine';
    const STATE_elifList = 'elifList';
    
    const STATE_forCodeLine = 'forCodeLine';
    
    const STATE_whileCodeLine = 'whileCodeLine';
    
    const STATE_baseImportList = 'baseImportList';
    const STATE_customImportList = 'customImportList';
    const STATE_isBaseImportPage = 'isBaseImportPage';
    const STATE_exceptList = 'exceptList';
    const STATE_exceptCodeLine = 'exceptCodeLine';
    const STATE_isFinally = 'isFinally';
    
    const STATE_returnOutParamList = 'returnOutParamList';
    
    const STATE_customCodeLine = 'customCodeLine';
    const STATE_breakCodeLine = 'breakCodeLine';
    const STATE_continueCodeLine = 'continueCodeLine';
    const STATE_passCodeLine = 'passCodeLine';

    /** ---------------------------------------- const Color String ------------------------------------------ */
    const COLOR_BLUE = `#2240c5`;
    const COLOR_RED = `#cc1f1f`;
    const COLOR_GREEN = `#14c51d`;
    const COLOR_YELLOW = 'yellow';
    const COLOR_WHITE = 'white';
    const COLOR_GRAY_input_your_code = '#d4d4d4';
    return {
        BLOCK_CODELINE_BTN_TYPE
        , BLOCK_CODELINE_TYPE
        , BLOCK_DIRECTION
        , BLOCK_TYPE
        , MAKE_CHILD_BLOCK

        , NUM_INDENT_DEPTH_PX
        , NUM_BLOCK_HEIGHT_PX
        , NUM_MAX_ITERATION
        
        , NUM_NULL
        , NUM_ZERO
        , NUM_HUNDREAD
        , NUM_THOUSAND
        , NUM_DELETE_KEY_EVENT_NUMBER 
        , NUM_DEFAULT_POS_X
        , NUM_DEFAULT_POS_Y
        , NUM_DEFAULT_BLOCK_LEFT_HOLDER_HEIGHT
        , NUM_BLOCK_BOTTOM_HOLDER_HEIGHT

        , STR_NULL
        , STR_DOT
        , STR_ONE_SPACE
        , STR_ONE_INDENT

        , STR_TOP
        , STR_LEFT
        , STR_DIV
        , STR_BORDER
        , STR_PX
        , STR_OPACITY
        , STR_MARGIN_TOP
        , STR_MARGIN_LEFT
        , STR_DISPLAY
        , STR_BACKGROUND_COLOR
        , STR_WIDTH
        , STR_HEIGHT
        , STR_INHERIT
        , STR_YES
        , STR_DATA_NUM_ID 
        , STR_DATA_DEPTH_ID
        , STR_NONE
        , STR_BLOCK
        , STR_SELECTED
        , STR_COLON_SELECTED
        , STR_POSITION
        , STR_STATIC
        , STR_RELATIVE
        , STR_ABSOLUTE
        , STR_NO
        , STR_COLOR
        , STR_IS_SELECTED

        , STR_CLASS
        , STR_DEF
        , STR_IF
        , STR_FOR
        , STR_WHILE
        , STR_IMPORT
        , STR_API
        , STR_TRY
        , STR_RETURN
        , STR_BREAK
        , STR_CONTINUE
        , STR_PASS
        , STR_CODE
        , STR_ELIF
        , STR_PROPERTY

        , STR_CSS_CLASS_VP_BLOCK_CONTAINER
        , STR_CSS_CLASS_VP_BLOCK_NULLBLOCK
        , STR_CSS_CLASS_VP_BLOCK_SHADOWBLOCK
        , STR_CSS_CLASS_VP_BLOCK_OPTION_BTN
        , STR_CSS_CLASS_VP_BLOCK_DELETE_BTN
        , STR_CSS_CLASS_VP_BLOCK_DEPTH_INFO
        , STR_CSS_CLASS_VP_BLOCK_LEFT_HOLDER
        , STR_CSS_CLASS_VP_BLOCK_BOTTOM_HOLDER

        , STR_CSS_CLASS_VP_NODEEDITOR_OPTION_INPUT_REQUIRED
        , STR_CSS_CLASS_VP_NODEEDITOR_LEFT
        , STR_CSS_CLASS_VP_NODEEDITOR_BOTTOM_TAB_VIEW
        , STR_CSS_CLASS_VP_NODEEDITOR_MINIMIZE
        , STR_CSS_CLASS_VP_NODEEDITOR_ARROW_UP
        , STR_CSS_CLASS_VP_NODEEDITOR_ARROW_DOWN
        , STR_CSS_CLASS_VP_NODEEDITOR_TAB_NAVIGATION_NODE_OPTION_TITLE_SAPN
        , STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK

        , STR_CHANGE_KEYUP_PASTE
        , STR_INPUT_YOUR_CODE
        , STR_MSG_BLOCK_DELETED

        , STR_ICON_ARROW_UP
        , STR_ICON_ARROW_DOWN

        , STATE_classInParamList
        , STATE_className
        , STATE_defName
        , STATE_defInParamList
        , STATE_ifCodeLine
        , STATE_isIfElse
        , STATE_isForElse
        , STATE_elifCodeLine
        , STATE_elifList
        , STATE_forCodeLine
        , STATE_whileCodeLine
        , STATE_baseImportList
        , STATE_customImportList
        , STATE_isBaseImportPage

        , STATE_exceptList
        , STATE_exceptCodeLine
        , STATE_isFinally
        , STATE_returnOutParamList
        , STATE_customCodeLine
        , STATE_breakCodeLine
        , STATE_continueCodeLine
        , STATE_passCodeLine
        
        , COLOR_BLUE
        , COLOR_RED
        , COLOR_GREEN
        , COLOR_YELLOW
        , COLOR_WHITE
        , COLOR_GRAY_input_your_code
        
        , IMPORT_LIBRARY_LIST
        , DEFAULT_VARIABLE_ARRAY_LIST

        , PNG_VP_APIBLOCK_OPTION_ICON
        , PNG_VP_APIBLOCK_DELETE_ICON
    }
});
