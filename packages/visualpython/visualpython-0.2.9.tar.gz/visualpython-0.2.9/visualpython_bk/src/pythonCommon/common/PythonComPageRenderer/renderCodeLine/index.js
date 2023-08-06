define ([
    // 기본 
    'require'
    // + 추가 python common 폴더 패키지 : 이진용 주임
    , './renderClassCodeLine'
    , './renderDefCodeLine'
    , './renderForCodeLine'
    , './renderIfCodeLine'
    , './renderWhileCodeLine'
    , './renderBlankCodeLine'
    , './renderMakeVariableCodeLine'
    , './renderBreakContinueElseCodeLine'
    , './renderElifCodeLine'
    , './renderReturnCodeLine'
    , './renderSelfVariableCodeLine'
    , './renderCommentCodeLine'

    , './renderCommonFunctionCodeLine'
], function( requirejs, 
             renderClassCodeLine, renderDefCodeLine, renderForCodeLine, renderIfCodeLine, renderWhileCodeLine,
             renderBlankCodeLine, renderMakeVariableCodeLine,
             renderBreakContinueElseCodeLine,
             renderElifCodeLine, renderReturnCodeLine, renderSelfVariableCodeLine, renderCommentCodeLine,
             
             renderCommonFunctionCodeLine ) {
    "use strict";
    const PYTHON_COMMON_RENDER_CODELINE_MAP = new Map();
    PYTHON_COMMON_RENDER_CODELINE_MAP.set("CLASS", renderClassCodeLine);
    PYTHON_COMMON_RENDER_CODELINE_MAP.set("DEF", renderDefCodeLine);
    PYTHON_COMMON_RENDER_CODELINE_MAP.set("DEF_INIT", renderDefCodeLine);
    PYTHON_COMMON_RENDER_CODELINE_MAP.set("DEF_DEL", renderDefCodeLine);
    PYTHON_COMMON_RENDER_CODELINE_MAP.set("FOR", renderForCodeLine);
    PYTHON_COMMON_RENDER_CODELINE_MAP.set("IF", renderIfCodeLine);
    PYTHON_COMMON_RENDER_CODELINE_MAP.set("WHILE", renderWhileCodeLine);
    PYTHON_COMMON_RENDER_CODELINE_MAP.set("RETURN", renderReturnCodeLine);
    PYTHON_COMMON_RENDER_CODELINE_MAP.set("BREAK", renderBreakContinueElseCodeLine);
    PYTHON_COMMON_RENDER_CODELINE_MAP.set("CONTINUE", renderBreakContinueElseCodeLine);
    PYTHON_COMMON_RENDER_CODELINE_MAP.set("ELSE", renderBreakContinueElseCodeLine);
    PYTHON_COMMON_RENDER_CODELINE_MAP.set("ELIF", renderElifCodeLine);
    PYTHON_COMMON_RENDER_CODELINE_MAP.set("CUSTOM_CODE_LINE", renderMakeVariableCodeLine);
    PYTHON_COMMON_RENDER_CODELINE_MAP.set("SELF_VARIABLE", renderSelfVariableCodeLine);
    PYTHON_COMMON_RENDER_CODELINE_MAP.set("COMMENT", renderCommentCodeLine);
    PYTHON_COMMON_RENDER_CODELINE_MAP.set("BLANK_CODE_LINE", renderBlankCodeLine);

    //COMMON_FUNCTION
    PYTHON_COMMON_RENDER_CODELINE_MAP.set("COMMON_FUNCTION", renderCommonFunctionCodeLine);
    return {
        PYTHON_COMMON_RENDER_CODELINE_MAP
    };
});