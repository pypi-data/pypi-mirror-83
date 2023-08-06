define ([
    'require'
    , './PythonComMakeListStateGenerator'

    , './PythonComCodeLineArrayStateGenerator'
    , './PythonComCodeLineStateGenerator'
], function( requirejs
             , PythonComMakeListStateGenerator
             
             , PythonComCodeLineArrayStateGenerator
             , PythonComCodeLineStateGenerator) {
    return {
        PythonComMakeListStateGenerator

        , PythonComCodeLineArrayStateGenerator
        , PythonComCodeLineStateGenerator
    }
});
