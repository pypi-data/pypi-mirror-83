define ([
    // 기본 
    'require'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/vpCommon'
    // + 추가 python common 폴더 패키지 : 이진용 주임
    , 'nbextensions/visualpython/src/pythonCommon/api/pythonComStateApi'
], function (requirejs, vpConst, vpCommon,
             pythonComStateApi ) {
    "use strict";

    /**
     * 
     * @param { pythonComPageRenderer this } pythonComPageRendererThis 
     * @param { string } typeEnum 
     * @param { number } currLineNumber 
     */
    var renderCodeLineArrayPalleteButton = function(pythonComPageRendererThis, typeEnum, currLineNumber) {
        var pythonComPageRendererThis = pythonComPageRendererThis;
        
        var title = ``;
        switch(typeEnum){
            case "CLASS":{
                title = `Class`;
                break;
            }
            case "IF":{
                title = `If`;
                break;
            }
            case "FOR":{
                title = `For`;
                break;
            }
            case "WHILE":{
                title = `While`;
                break;
            }
            case "CUSTOM_CODE_LINE":{
                title = `Make Code Line`;
                break;
            }
            case "DEF":{
                title = `Def`;
                break;
            }
            case "RETURN":{
                title = `Return`;
                break;
            }
            case "BREAK":{
                title = `Break`;
                break;
            }
            case "CONTINUE":{
                title = `Continue`;
                break;
            }
            case "ELIF":{
                title = `Elif`;
                break;
            }
            case "ELSE":{
                title = `Else`;
                break;
            }
            case "PRINT_FUNC":{
                title = `Print()`;
                break;
            }
            case "RANGE_FUNC":{
                title = `Range()`;
                break;
            }
            case "ENUMERATE_FUNC":{
                title = `Enumerate()`;
                break;
            }
            case "COMMENT":{
                title = `Comment`;
                break;
            }
            case "SELF_VARIABLE": {
                title = `Self Variable`;
                break;
            }

            default: {
                break;
            }
        }
        var button = $(`<button class="vp-pythonCom-func-btn" value="${currLineNumber}"> 
                            <span class="vp-multilang" data-caption-id="${title}"> ${title} </span>
                        </button> `);
        return button;
    }

    return renderCodeLineArrayPalleteButton;
});