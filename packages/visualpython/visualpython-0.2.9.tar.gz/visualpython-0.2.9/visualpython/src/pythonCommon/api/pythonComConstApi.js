define ([
    'require'
    , 'nbextensions/visualpython/src/common/constant'

    , 'nbextensions/visualpython/src/common/constant_pythonCommon'
], function(requirejs, vpCommon
            , vpPythonConst ) {
    "use strict";

    var PYTHON_COMMON_PROP_MAP = vpPythonConst.PYTHON_COMMON_PROP_MAP;
    // var vpPythonConst
    // 안 쓰는 old api
    var mapFuncIdToPythonComFuncData = function( funcId ) {
        if (PYTHON_COMMON_PROP_MAP.has(funcId) === false) {
            // FIXME: PYTHON_COMMON_PROP_MAP 객체에 funcId가 없을 때 에러 처리
            alert("NUMPY_PROP_MAP not has funcId");
            return;
        }

        var pythonComCodeGenerator = PYTHON_COMMON_PROP_MAP.get(funcId).pythonComCodeGenerator;
        var pythonComCodeValidator = PYTHON_COMMON_PROP_MAP.get(funcId).pythonComCodeValidator;
        var pythonComPageRenderer = PYTHON_COMMON_PROP_MAP.get(funcId).pythonComPageRenderer;
        var htmlUrlPath = PYTHON_COMMON_PROP_MAP.get(funcId).htmlUrlPath;
        var state = PYTHON_COMMON_PROP_MAP.get(funcId).state;

        console.log("PYTHON_COMMON_PROP_MAP htmlUrlPath state", PYTHON_COMMON_PROP_MAP, htmlUrlPath, state);
        
        return {
            pythonComCodeGenerator
            , pythonComCodeValidator
            , pythonComPageRenderer
            , htmlUrlPath
            , state
        }
    }
    
    var mapFuncIdToHtmlUrlPath = function( funcId ) {
        if (PYTHON_COMMON_PROP_MAP.has(funcId) === false) {
            // FIXME: PYTHON_COMMON_PROP_MAP 객체에 funcId가 없을 때 에러 처리
            alert("NUMPY_PROP_MAP not has funcId");
            return;
        }

        var htmlUrlPath = PYTHON_COMMON_PROP_MAP.get(funcId).htmlUrlPath;
        return htmlUrlPath;
    }

    // 현재 사용할 api
    var newMapFuncIdToPythonComFuncData = function( funcId ) {
        if (PYTHON_COMMON_PROP_MAP.has(funcId) === false) {
            // FIXME: PYTHON_COMMON_PROP_MAP 객체에 funcId가 없을 때 에러 처리
            alert("PYTHON_COMMON_PROP_MAP not has funcId");
            return;
        }

        var pythonComCodeGenerator = new ( PYTHON_COMMON_PROP_MAP.get(funcId).pythonComCodeGenerator );
        var pythonComCodeValidator = new ( PYTHON_COMMON_PROP_MAP.get(funcId).pythonComCodeValidator );
        var pythonComPageRenderer = new ( PYTHON_COMMON_PROP_MAP.get(funcId).pythonComPageRenderer );
        var pythonComStateGenerator = new ( PYTHON_COMMON_PROP_MAP.get(funcId).pythonComStateGenerator );
   
        var htmlUrlPath = PYTHON_COMMON_PROP_MAP.get(funcId).htmlUrlPath;
        var bluePrintReadOnlyState = { ...PYTHON_COMMON_PROP_MAP.get(funcId).state };

        pythonComStateGenerator.makeState(bluePrintReadOnlyState);
        var state = pythonComStateGenerator.getStateAll();

        pythonComCodeGenerator.setStateGenerator(pythonComStateGenerator);
        pythonComPageRenderer.setStateGenerator(pythonComStateGenerator);

        var pythonComConstObj = {
            PYTHON_COMMON_GENERATE_CODE_MAKE_VARIABLE_ENUM: vpPythonConst.PYTHON_COMMON_GENERATE_CODE_MAKE_VARIABLE_ENUM
            , PYTHON_COMMON_GENERATE_CODE_LINE_ENUM: vpPythonConst.PYTHON_COMMON_GENERATE_CODE_LINE_ENUM
            , PYTHON_COMMON_PYTHON_DATA_TYPE_ENUM: vpPythonConst.PYTHON_COMMON_PYTHON_DATA_TYPE_ENUM
        }
        pythonComPageRenderer.setPythonComConstData(pythonComConstObj);
        pythonComPageRenderer.setNewMapFuncIdToPythonComFuncDataFunction(newMapFuncIdToPythonComFuncData);
        return {
            pythonComCodeGenerator
            , pythonComCodeValidator
            , pythonComPageRenderer
            , pythonComStateGenerator
            , htmlUrlPath
            , state
        }
    }

    var readJson = function(file, callback) {
        var rawFile = new XMLHttpRequest();
        rawFile.overrideMimeType("application/json");
        rawFile.open("GET", file, true);
        rawFile.onreadystatechange = function() {
            if (rawFile.readyState === 4 && rawFile.status == "200") {
                callback(rawFile.responseText);
            }
        }
        rawFile.send(null);
    }
    
    //usage:
    // readTextFile("./test.json", function(text){
    //     var data = JSON.parse(text);
    //     console.log(data);
    // });
    return {
        mapFuncIdToPythonComFuncData
        , mapFuncIdToHtmlUrlPath
        , newMapFuncIdToPythonComFuncData
        , readJson
    }
    
});