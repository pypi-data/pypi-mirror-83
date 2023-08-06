define([
    'require'
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComCodeGenerator/child/index'
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComCodeValidator/child/index'
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComPageRenderer/child/index'
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComStateGenerator/child/index'
    , 'nbextensions/visualpython/src/pythonCommon/common/PythonComStateGenerator/parent/PythonComStateGenerator'
], function( requirejs, 
             pythonComCodeGeneratorList, pythonComCodeValidatorList, pythonComPageRenderererList, pythonComStateGeneratorList,
             PythonComStateGenerator ) {
    "use strict";
    const { PythonComMakeListCodeGenerator,
            PythonComMakeDictionaryCodeGenerator, PythonComMakeSetCodeGenerator
            , PythonComMakeTupleCodeGenerator, PythonComRangeCodeGenerator, PythonComEnumerateCodeGenerator
            , PythonComPrintCodeGenerator, PythonComCommentCodeGenerator
            , PythonComCodeLineArrayCodeGenerator
            , PythonComCodeLineCodeGenerator } = pythonComCodeGeneratorList;
    const { PythonComMakeListCodeValidator,
            PythonComMakeDictionaryCodeValidator, PythonComMakeSetCodeValidator
            , PythonComMakeTupleCodeValidator, PythonComRangeCodeValidator, PythonComEnumerateCodeValidator
            , PythonComPrintCodeValidator, PythonComCommentCodeValidator
            , PythonComCodeLineArrayCodeValidator
            , PythonComCodeLineCodeValidator } = pythonComCodeValidatorList;
    const { PythonComMakeListPageRenderer,
            PythonComMakeDictionaryPageRenderer, PythonComMakeSetPageRenderer
            , PythonComMakeTuplePageRenderer, PythonComRangePageRenderer, PythonComEnumeratePageRenderer
            , PythonComPrintPageRenderer, PythonComCommentPageRenderer
            , PythonComCodeLineArrayPageRenderer
            , PythonComCodeLinePageRenderer } = pythonComPageRenderererList;
    const { PythonComMakeListStateGenerator
            , PythonComCodeLineArrayStateGenerator
            , PythonComCodeLineStateGenerator} = pythonComStateGeneratorList;
             


    const pythonCommonGenerateCodeMakeVariableEnum = {
        ASSIGN_OPERATOR_TYPE: Symbol()
        , LEFT_BRACKET_TYPE: Symbol()
        , RIGHT_BRACKET_TYPE: Symbol()
        , DATA_VARIABLE_TYPE: Symbol()
        , DATA_NUMBER_TYPE: Symbol()

        , DATA_STRING_TYPE: Symbol()
        , DATA_LIST_TYPE: Symbol()
        , DATA_DICTIONARY_TYPE: Symbol()
        , DATA_TUPLE_TYPE: Symbol()

        , DATA_SET_TYPE: Symbol()

        , NUMPY_FUNCTION_TYPE: Symbol()
        , NUMPY_INSTANCE_FUNCTION_TYPE: Symbol()
        , CONDITION_OPERATOR_TYPE: Symbol()
        , CALCULATION_OPERATOR_TYPE: Symbol()
    }

    const pythonCommonGenerateCodeLineEnum = {
        CLASS_TYPE: Symbol()
        , DEF_TYPE: Symbol()
        , FOR_TYPE: Symbol()
        , IF_TYPE: Symbol()
        , WHILE_TYPE: Symbol()
        , ELIF_TYPE: Symbol()
        , ELSE_TYPE: Symbol()
        , MAKE_VARIABLE_TYPE: Symbol()
        , BREAK_TYPE: Symbol()
        , CONTINUE_TYPE: Symbol()
        , RETURN_TYPE: Symbol()
        , PRINT_FUNC_TYPE: Symbol()
        , RANGE_FUNC_TYPE: Symbol()
        , ENUMERATE_FUNC_TYPE: Symbol()
        , COMMENT_TYPE: Symbol()
        , SELF_VARIABLE_TYPE: Symbol()
    }

    const pythonCommonInputVarPaletteButtonEnum = {
        VARIABLE_TYPE: Symbol()
        , NUMBER_TYPE: Symbol()
        , STRING_TYPE: Symbol()
        , LIST_TYPE: Symbol()
        , DICTIONARY_TYPE: Symbol()
        , TUPLE_TYPE: Symbol()
        , SET_TYPE: Symbol()
    }

    const pythonCommonFunctionBluePrintList = [
        {
            funcName: "python class"
            , funcId: "JY400"
            , htmlUrlPath: "pythonCommon/pageList/statementList/class/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineArrayCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineArrayCodeValidator
            , pythonComPageRenderer: PythonComCodeLineArrayPageRenderer 
            , pythonComStateGenerator: PythonComCodeLineArrayStateGenerator
            , state: {
                currLineNumber: 1
                , codeLineArray: [
                    { 
                        type: "CLASS"
                        , data: {
                            name: "yourClass"
                        }
                        , indentSpaceNum: 0
                    }
                ]
                , codeLineArrayStack: []
                , cacheBufferData:{
                    classParamList: [""]
                    , className: ""
                    , defParamList: [""]
                    , defName:""
                    , forIndexValueList: [""]
                    , forOperator: ""
                }
            }
        },
        {
            funcName: "python def"
            , funcId: "JY401"
            , htmlUrlPath: "pythonCommon/pageList/statementList/def/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineArrayCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineArrayCodeValidator
            , pythonComPageRenderer: PythonComCodeLineArrayPageRenderer 
            , pythonComStateGenerator: PythonComCodeLineArrayStateGenerator
            , state: {
                currLineNumber: 1
                , codeLineArray: [
                    { 
                        type: "DEF"
                        , data: {
                                name:"makeYourData" , paramList: ["a"]
                        }
                        , indentSpaceNum: 0
                    }
                ]
                , codeLineArrayStack: []
                , cacheBufferData:{
                    classParamList: [""]
                    , className: ""
                    , defParamList: [""]
                    , defName:""
                    , forIndexValueList: [""]
                    , forOperator: ""
                }
            }
        },
        {
            funcName: "python for"
            , funcId: "JY402"
            , htmlUrlPath: "pythonCommon/pageList/statementList/for/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineArrayCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineArrayCodeValidator
            , pythonComPageRenderer: PythonComCodeLineArrayPageRenderer 
            , pythonComStateGenerator: PythonComCodeLineArrayStateGenerator
            , state: {
                currLineNumber: 1
                , codeLineArray: [
                    {
                        type:"FOR"
                        , data: {
                            indexValueList: ["i"]
                            , operator: "in"
                            , iterableObjData: [ 
                                {type:"COMMON_FUNCTION", data:"range(100)"} 
                            ]
                        }
                        , indentSpaceNum: 0
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [ {type:"COMMON_FUNCTION", data:"print(i)"} ]
                        , indentSpaceNum: 4 
                    }
                ]
                , codeLineArrayStack: []
                , cacheBufferData:{
                    classParamList: [""]
                    , className: ""
                    , defParamList: [""]
                    , defName:""
                    , forIndexValueList: [""]
                    , forOperator: ""
                }
            }
        },
        {
            funcName: "python while"
            , funcId: "JY403"
            , htmlUrlPath: "pythonCommon/pageList/statementList/while/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineArrayCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineArrayCodeValidator
            , pythonComPageRenderer: PythonComCodeLineArrayPageRenderer 
            , pythonComStateGenerator: PythonComCodeLineArrayStateGenerator
            , state: {
                currLineNumber: 1
                , codeLineArray: [
                    {
                        type:"WHILE"
                        , data: [ {type:"VARIABLE", data:"left_var"},
                                  {type:"CONDITION_OPERATOR", data:"=="},
                                  {type:"VARIABLE", data:"right_var"} ]
                        , indentSpaceNum: 0
                    }
                ]
                , codeLineArrayStack: []
                , cacheBufferData:{
                    classParamList: [""]
                    , className: ""
                    , defParamList: [""]
                    , defName:""
                    , forIndexValueList: [""]
                    , forOperator: ""
                }
            }
        },
        {
            funcName: "python 변수 선언"
            , funcId: "JY404"
            , htmlUrlPath: "pythonCommon/pageList/makeDataList/makeVariable/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineCodeValidator
            , pythonComPageRenderer: PythonComCodeLinePageRenderer
            , pythonComStateGenerator: PythonComCodeLineStateGenerator
            , state: {
                paramList: [
                    {type: pythonCommonGenerateCodeMakeVariableEnum.DATA_VARIABLE_TYPE, data: "yourVariable"}
                    , {type: pythonCommonGenerateCodeMakeVariableEnum.ASSIGN_OPERATOR_TYPE, data: "="}
                ]
            }
        },
        {
            funcName: "python List"
            , funcId: "JY405"
            , htmlUrlPath: "pythonCommon/pageList/makeDataList/makeList/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComMakeListCodeGenerator
            , pythonComCodeValidator: PythonComMakeListCodeValidator
            , pythonComPageRenderer: PythonComMakeListPageRenderer
            , pythonComStateGenerator: PythonComMakeListStateGenerator
            , state: {
                paramList: [
                    "0"
                ]
                , returnVariable: ""
                , isReturnVariable: false
            }
        },
        {
            funcName: "python Dictionary"
            , funcId: "JY406"
            , htmlUrlPath: "pythonCommon/pageList/makeDataList/makeDictionary/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComMakeDictionaryCodeGenerator
            , pythonComCodeValidator: PythonComMakeDictionaryCodeValidator
            , pythonComPageRenderer: PythonComMakeDictionaryPageRenderer
            , pythonComStateGenerator: PythonComStateGenerator
            , state: {
                paramList: [
 
                ]
                , returnVariable: ""
                , isReturnVariable: false
            }
        },
        {
            funcName: "python Tuple"
            , funcId: "JY407"
            , htmlUrlPath: "pythonCommon/pageList/makeDataList/makeTuple/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComMakeTupleCodeGenerator
            , pythonComCodeValidator: PythonComMakeTupleCodeValidator
            , pythonComPageRenderer: PythonComMakeTuplePageRenderer
            , pythonComStateGenerator: PythonComStateGenerator
            , state: {
                paramList: [
 
                ]
                , returnVariable: ""
                , isReturnVariable: false
            }
        },
        {
            funcName: "python Set"
            , funcId: "JY408"
            , htmlUrlPath: "pythonCommon/pageList/makeDataList/makeSet/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComMakeSetCodeGenerator
            , pythonComCodeValidator: PythonComMakeSetCodeValidator
            , pythonComPageRenderer: PythonComMakeSetPageRenderer
            , pythonComStateGenerator: PythonComStateGenerator
            , state: {
                paramList: [
 
                ]
                , returnVariable: ""
                , isReturnVariable: false
            }
        },          
        {
            funcName: "python Comment"
            , funcId: "JY409"
            , htmlUrlPath: "pythonCommon/pageList/makeDataList/makeComment/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCommentCodeGenerator
            , pythonComCodeValidator: PythonComCommentCodeValidator
            , pythonComPageRenderer: PythonComCommentPageRenderer
            , pythonComStateGenerator: PythonComStateGenerator
            , state: {
                paramData: {
                    comment: ""
                }
            }
        },
        {
            funcName: "python range()"
            , funcId: "JY410"
            , htmlUrlPath: "pythonCommon/pageList/functionList/range/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComRangeCodeGenerator
            , pythonComCodeValidator: PythonComRangeCodeValidator
            , pythonComPageRenderer: PythonComRangePageRenderer
            , pythonComStateGenerator: PythonComStateGenerator
            , state: {
                paramOption: "1"
                , paramData: {
                    param1Start: "", 

                    param2Start: "", 
                    param2Stop: "", 

                    param3Start: "", 
                    param3Stop: "", 
                    param3Step: ""
                }
                , returnVariable: ""
                , isReturnVariable: false
            }
        },
        {
            funcName: "python enumerate()"
            , funcId: "JY411"
            , htmlUrlPath: "pythonCommon/pageList/functionList/enumerate/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComEnumerateCodeGenerator
            , pythonComCodeValidator: PythonComEnumerateCodeValidator
            , pythonComPageRenderer: PythonComEnumeratePageRenderer
            , pythonComStateGenerator: PythonComStateGenerator
            , state: {
                paramOption: "1"
                ,paramList: [
                    "0"
                ]
                , returnVariable: ""
                , isReturnVariable: false
            }
        },
        {
            funcName: "python print()"
            , funcId: "JY412"
            , htmlUrlPath: "pythonCommon/pageList/functionList/print/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComPrintCodeGenerator
            , pythonComCodeValidator: PythonComPrintCodeValidator
            , pythonComPageRenderer: PythonComPrintPageRenderer
            , pythonComStateGenerator: PythonComStateGenerator
            , state: {
                paramData: {
                    paramVariable: ""
                }
             
            }
        },
        {
            funcName: "python if"
            , funcId: "JY413"
            , htmlUrlPath: "pythonCommon/pageList/statementList/if/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineArrayCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineArrayCodeValidator
            , pythonComPageRenderer: PythonComCodeLineArrayPageRenderer 
            , pythonComStateGenerator: PythonComCodeLineArrayStateGenerator
            , state: {
                currLineNumber: 1
                , codeLineArray: [
                    {
                        type:"IF"
                        , data: [ {type:"VARIABLE", data:"left_var"},
                                  {type:"CONDITION_OPERATOR", data:"=="},
                                  {type:"VARIABLE", data:"right_var"} ]
                        , indentSpaceNum: 0
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [ {type:"VARIABLE", data:"left_var"},
                                  {type:"ASSIGN_OPERATOR", data:"="},
                                  {type:"NUMBER", data:"0"} ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"ELIF"
                        , data: [ {type:"VARIABLE", data:"left_var"},
                                  {type:"CONDITION_OPERATOR", data:"!="},
                                  {type:"VARIABLE", data:"right_var"} ]
                        , indentSpaceNum: 0
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [ {type:"VARIABLE", data:"right_var"},
                                  {type:"ASSIGN_OPERATOR", data:"="},
                                  {type:"NUMBER", data:"1"}, ]
                        , indentSpaceNum: 4
                    }
                ]
                , codeLineArrayStack: []
                , cacheBufferData:{
                    classParamList: [""]
                    , className: ""
                    , defParamList: [""]
                    , defName:""
                    , forIndexValueList: [""]
                    , forOperator: ""
                }
            }
        },

        {
            funcName: "template 구구단"
            , funcId: "JY500"
            , htmlUrlPath: "pythonCommon/pageList/templateList/gugudan/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineArrayCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineArrayCodeValidator
            , pythonComPageRenderer: PythonComCodeLineArrayPageRenderer 
            , pythonComStateGenerator: PythonComCodeLineArrayStateGenerator
            , state: {
                currLineNumber: 1
                , codeLineArray: [
                    {
                        type:"COMMENT"
                        , data: "2 ~ 9 까지 반복"
                        , indentSpaceNum: 0
                    },
                    {
                        type:"FOR"
                        , data: {
                            indexValueList: ["i"]
                            , operator: "in"
                            , iterableObjData: [ 
                                {type:"COMMON_FUNCTION", data:"range(2, 10)"} 
                            ]
                        }
                        , indentSpaceNum: 0
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [ 
                            {type:"COMMON_FUNCTION", data:"print(i)"} 
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"COMMENT"
                        , data: "1 ~ 9 까지 반복"
                        , indentSpaceNum: 4
                    },
                    {
                        type:"FOR"
                        , data: {
                            indexValueList: ["j"]
                            , operator: "in"
                            , iterableObjData: [ 
                                {type:"COMMON_FUNCTION", data:"range(1, 10)"} 
                            ]
                        }
                        , indentSpaceNum: 4
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [ 
                            {type:"COMMON_FUNCTION", data:"print((i, j, i * j))"} 
                        ]
                        , indentSpaceNum: 8
                    },
                ]
                , codeLineArrayStack: []
                , cacheBufferData:{
                    classParamList: [""]
                    , className: ""
                    , defParamList: [""]
                    , defName:""
                    , forIndexValueList: [""]
                    , forOperator: ""
                }
            }
        },

        {
            funcName: "template 망델브로집합"
            , funcId: "JY501"
            , htmlUrlPath: "pythonCommon/pageList/templateList/mandelbrot/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineArrayCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineArrayCodeValidator
            , pythonComPageRenderer: PythonComCodeLineArrayPageRenderer 
            , pythonComStateGenerator: PythonComCodeLineArrayStateGenerator
            , state: {
                currLineNumber: 1
                , codeLineArray: [
                    { 
                        type: "DEF"
                        , data: {
                            name:"mandelbrot" , paramList: ["h","w", "maxit=20"]
                        }
                        , indentSpaceNum: 0
                    },
                    {
                        type:"COMMENT"
                        , data: `Returns an image of the Mandelbrot fractal of size (h,w).`
                        , indentSpaceNum: 0
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [ 
                            {type:"VARIABLE", data:"y"},
                            {type:"COMMA", data:","},
                            {type:"VARIABLE", data:"x"}, 
                            {type:"ASSIGN_OPERATOR", data:"="},
                            {type:"NUMPY_FUNCTION", data:"np.ogrid[ -1.4:1.4:h*1j, -2:0.8:w*1j ]"}  
                        ]
                        , indentSpaceNum: 4
                    },
                    { 
                        type:"CUSTOM_CODE_LINE"
                        , data: [ 
                            {type:"VARIABLE", data:"c"},
                            {type:"ASSIGN_OPERATOR", data:"="},
                            {type:"VARIABLE", data:"x"}, 
                            {type:"CALCULATION_OPERATOR", data:"+"},
                            {type:"VARIABLE", data:"y"},
                            {type:"CALCULATION_OPERATOR", data:"*"},
                            {type:"VARIABLE", data:"1j"}   
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [ 
                            {type:"VARIABLE", data:"z"},
                            {type:"ASSIGN_OPERATOR", data:"="},
                            {type:"VARIABLE", data:"c"}
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [ 
                            {type:"VARIABLE", data:"divtime"},
                            {type:"ASSIGN_OPERATOR", data:"="},
                            {type:"VARIABLE", data:"maxit"},
                            {type:"CALCULATION_OPERATOR", data:"+"},
                            {type:"NUMPY_FUNCTION", data:"np.zeros(z.shape, dtype=int)"},
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"FOR"
                        , data: {
                            indexValueList: ["i"]
                            , operator: "in"
                            , iterableObjData: [ 
                                {type:"COMMON_FUNCTION", data:"range(maxit)"} 
                            ]
                        }
                        , indentSpaceNum: 4
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [ 
                            {type:"VARIABLE", data:"z"},
                            {type:"ASSIGN_OPERATOR", data:"="},
                            {type:"VARIABLE", data:"z"},
                            {type:"CALCULATION_OPERATOR", data:"**"},
                            {type:"NUMBER", data:"2"},
                            {type:"CALCULATION_OPERATOR", data:"+"},
                            {type:"VARIABLE", data:"c"},
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [ 
                            {type:"VARIABLE", data:"diverge"},
                            {type:"ASSIGN_OPERATOR", data:"="},
                            {type:"VARIABLE", data:"z"},
                            {type:"CALCULATION_OPERATOR", data:"*"},
                            {type:"NUMBER", data:"np.conj(z)"},
                            {type:"CONDITION_OPERATOR", data:">"},
                            {type:"NUMBER", data:"2"},
                            {type:"CALCULATION_OPERATOR", data:"**"},
                            {type:"NUMBER", data:"2"},
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [ 
                            {type:"VARIABLE", data:"div_now"},
                            {type:"ASSIGN_OPERATOR", data:"="},
                            {type:"VARIABLE", data:"diverge"},
                            {type:"CONDITION_OPERATOR", data:"&"},
                            {type:"LEFT_BRACKET", data:"("},
                            {type:"VARIABLE", data:"divtime"},
                            {type:"CONDITION_OPERATOR", data:"=="},
                            {type:"VARIABLE", data:"maxit"},
                            {type:"RIGHT_BRACKET", data:")"},
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [ 
                            {type:"VARIABLE", data:"divtime[div_now]"},
                            {type:"ASSIGN_OPERATOR", data:"="},
                            {type:"VARIABLE", data:"i"}
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [ 
                            {type:"VARIABLE", data:"z[diverge]"},
                            {type:"ASSIGN_OPERATOR", data:"="},
                            {type:"VARIABLE", data:"2"}
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type:"RETURN"
                        , data: [
                            {type:"VARIABLE", data:"divtime"}
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"BLANK_CODE_LINE"
                        , data:""
                        , indentSpaceNum: 0
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [ 
                            {type:"VARIABLE", data:"mandelbro_var"},
                            {type:"ASSIGN_OPERATOR", data:"="},
                            {type:"CALL_CUSTOM_FUNCTION", data:"mandelbrot(400,400)"}
                        ]
                        , indentSpaceNum: 0
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [ 
                            {type:"MATPLOTLIB_FUNCTION", data:"plt.imshow(mandelbro_var)"},
                        ]
                        , indentSpaceNum: 0
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [ 
                            {type:"MATPLOTLIB_FUNCTION", data:"plt.show()"},
                        ]
                        , indentSpaceNum: 0
                    }
                ]
                , codeLineArrayStack: []
                , cacheBufferData:{
                    classParamList: [""]
                    , className: ""
                    , defParamList: [""]
                    , defName:""
                    , forIndexValueList: [""]
                    , forOperator: ""
                }
            }
        },
        {
            funcName: "template class 1"
            , funcId: "JY502"
            , htmlUrlPath: "pythonCommon/pageList/templateList/class1/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineArrayCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineArrayCodeValidator
            , pythonComPageRenderer: PythonComCodeLineArrayPageRenderer 
            , pythonComStateGenerator: PythonComCodeLineArrayStateGenerator
            , state: {
                currLineNumber: 1
                , codeLineArray: [
                    {
                        type:"CLASS"
                        , data: {
                            name: "Car",
                            paramList: ["object"]
                        }
                        , indentSpaceNum: 0
                    },
                    {
                        type:"DEF_DEL"
                        , data: {
                            name: "__init__",
                            paramList: []
                        }
                        , indentSpaceNum: 4
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"SELF_VARIABLE", data: "self._speed" },
                            { type:"ASSIGN_OPERATOR", data:"="},
                            { type:"NUMBER", data:"0"}
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type:"BLANK_CODE_LINE"
                        , data:""
                        , indentSpaceNum: 0
                    },
                    {
                        type:"DEF"
                        , data: {
                            name: "speed",
                            paramList: ["self"]
                        }
                        , indentSpaceNum: 4
                    },
                    { 
                        type:"RETURN"
                        , data: [
                            { type:"SELF_VARIABLE", data: "self._speed" },
          
                        ]
                        , indentSpaceNum: 8
                    },
                ]
                , codeLineArrayStack: []
                , cacheBufferData:{
                    classParamList: [""]
                    , className: ""
                    , defParamList: [""]
                    , defName:""
                    , forIndexValueList: [""]
                    , forOperator: ""
                }
            }
        },
        {
            funcName: "template class 2"
            , funcId: "JY503"
            , htmlUrlPath: "pythonCommon/pageList/templateList/class2/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineArrayCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineArrayCodeValidator
            , pythonComPageRenderer: PythonComCodeLineArrayPageRenderer 
            , pythonComStateGenerator: PythonComCodeLineArrayStateGenerator
            , state: {
                currLineNumber: 1
                , codeLineArray: [
                    {
                        type:"CLASS"
                        , data: {
                            name: "Car",
                            paramList: ["object"]
                        }
                        , indentSpaceNum: 0
                    },
                    {
                        type:"DEF_DEL"
                        , data: {
                            name: "__init__",
                            paramList: []
                        }
                        , indentSpaceNum: 4
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"SELF_VARIABLE", data: "self._speed" },
                            { type:"ASSIGN_OPERATOR", data:"="},
                            { type:"NUMBER", data:"0"}
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type:"BLANK_CODE_LINE"
                        , data:""
                        , indentSpaceNum: 0
                    },
                    {
                        type:"DEF"
                        , data: {
                            name: "getSpeed",
                            paramList: ["self"]
                        }
                        , indentSpaceNum: 4
                    },
                    { 
                        type:"RETURN"
                        , data: [
                            { type:"SELF_VARIABLE", data: "self._speed" },
          
                        ]
                        , indentSpaceNum: 8
                    },
                ]
                , codeLineArrayStack: []
                , cacheBufferData:{
                    classParamList: [""]
                    , className: ""
                    , defParamList: [""]
                    , defName:""
                    , forIndexValueList: [""]
                    , forOperator: ""
                }
            }
        },
        {
            funcName: "template mean"
            , funcId: "JY520"
            , htmlUrlPath: "pythonCommon/pageList/templateList/timeseriesList/mean/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineArrayCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineArrayCodeValidator
            , pythonComPageRenderer: PythonComCodeLineArrayPageRenderer 
            , pythonComStateGenerator: PythonComCodeLineArrayStateGenerator
            , state: {
                currLineNumber: 1
                , codeLineArray: [
                    {
                        type:"DEF"
                        , data: {
                            name: "makeMean",
                            paramList: ["list"]
                        }
                        , indentSpaceNum: 0
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "sum" },
                            { type:"ASSIGN_OPERATOR", data:"="},
                            { type:"NUMBER", data:"0"}
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"FOR"
                        , data: {
                            indexValueList: ["i"]
                            , operator: "in"
                            , iterableObjData: [ 
                                {type:"VARIABLE", data:"list"} 
                            ]
                        }
                        , indentSpaceNum: 4
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "sum" },
                            { type:"ASSIGN_OPERATOR", data:"+="},
                            { type:"VARIABLE", data:"i"}
                        ]
                        , indentSpaceNum: 8
                    },
                    { 
                        type:"RETURN"
                        , data: [
                            { type:"SELF_VARIABLE", data: "sum" },
                            { type:"CALCULATION_OPERATOR", data: "/" },
                            { type:"COMMON_FUNCTION", data: "len(list)" },
                        ]
                        , indentSpaceNum: 4
                    },
                ]
                , codeLineArrayStack: []
                , cacheBufferData:{
                    classParamList: [""]
                    , className: ""
                    , defParamList: [""]
                    , defName:""
                    , forIndexValueList: [""]
                    , forOperator: ""
                }
            }
        },
        {
            funcName: "template variance"
            , funcId: "JY521"
            , htmlUrlPath: "pythonCommon/pageList/templateList/timeseriesList/variance/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineArrayCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineArrayCodeValidator
            , pythonComPageRenderer: PythonComCodeLineArrayPageRenderer 
            , pythonComStateGenerator: PythonComCodeLineArrayStateGenerator
            , state: {
                currLineNumber: 1
                , codeLineArray: [
                    {
                        type:"DEF"
                        , data: {
                            name: "makeVariance",
                            paramList: ["list"]
                        }
                        , indentSpaceNum: 0
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "mean" },
                            { type:"ASSIGN_OPERATOR", data:"="},
                            { type:"CALL_CUSTOM_FUNCTION", data:"makeMean(arr)"}
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "sum" },
                            { type:"ASSIGN_OPERATOR", data:"="},
                            { type:"NUMBER", data:"0"}
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"FOR"
                        , data: {
                            indexValueList: ["i"]
                            , operator: "in"
                            , iterableObjData: [ 
                                {type:"VARIABLE", data:"list"} 
                            ]
                        }
                        , indentSpaceNum: 4
                    },
                    { 
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "sum" },
                            { type:"CALCULATION_OPERATOR", data: "+=" },
                            { type:"LEFT_BRACKET", data: "(" },
                            { type:"VARIABLE", data: "i" },
                            { type:"CALCULATION_OPERATOR", data: "-" },
                            { type:"VARIABLE", data: "mean" },
                            { type:"RIGHT_BRACKET", data: ")" },
                            { type:"CALCULATION_OPERATOR", data: "*" },
                            { type:"LEFT_BRACKET", data: "(" },
                            { type:"VARIABLE", data: "i" },
                            { type:"CALCULATION_OPERATOR", data: "-" },
                            { type:"VARIABLE", data: "mean" },
                            { type:"RIGHT_BRACKET", data: ")" },
                        ]
                        , indentSpaceNum: 8
                    },
                    { 
                        type:"RETURN"
                        , data: [
                            { type:"SELF_VARIABLE", data: "sum" },
                            { type:"CALCULATION_OPERATOR", data: "/" },
                            { type:"COMMON_FUNCTION", data: "len(list)" },
                        ]
                        , indentSpaceNum: 4
                    },
                ]
                , codeLineArrayStack: []
                , cacheBufferData:{
                    classParamList: [""]
                    , className: ""
                    , defParamList: [""]
                    , defName:""
                    , forIndexValueList: [""]
                    , forOperator: ""
                }
            }
        },
        {
            funcName: "template covariance"
            , funcId: "JY522"
            , htmlUrlPath: "pythonCommon/pageList/templateList/timeseriesList/covariance/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineArrayCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineArrayCodeValidator
            , pythonComPageRenderer: PythonComCodeLineArrayPageRenderer 
            , pythonComStateGenerator: PythonComCodeLineArrayStateGenerator
            , state: {
                currLineNumber: 1
                , codeLineArray: [
                    {
                        type:"DEF"
                        , data: {
                            name: "makeCovariance",
                            paramList: ["listX", "listY"] 
                        }
                        , indentSpaceNum: 0
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "meanX" },
                            { type:"ASSIGN_OPERATOR", data:"="},
                            { type:"CALL_CUSTOM_FUNCTION", data:"makeMean(listX)"}
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "meanY" },
                            { type:"ASSIGN_OPERATOR", data:"="},
                            { type:"CALL_CUSTOM_FUNCTION", data:"makeMean(listY)"}
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "meanXY" },
                            { type:"ASSIGN_OPERATOR", data:"="},
                            { type:"NUMBER", data:"0"}
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"BLANK_CODE_LINE"
                        , data:""
                        , indentSpaceNum: 0
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "list_length" },
                            { type:"ASSIGN_OPERATOR", data:"="},
                            { type:"COMMON_FUNCTION", data:"len(listX)"}
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "sum" },
                            { type:"ASSIGN_OPERATOR", data:"="},
                            { type:"NUMBER", data:"0"}
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"WHILE"
                        , data: [
                            { type:"VARIABLE", data: "list_length" },
                            { type:"CONDITION_OPERATOR", data:"!="},
                            { type:"NUMBER", data:"0"}
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "list_length " },
                            { type:"CALCULATION_OPERATOR", data:"-="},
                            { type:"NUMBER", data:"1"}
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "sum" },
                            { type:"CALCULATION_OPERATOR", data:"+="},
                            { type:"VARIABLE", data:"listX[list_length]"},
                            { type:"CALCULATION_OPERATOR", data:"*"},
                            { type:"VARIABLE", data:"listY[list_length]"}
                        ]
                        , indentSpaceNum: 8
                    },
                    { 
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "meanXY" },
                            { type:"ASSIGN_OPERATOR", data:"="},
                            { type:"VARIABLE", data: "sum" },
                            { type:"CALCULATION_OPERATOR", data: "/" },
                            { type:"COMMON_FUNCTION", data: "len(listX)" },
                        ]
                        , indentSpaceNum: 4
                    },
                    { 
                        type:"RETURN"
                        , data: [
                            { type:"VARIABLE", data: "meanXY" },
                            { type:"CALCULATION_OPERATOR", data: "-" },           
                            { type:"LEFT_BRACKET", data: "(" },
                            { type:"VARIABLE", data: "meanX" },
                            { type:"CALCULATION_OPERATOR", data: "*" },
                            { type:"VARIABLE", data: "meanY" },
                            { type:"RIGHT_BRACKET", data: ")" },
                        ]
                        , indentSpaceNum: 4
                    }
                ]
                , codeLineArrayStack: []
                , cacheBufferData:{
                    classParamList: [""]
                    , className: ""
                    , defParamList: [""]
                    , defName:""
                    , forIndexValueList: [""]
                    , forOperator: ""
                }
            }
        },
        {
            funcName: "template correlation"
            , funcId: "JY523"
            , htmlUrlPath: "pythonCommon/pageList/templateList/timeseriesList/correlation/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineArrayCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineArrayCodeValidator
            , pythonComPageRenderer: PythonComCodeLineArrayPageRenderer 
            , pythonComStateGenerator: PythonComCodeLineArrayStateGenerator
            , state: {
                currLineNumber: 1
                , codeLineArray: [
                    {
                        type:"DEF"
                        , data: {
                            name: "makeCorrelation",
                            paramList: ["listX", "listY"] 
                        }
                        , indentSpaceNum: 0
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "varianceX" },
                            { type:"ASSIGN_OPERATOR", data:"="},
                            { type:"CALL_CUSTOM_FUNCTION", data:"makeVariance(listX)"}
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "varianceY" },
                            { type:"ASSIGN_OPERATOR", data:"="},
                            { type:"CALL_CUSTOM_FUNCTION", data:"makeVariance(listY)"}
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "stdVarX" },
                            { type:"ASSIGN_OPERATOR", data:"="},
                            { type:"CALL_CUSTOM_FUNCTION", data:"math.sqrt(varianceX)"}
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "stdVarY" },
                            { type:"ASSIGN_OPERATOR", data:"="},
                            { type:"CALL_CUSTOM_FUNCTION", data:"math.sqrt(varianceY)"}
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "covXY" },
                            { type:"ASSIGN_OPERATOR", data:"="},
                            { type:"CALL_CUSTOM_FUNCTION", data:"makeCovariance(listX,listY)"}
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"BLANK_CODE_LINE"
                        , data:""
                        , indentSpaceNum: 0
                    },
                    {
                        type:"IF"
                        , data: [
                            { type:"VARIABLE", data: "covXY" },
                            { type:"CONDITION_OPERATOR", data:"=="},
                            { type:"NUMBER", data:"0"},
                            { type:"ASSIGN_OPERATOR", data:"or"},
                            { type:"VARIABLE", data: "stdVarX" },
                            { type:"CONDITION_OPERATOR", data:"=="},
                            { type:"NUMBER", data:"0"},
                            { type:"ASSIGN_OPERATOR", data:"or"},
                            { type:"VARIABLE", data: "stdVarY" },
                            { type:"CONDITION_OPERATOR", data:"=="},
                            { type:"NUMBER", data:"0"},
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"RETURN"
                        , data: [
                            { type:"NUMBER", data: "0" }
                        ]
                        , indentSpaceNum: 8
                    },
                    { 
                        type:"RETURN"
                        , data: [
                            { type:"VARIABLE", data: "covXY" },
                            { type:"CALCULATION_OPERATOR", data: "/" },           
                            { type:"LEFT_BRACKET", data: "(" },
                            { type:"VARIABLE", data: "stdVarX" },
                            { type:"CALCULATION_OPERATOR", data: "*" },
                            { type:"VARIABLE", data: "stdVarY" },
                            { type:"RIGHT_BRACKET", data: ")" },
                        ]
                        , indentSpaceNum: 4
                    },
                ]
                , codeLineArrayStack: []
                , cacheBufferData:{
                    classParamList: [""]
                    , className: ""
                    , defParamList: [""]
                    , defName:""
                    , forIndexValueList: [""]
                    , forOperator: ""
                }
            }
        },
        {
            funcName: "template autoCovariance"
            , funcId: "JY524"
            , htmlUrlPath: "pythonCommon/pageList/templateList/timeseriesList/autoCovariance/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineArrayCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineArrayCodeValidator
            , pythonComPageRenderer: PythonComCodeLineArrayPageRenderer 
            , pythonComStateGenerator: PythonComCodeLineArrayStateGenerator
            , state: {
                currLineNumber: 1
                , codeLineArray: [
                    {
                        type:"DEF"
                        , data: { 
                            name: "makeAutoCovariance", 
                            paramList: ["list", "lagNum"] 
                        }
                        , indentSpaceNum: 0
                    },
                    {
                        type: 'IF'
                        , data: [
                            { type: "COMMON_FUNCTION",  data: "len(list)" }
                            , { type:"CONDITION_OPERATOR", data:"==" }
                            , { type:"VARIABLE", data:"lagNum" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: "RETURN"
                        , data: [
                            { type: "NUMBER", data:"0" }
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type: "BLANK_CODE_LINE"
                        , data: ""
                        , indentSpaceNum: 8
                    },
                    {
                        type: 'CUSTOM_CODE_LINE'
                        , data: [
                            { type: "VARIABLE",  data: "mean" }
                            , { type: "ASSIGN_OPERATOR", data: "=" }
                            , { type: "CUSTOM_FUNCTION", data: "makeMean(list)" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: 'CUSTOM_CODE_LINE'
                        , data: [
                            { type: "VARIABLE",  data: "list_length" }
                            , { type: "ASSIGN_OPERATOR", data: "=" }
                            , { type: "CUSTOM_FUNCTION", data: "len(list)" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: 'CUSTOM_CODE_LINE'
                        , data: [
                            { type: "VARIABLE",  data: "times" }
                            , { type: "ASSIGN_OPERATOR", data: "=" }
                            , { type: "CUSTOM_FUNCTION", data: "0" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: 'CUSTOM_CODE_LINE'
                        , data: [
                            { type: "VARIABLE",  data: "autoCov" }
                            , { type: "ASSIGN_OPERATOR", data: "=" }
                            , { type: "CUSTOM_FUNCTION", data: "0" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"FOR"
                        , data: {
                            indexValueList: ["i"]
                            , operator: "in"
                            , iterableObjData: [ 
                                {type:"COMMON_FUNCTION", data:"range(0, list_length - lagNum)"} 
                            ]
                        }
                        , indentSpaceNum: 4
                    },
 
                    {
                        type: 'CUSTOM_CODE_LINE'
                        , data: [
                            { type: "VARIABLE",  data: "autoCov" }
                            , { type: "CALCULATION_OPERATOR", data: "+=" }
                            , { type: "LEFT_BRACKET", data: "(" }
                            , { type: "VARIABLE", data: "list[i + lagNum]" }
                            , { type: "CALCULATION_OPERATOR", data: "-" }
                            , { type: "VARIABLE", data: "mean" }
                            , { type: "RIGHT_BRACKET", data: ")" }
                            , { type: "CALCULATION_OPERATOR", data: "*" }
                            , { type: "LEFT_BRACKET", data: "(" }
                            , { type: "VARIABLE", data: "list[i]" }
                            , { type: "CALCULATION_OPERATOR", data: "-" }
                            , { type: "VARIABLE", data: "mean" }
                            , { type: "RIGHT_BRACKET", data: ")" }
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type: 'CUSTOM_CODE_LINE'
                        , data: [
                            { type: "VARIABLE",  data: "times" }
                            , { type: "CALCULATION_OPERATOR", data: "+=" }
                            , { type: "NUMBER", data: "1" }
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type: "BLANK_CODE_LINE"
                        , data: ""
                        , indentSpaceNum: 8
                    },
                    { 
                        type:"RETURN"
                        , data: [
                            { type:"VARIABLE", data: "autoCov" },
                            { type:"CALCULATION_OPERATOR", data: "/" },           
                            { type:"LEFT_BRACKET", data: "times" },
                        ]
                        , indentSpaceNum: 4
                    },
                ]
                , codeLineArrayStack: []
                , cacheBufferData:{
                    classParamList: [""]
                    , className: ""
                    , defParamList: [""]
                    , defName:""
                    , forIndexValueList: [""]
                    , forOperator: ""
                }
            }
        },
        {
            funcName: "template autoCorrelation"
            , funcId: "JY525"
            , htmlUrlPath: "pythonCommon/pageList/templateList/timeseriesList/autoCorrelation/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineArrayCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineArrayCodeValidator
            , pythonComPageRenderer: PythonComCodeLineArrayPageRenderer 
            , pythonComStateGenerator: PythonComCodeLineArrayStateGenerator
            , state: {
                currLineNumber: 1
                , codeLineArray: [
                    {
                        type:"DEF"
                        , data: { 
                            name: "makeAutoCorrelation", 
                            paramList: ["list", "lagNum"] 
                        }
                        , indentSpaceNum: 0
                    },
                    {
                        type: 'CUSTOM_CODE_LINE'
                        , data: [
                            { type: "VARIABLE",  data: "rh" }
                            , { type: "ASSIGN_OPERATOR", data: "=" }
                            , { type: "CUSTOM_FUNCTION", data: "autoCovariance(list, lagNum)" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: 'CUSTOM_CODE_LINE'
                        , data: [
                            { type: "VARIABLE",  data: "r0" }
                            , { type: "ASSIGN_OPERATOR", data: "=" }
                            , { type: "CUSTOM_FUNCTION", data: "autoCovariance(list, 0)" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: "BLANK_CODE_LINE"
                        , data: ""
                        , indentSpaceNum: 4
                    },
                    {
                        type:"IF"
                        , data: [
                            { type:"VARIABLE", data: "rh" },
                            { type:"CONDITION_OPERATOR", data:"=="},
                            { type:"NUMBER", data:"0"},
                            { type:"ASSIGN_OPERATOR", data:"or"},
                            { type:"VARIABLE", data: "r0" },
                            { type:"CONDITION_OPERATOR", data:"=="},
                            { type:"NUMBER", data:"0"},
                        ]
                        , indentSpaceNum: 4
                    },
                    { 
                        type:"RETURN"
                        , data: [
                            { type:"NUMBER", data: "0" }
                        ]
                        , indentSpaceNum: 8
                    },
                    { 
                        type:"RETURN"
                        , data: [
                            { type:"VARIABLE", data: "rh" },
                            { type:"CALCULATION_OPERATOR", data:"/"},
                            { type:"VARIABLE", data:"r0"},
                        ]
                        , indentSpaceNum: 4
                    }
                ]
                , codeLineArrayStack: []
                , cacheBufferData:{
                    classParamList: [""]
                    , className: ""
                    , defParamList: [""]
                    , defName:""
                    , forIndexValueList: [""]
                    , forOperator: ""
                }
            }
        },
        {
            funcName: "template AR2"
            , funcId: "JY526"
            , htmlUrlPath: "pythonCommon/pageList/templateList/timeseriesList/ar2/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineArrayCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineArrayCodeValidator
            , pythonComPageRenderer: PythonComCodeLineArrayPageRenderer 
            , pythonComStateGenerator: PythonComCodeLineArrayStateGenerator
            , state: {
                currLineNumber: 1
                , codeLineArray: [
                    {
                        type:"DEF"
                        , data: { 
                            name: "generateAR2", 
                            paramList: [] 
                        }
                        , indentSpaceNum: 0
                    },
                    {
                        type: 'CUSTOM_CODE_LINE'
                        , data: [
                            { type: "VARIABLE",  data: "x_t_minus_2" }
                            , { type: "ASSIGN_OPERATOR", data: "=" }
                            , { type: "NUMBER", data: "2" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: 'CUSTOM_CODE_LINE'
                        , data: [
                            { type: "VARIABLE",  data: "x_t_minus_1" }
                            , { type: "ASSIGN_OPERATOR", data: "=" }
                            , { type: "NUMBER", data: "3" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: 'CUSTOM_CODE_LINE'
                        , data: [
                            { type: "VARIABLE",  data: "x_t" }
                            , { type: "ASSIGN_OPERATOR", data: "=" }
                            , { type: "NUMBER", data: "0" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: 'CUSTOM_CODE_LINE'
                        , data: [
                            { type: "VARIABLE",  data: "a_t" }
                            , { type: "ASSIGN_OPERATOR", data: "=" }
                            , { type: "NUMBER", data: "0" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: 'CUSTOM_CODE_LINE'
                        , data: [
                            { type: "VARIABLE",  data: "AR2_list" }
                            , { type: "ASSIGN_OPERATOR", data: "=" }
                            , { type: "LIST", data: "[x_t_minus_2, x_t_minus_1]" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"FOR"
                        , data: {
                            indexValueList: ["i"]
                            , operator: "in"
                            , iterableObjData: [ 
                                {type:"COMMON_FUNCTION", data:"range(2, 1440)"} 
                            ]
                        }
                        , indentSpaceNum: 4
                    },
                    {
                        type: 'CUSTOM_CODE_LINE'
                        , data: [
                            { type: "VARIABLE",  data: "a_t" }
                            , { type: "ASSIGN_OPERATOR", data: "=" }
                            , { type: "NUMPY_FUNCTION", data: "np.random.randn()" }
                            , { type: "COMMENT", data: "# -1 to 1 난수 생성" }
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type: 'CUSTOM_CODE_LINE'
                        , data: [
                            { type: "VARIABLE",  data: "x_t" }
                            , { type: "ASSIGN_OPERATOR", data: "=" }
                            , { type: "LEFT_BRACKET", data: "(" }
                            , { type: "NUMBER", data: "1.5" }
                            , { type: "CALCULATION_OPERATOR", data: "*" }
                            , { type: "VARIABLE", data: "x_t_minus_1" }
                            , { type: "RIGHT_BRACKET", data: ")" }
                            , { type: "CALCULATION_OPERATOR", data: "-" }
                            , { type: "LEFT_BRACKET", data: "(" }
                            , { type: "NUMBER", data: "0.75" }
                            , { type: "CALCULATION_OPERATOR", data: "*" }
                            , { type: "VARIABLE", data: "x_t_minus_2" }
                            , { type: "RIGHT_BRACKET", data: ")" }
                            , { type: "CALCULATION_OPERATOR", data: "+" }
                            , { type: "VARIABLE", data: "a_t" }
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type: 'CUSTOM_CODE_LINE'
                        , data: [
                            { type: "VARIABLE",  data: "x_t_minus_2" }
                            , { type: "ASSIGN_OPERATOR", data: "=" }
                            , { type: "VARIABLE", data: "x_t_minus_1" }
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type: 'CUSTOM_CODE_LINE'
                        , data: [
                            { type: "COMMON_FUNCTION",  data: "AR2_list.append(x_t)" }
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type:"RETURN"
                        , data: [
                            { type:"VARIABLE", data: "AR2_list" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: "BLANK_CODE_LINE"
                        , data: ""
                        , indentSpaceNum: 4
                    },
                    {
                        type: "CUSTOM_CODE_LINE"
                        , data: [
                            { type: "VARIABLE",  data: "AR2" }
                            , { type: "ASSIGN_OPERATOR", data: "=" }
                            , { type: "COSTOM_FUNCTION", data: "generateAR2()" }
                        ]
                        , indentSpaceNum: 0
                    },
                    {
                        type: "CUSTOM_CODE_LINE"
                        , data: [
                            { type: "MATPLOTLIB_FUNCTION",  data: "plt.plot(AR2)" }
                        ]
                        , indentSpaceNum: 0
                    },
                    {
                        type: "CUSTOM_CODE_LINE"
                        , data: [
                            { type: "MATPLOTLIB_FUNCTION",  data: "plt.show()" }
                        ]
                        , indentSpaceNum: 0
                    }
                ]
                , codeLineArrayStack: []
                , cacheBufferData: {
                    classParamList: [""]
                    , className: ""
                    , defParamList: [""]
                    , defName:""
                    , forIndexValueList: [""]
                    , forOperator: ""
                }
            }
        },
        {
            funcName: "template MA2"
            , funcId: "JY527"
            , htmlUrlPath: "pythonCommon/pageList/templateList/timeseriesList/ma2/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCodeLineArrayCodeGenerator
            , pythonComCodeValidator: PythonComCodeLineArrayCodeValidator
            , pythonComPageRenderer: PythonComCodeLineArrayPageRenderer 
            , pythonComStateGenerator: PythonComCodeLineArrayStateGenerator
            , state: {
                currLineNumber: 1
                , codeLineArray: [
                    {
                        type:"DEF"
                        , data: { 
                            name: "generateMA2", 
                            paramList: [] 
                        }
                        , indentSpaceNum: 0
                    },
                    {
                        type: "CUSTOM_CODE_LINE"
                        , data: [
                            { type: "VARIABLE",  data: "x0" }
                            , { type: "ASSIGN_OPERATOR",  data: "=" }
                            , { type: "NUMBER",  data: "2" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: "CUSTOM_CODE_LINE"
                        , data: [
                            { type: "VARIABLE",  data: "x1" }
                            , { type: "ASSIGN_OPERATOR",  data: "=" }
                            , { type: "NUMBER",  data: "3" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: "CUSTOM_CODE_LINE"
                        , data: [
                            { type: "VARIABLE",  data: "xt" }
                            , { type: "ASSIGN_OPERATOR",  data: "=" }
                            , { type: "NUMBER",  data: "0" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: "BLANK_CODE_LINE"
                        , data: ""
                        , indentSpaceNum: 4
                    },
                    {
                        type: "CUSTOM_CODE_LINE"
                        , data: [
                            { type: "VARIABLE",  data: "a_t" }
                            , { type: "ASSIGN_OPERATOR",  data: "=" }
                            , { type: "NUMBER",  data: "np.random.randn()" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: "CUSTOM_CODE_LINE"
                        , data: [
                            { type: "VARIABLE",  data: "a_t_minus_1" }
                            , { type: "ASSIGN_OPERATOR",  data: "=" }
                            , { type: "NUMBER",  data: "np.random.randn()" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: "CUSTOM_CODE_LINE"
                        , data: [
                            { type: "VARIABLE",  data: "a_t_minus_2" }
                            , { type: "ASSIGN_OPERATOR",  data: "=" }
                            , { type: "NUMPY_FUNCTION",  data: "np.random.randn()" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: "BLANK_CODE_LINE"
                        , data: ""
                        , indentSpaceNum: 4
                    },
                    {
                        type: "CUSTOM_CODE_LINE"
                        , data: [
                            { type: "VARIABLE",  data: "MA2" }
                            , { type: "ASSIGN_OPERATOR",  data: "=" }
                            , { type: "LIST",  data: "[x0, x1]" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type:"FOR"
                        , data: {
                            indexValueList: ["i"]
                            , operator: "in"
                            , iterableObjData: [ 
                                {type:"COMMON_FUNCTION", data:"range(2, 1440)"} 
                            ]
                        }
                        , indentSpaceNum: 4
                    },
                    {
                        type: "CUSTOM_CODE_LINE"
                        , data: [
                            { type: "VARIABLE",  data: "x_t" }
                            , { type: "ASSIGN_OPERATOR", data: "=" }
                            , { type: "VARIABLE",  data: "a_t" }
                            , { type: "ASSIGN_OPERATOR", data: "+" }
                            , { type: "LEFT_BRACKET", data: "(" }
                            , { type: "NUMBER", data: "0.7" }
                            , { type: "CALCULATION_OPERATOR", data: "*" }
                            , { type: "VARIABLE", data: "a_t_minus_1" }
                            , { type: "RIGHT_BRACKET", data: ")" }
                            , { type: "CALCULATION_OPERATOR", data: "+" }
                            , { type: "LEFT_BRACKET", data: "(" }
                            , { type: "NUMBER", data: "0.8" }
                            , { type: "CALCULATION_OPERATOR", data: "*" }
                            , { type: "VARIABLE", data: "a_t_minus_2" }
                            , { type: "RIGHT_BRACKET", data: ")" }
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type: "CUSTOM_CODE_LINE"
                        , data: [
                            { type: "VARIABLE",  data: "a_t_minus_2" }
                            , { type: "ASSIGN_OPERATOR",  data: "=" }
                            , { type: "VARIABLE",  data: "a_t_minus_1" }
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type: "CUSTOM_CODE_LINE"
                        , data: [
                            { type: "VARIABLE",  data: "a_t_minus_1" }
                            , { type: "ASSIGN_OPERATOR",  data: "=" }
                            , { type: "VARIABLE",  data: "a_t" }
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type: "CUSTOM_CODE_LINE"
                        , data: [
                            { type: "VARIABLE",  data: "a_t" }
                            , { type: "ASSIGN_OPERATOR",  data: "=" }
                            , { type: "NUMPY_FUNCTION",  data: "np.random.randn()" }
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type: "CUSTOM_CODE_LINE"
                        , data: [
                            { type: "COMMON_FUNCTION",  data: "MA2.append(x_t)" }
                        ]
                        , indentSpaceNum: 8
                    },
                    {
                        type:"RETURN"
                        , data: [
                            { type:"VARIABLE", data: "MA2" }
                        ]
                        , indentSpaceNum: 4
                    },
                    {
                        type: "BLANK_CODE_LINE"
                        , data: ""
                        , indentSpaceNum: 4
                    },
                    {
                        type: "CUSTOM_CODE_LINE"
                        , data: [
                            { type:"VARIABLE", data: "MA2" }
                            , { type: "ASSIGN_OPERATOR",  data: "=" }
                            , { type: "COMMON_FUNCTION",  data: "generateMA2()" }
                        ]
                        , indentSpaceNum: 0
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"MATPLOTLIB_FUNCTION", data: "plt.plot(MA2)" }
                        ]
                        , indentSpaceNum: 0
                    },
                    {
                        type:"CUSTOM_CODE_LINE"
                        , data: [
                            { type:"MATPLOTLIB_FUNCTION", data: "plt.show()" }
                        ]
                        , indentSpaceNum: 0
                    }
                ]
                , codeLineArrayStack: []
                , cacheBufferData: {
                    classParamList: [""]
                    , className: ""
                    , defParamList: [""]
                    , defName:""
                    , forIndexValueList: [""]
                    , forOperator: ""
                }
            }
        },
        {
            funcName: "Node Editor"
            , funcId: "JY599"
            , htmlUrlPath: "pythonCommon/pageList/nodeEditor/index.html"
            , stepCount: 1
            , pythonComCodeGenerator: PythonComCommentCodeGenerator
            , pythonComCodeValidator: PythonComCommentCodeValidator
            , pythonComPageRenderer: PythonComCommentPageRenderer
            , pythonComStateGenerator: PythonComStateGenerator
            , state: {

            }
        }
    ];

    const pythonComPropMap = new Map();
    pythonCommonFunctionBluePrintList.forEach( function(element) {
        pythonComPropMap.set(element.funcId, {
            pythonComCodeGenerator: element.pythonComCodeGenerator
            , pythonComCodeValidator: element.pythonComCodeValidator
            , pythonComPageRenderer: element.pythonComPageRenderer
            , pythonComStateGenerator: element.pythonComStateGenerator
            , htmlUrlPath: element.htmlUrlPath
            , state: element.state
        });
    });


    const pythonBaseCssPath = "python/index.css";
        
    return {
        PYTHON_COMMON_FUNCTIONS_BLUEPRINT: pythonCommonFunctionBluePrintList
        , PYTHON_COMMON_PROP_MAP: pythonComPropMap
        , PYTHON_COMMON_BASE_CSS_PATH: pythonBaseCssPath
        , PYTHON_COMMON_GENERATE_CODE_MAKE_VARIABLE_ENUM: pythonCommonGenerateCodeMakeVariableEnum
        , PYTHON_COMMON_GENERATE_CODE_LINE_ENUM: pythonCommonGenerateCodeLineEnum
        , PYTHON_COMMON_PYTHON_DATA_TYPE_ENUM: pythonCommonInputVarPaletteButtonEnum
        , PYTHON_BASE_CSS_PATH: pythonBaseCssPath
    }
});
