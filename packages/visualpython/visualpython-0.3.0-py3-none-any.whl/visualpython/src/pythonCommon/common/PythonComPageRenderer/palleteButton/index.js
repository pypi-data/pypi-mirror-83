define ([
    // 기본 
    'require'
    // + 추가 python common 폴더 패키지 : 이진용 주임
    , './codeLineOnePalleteButton/renderAssignOperatorPaletteButton'
    , './codeLineOnePalleteButton/renderLeftBracketPaletteButton'
    , './codeLineOnePalleteButton/renderRightBracketPaletteButton'
    , './codeLineOnePalleteButton/renderConditionOperatorPalleteButton'
    , './codeLineOnePalleteButton/renderCalculationOperatorPaletteButton'
    , './codeLineOnePalleteButton/renderInputVarPaletteButton'
    , './codeLineOnePalleteButton/renderNumpyPaletteButton'

    , './codeLineArrayPalleteButton/renderCodeLineArrayPalleteButton'
], function( requirejs, 
             renderAssignOperatorPaletteButton, renderLeftBracketPaletteButton, renderRightBracketPaletteButton, renderConditionOperatorPalleteButton,
             renderCalculationOperatorPaletteButton, renderInputVarPaletteButton,
             renderNumpyPaletteButton,
             
             renderCodeLineArrayPalleteButton ) {
    "use strict";
    return {
        renderAssignOperatorPaletteButton, renderLeftBracketPaletteButton, renderRightBracketPaletteButton, renderConditionOperatorPalleteButton,
        renderCalculationOperatorPaletteButton, renderInputVarPaletteButton,
        renderNumpyPaletteButton,

        renderCodeLineArrayPalleteButton
    }
});