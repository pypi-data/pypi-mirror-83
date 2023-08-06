define ([
    // 기본 
    'require'
    , './tokenPalleteBlock/renderInputVarPaletteBlock'
    , './tokenPalleteBlock/renderConditionOperatorPalleteBlock'
    , './tokenPalleteBlock/renderCalculationOperatorPaletteBlock'

    , './codeLineArrayPalleteBlock/keywordList/renderBreakContinueElsePaletteBlock'
    , './codeLineArrayPalleteBlock/keywordList/renderForPaletteBlock'
    , './codeLineArrayPalleteBlock/keywordList/renderFunctionPaletteBlock'
    , './codeLineArrayPalleteBlock/keywordList/renderIfPaletteBlock'
    , './codeLineArrayPalleteBlock/keywordList/renderWhilePaletteBlock'
    , './codeLineArrayPalleteBlock/keywordList/renderReturnPaletteBlock'
    , './codeLineArrayPalleteBlock/keywordList/renderElifPaletteBlock'
    , './codeLineArrayPalleteBlock/keywordList/renderClassPaletteBlock'
    , './codeLineArrayPalleteBlock/keywordList/renderClassSelfVariablePaletteBlock'

    , './codeLineArrayPalleteBlock/functionList/renderEnumerateFuncPalleteBlock'
    , './codeLineArrayPalleteBlock/functionList/renderRangeFuncPalleteBlock'
    , './codeLineArrayPalleteBlock/functionList/renderPrintFuncPalleteBlock'

    , './codeLineArrayPalleteBlock/renderCodeLinePaletteBlock'
    , './codeLineArrayPalleteBlock/renderCommentPaletteBlock'

], function( requirejs, 
             renderInputVarPaletteBlock, renderConditionOperatorPalleteBlock, renderCalculationOperatorPaletteBlock,
             
             renderBreakContinueElsePaletteBlock, renderForPaletteBlock, renderFunctionPaletteBlock,
             renderIfPaletteBlock, renderWhilePaletteBlock,
             renderReturnPaletteBlock, renderElifPaletteBlock, renderClassPaletteBlock, renderClassSelfVariablePaletteBlock,
             
             renderEnumerateFuncPalleteBlock, renderRangeFuncPalleteBlock, renderPrintFuncPalleteBlock,
             
             renderCodeLinePaletteBlock,
             renderCommentPaletteBlock
              ) {
    "use strict";

    /**
     * PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP
     * javascript Map 객체 
     * key : string, value : renderPaletteBlock
     */
    const PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP = new Map();
    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`CLASS`, renderClassPaletteBlock);

    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`DEF`, renderFunctionPaletteBlock);
    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`DEF_INIT`, renderFunctionPaletteBlock);
    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`DEF_DEL`, renderFunctionPaletteBlock);

    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`FOR`, renderForPaletteBlock);
    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`IF`, renderIfPaletteBlock);
    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`WHILE`, renderWhilePaletteBlock);
    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`ELIF`, renderElifPaletteBlock);
    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`ELSE`, renderBreakContinueElsePaletteBlock);
    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`CUSTOM_CODE_LINE`, renderCodeLinePaletteBlock);
    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`BLANK_CODE_LINE`, renderCodeLinePaletteBlock);
    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`BREAK`, renderBreakContinueElsePaletteBlock);
    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`CONTINUE`, renderBreakContinueElsePaletteBlock);
    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`RETURN`, renderReturnPaletteBlock);
    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`PRINT_FUNC`, renderPrintFuncPalleteBlock);
    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`RANGE_FUNC`, renderRangeFuncPalleteBlock);
    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`ENUMERATE_FUNC`, renderEnumerateFuncPalleteBlock);
    PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`COMMENT`, renderCommentPaletteBlock);
    // PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP.set(`SELF_VARIABLE`, renderClassSelfVariablePaletteBlock);
    
    return {
        renderInputVarPaletteBlock, renderConditionOperatorPalleteBlock, renderCalculationOperatorPaletteBlock,

        renderBreakContinueElsePaletteBlock, renderForPaletteBlock, renderFunctionPaletteBlock,
        renderIfPaletteBlock, renderCodeLinePaletteBlock,renderWhilePaletteBlock,
        renderReturnPaletteBlock, renderElifPaletteBlock , renderClassPaletteBlock,

        renderEnumerateFuncPalleteBlock, renderRangeFuncPalleteBlock, renderPrintFuncPalleteBlock,

        renderCommentPaletteBlock,
        renderClassSelfVariablePaletteBlock,

        PYTHON_COMMON_RENDER_CODELINE_PALETTEBLOCK_MAP
    }
});