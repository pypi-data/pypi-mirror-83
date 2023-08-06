define ([
    // 기본 
    'require'
    // + 추가 python common 폴더 패키지 : 이진용 주임
    , 'nbextensions/visualpython/src/pythonCommon/api/pythonComStateApi'
], function( requirejs
             , pythonComStateApi ) {
    "use strict";

    var PalleteBlockState = function() {
        this.palleteBlockState = {}
    }

    PalleteBlockState.prototype.setPalleteBlockState = function(palleteBlockState) {
        this.palleteBlockState = palleteBlockState;
    }

    PalleteBlockState.prototype.getPalleteBlockState = function() {
        return this.palleteBlockState;
    }

    return PalleteBlockState;
});