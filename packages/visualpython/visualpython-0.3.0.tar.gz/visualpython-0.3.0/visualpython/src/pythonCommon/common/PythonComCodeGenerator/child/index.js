define ([
    'require'
    , './PythonComMakeListCodeGenerator'
    , './PythonComMakeDictionaryCodeGenerator'
    , './PythonComMakeSetCodeGenerator'
    , './PythonComMakeTupleCodeGenerator'
    , './PythonComRangeCodeGenerator'
    , './PythonComEnumerateCodeGenerator'
    , './PythonComMakeCommentCodeGenerator'
    , './PythonComPrintCodeGenerator'
    , './PythonComCommentCodeGenerator'

    , './PythonComCodeLineArrayCodeGenerator'
    , './PythonComCodeLineCodeGenerator'
], function( requirejs
             , PythonComMakeListCodeGenerator
             , PythonComMakeDictionaryCodeGenerator
             , PythonComMakeSetCodeGenerator
             , PythonComMakeTupleCodeGenerator
             , PythonComRangeCodeGenerator
             , PythonComEnumerateCodeGenerator
             , PythonComMakeCommentCodeGenerator
             , PythonComPrintCodeGenerator
             , PythonComCommentCodeGenerator

             , PythonComCodeLineArrayCodeGenerator
             , PythonComCodeLineCodeGenerator ) {
    return {
        PythonComMakeListCodeGenerator
        , PythonComMakeDictionaryCodeGenerator
        , PythonComMakeSetCodeGenerator
        , PythonComMakeTupleCodeGenerator
        , PythonComRangeCodeGenerator
        , PythonComEnumerateCodeGenerator
        , PythonComMakeCommentCodeGenerator
        , PythonComPrintCodeGenerator
        , PythonComCommentCodeGenerator

        , PythonComCodeLineArrayCodeGenerator
        , PythonComCodeLineCodeGenerator
    }
});
