define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/container/vpContainer'
    , 'nbextensions/visualpython/src/pandas/common/pandasGenerator'
], function (requirejs, $, vpCommon, vpConst, sb, vpFuncJS, vpContainer, pdGen) {
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "Create chart"
        , funcID : "mp_plot"  // TODO: ID 규칙 생성 필요
    }

    /**
     * html load 콜백. 고유 id 생성하여 부과하며 js 객체 클래스 생성하여 컨테이너로 전달
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
    var optionLoadCallback = function(callback) {
        // document.getElementsByTagName("head")[0].appendChild(link);
        // 컨테이너에서 전달된 callback 함수가 존재하면 실행.
        if (typeof(callback) === 'function') {
            var uuid = vpCommon.getUUID();
            // 최대 10회 중복되지 않도록 체크
            for (var idx = 0; idx < 10; idx++) {
                // 이미 사용중인 uuid 인 경우 다시 생성
                if ($(vpConst.VP_CONTAINER_ID).find("." + uuid).length > 0) {
                    uuid = vpCommon.getUUID();
                }
            }
            $(vpCommon.wrapSelector(vpConst.OPTION_GREEN_ROOM)).find(vpConst.OPTION_PAGE).addClass(uuid);

            // 옵션 객체 생성
            var mpPackage = new MatplotPackage(uuid);

            // 옵션 속성 할당.
            mpPackage.setOptionProp(funcOptProp);
            // html 설정.
            mpPackage.initHtml();
            callback(mpPackage);  // 공통 객체를 callback 인자로 전달
        }
    }
    
    /**
     * html 로드. 
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
    var initOption = function(callback) {
        vpCommon.loadHtml(vpCommon.wrapSelector(vpConst.OPTION_GREEN_ROOM), "matplotlib/plot.html", optionLoadCallback, callback);
    }

    /**
     * 본 옵션 처리 위한 클래스
     * @param {String} uuid 고유 id
     */
    var MatplotPackage = function(uuid) {
        this.uuid = uuid;           // Load html 영역의 uuid.
        this.plotPackage = {
            'plot': {
                code: '${i0}.${kind}(${x}, ${y}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: '대상 변수명',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: '차트 유형'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'x축 데이터'
                    },
                    {
                        name: 'y',
                        type: 'var',
                        label: 'y축 데이터'
                    }
                ],
                variable: [
                    {
                        name: 'label',
                        type: 'text'
                    },
                    {
                        name: 'color', 
                        type: 'text',
                        default: '#000000'
                    },
                    {
                        name: 'marker',
                        type: 'text'
                    },
                    {
                        name: 'linestyle',
                        type: 'text',
                        component: 'option_select',
                        default: '-'
                    }
                ]
            },
            'bar': {
                code: '${i0}.${kind}(${x}, ${y}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: '대상 변수명',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: '차트 유형'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'x축 데이터'
                    },
                    {
                        name: 'y',
                        type: 'var',
                        label: 'y축 데이터'
                    }
                ],
                variable: [
                    {
                        name: 'label',
                        type: 'text'
                    },
                    {
                        name: 'color', 
                        type: 'text',
                        default: '#000000'
                    },
                    {
                        name: 'linestyle',
                        type: 'text',
                        component: 'option_select',
                        default: '-'
                    }
                ]
            },
            'barh': {
                code: '${i0}.${kind}(${x}, ${y}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: '대상 변수명',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: '차트 유형'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'x축 데이터'
                    },
                    {
                        name: 'y',
                        type: 'var',
                        label: 'y축 데이터'
                    }
                ],
                variable: [
                    {
                        name: 'label',
                        type: 'text'
                    },
                    {
                        name: 'color', 
                        type: 'text',
                        default: '#000000'
                    },
                    {
                        name: 'linestyle',
                        type: 'text',
                        component: 'option_select',
                        default: '-'
                    }
                ]
            },
            'hist': {
                code: '${i0}.${kind}(${x}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: '대상 변수명',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: '차트 유형'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: '데이터'
                    }
                ],
                variable: [
                    {
                        name: 'bins',
                        type: 'int',
                        required: true,
                        label: 'bins' // TODO: 라벨명
                    },
                    {
                        name: 'label',
                        type: 'text'
                    },
                    {
                        name: 'color', 
                        type: 'text',
                        default: '#000000'
                    },
                    {
                        name: 'linestyle',
                        type: 'text',
                        component: 'option_select',
                        default: '-'
                    }
                ]
            },
            'boxplot': {
                code: '${i0}.${kind}(${x}, ${y}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: '대상 변수명',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: '차트 유형'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'x축 데이터'
                    },
                    {
                        name: 'y',
                        type: 'var',
                        label: 'y축 데이터'
                    }
                ],
                variable: [
                ]
            },
            'stackplot': {
                code: '${i0}.${kind}(${x}, ${y}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: '대상 변수명',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: '차트 유형'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'x축 데이터'
                    },
                    {
                        name: 'y',
                        type: 'var',
                        label: 'y축 데이터'
                    }
                ],
                variable: [
                    {
                        name: 'color', 
                        type: 'text',
                        default: '#000000'
                    },
                    {
                        name: 'linestyle',
                        type: 'text',
                        component: 'option_select',
                        default: '-'
                    }
                ]
            },
            'pie': {
                code: '${i0}.${kind}(${x}${v}${etc})',
                tailCode: `${i0}.axis('equal')`,
                input: [
                    {
                        name: 'i0',
                        label: '대상 변수명',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: '차트 유형'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: '데이터'
                    }
                ],
                variable: [
                ]
            },
            'hexbin': {
                code: '${i0}.${kind}(${x}, ${y}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: '대상 변수명',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: '차트 유형'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'x축 데이터'
                    },
                    {
                        name: 'y',
                        type: 'var',
                        label: 'y축 데이터'
                    }
                ],
                variable: [
                    {
                        name: 'label',
                        type: 'text'
                    },
                    {
                        name: 'color', 
                        type: 'text',
                        default: '#000000'
                    }
                ]
            },
            'contour': {
                code: '${i0}.${kind}(${x}, ${y}, ${z}${v}${etc})',
                tailCode: '${i0}.colorbar()', // 색상 막대 범례 표시
                input: [
                    {
                        name: 'i0',
                        label: '대상 변수명',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: '차트 유형'
                    },
                    {
                        name: 'x',
                        type: 'var',
                        label: 'x축 데이터'
                    },
                    {
                        name: 'y',
                        type: 'var',
                        label: 'y축 데이터'
                    },
                    {
                        name: 'z',
                        type: 'var',
                        label: 'z축 데이터'
                    }
                ],
                variable: [
                    {
                        name: 'cmap',
                        type: 'text'
                    },
                    {
                        name: 'label',
                        type: 'text'
                    }
                ]
            },
            'imshow': {
                code: '${i0}.${kind}(${z}${v}${etc})',
                input: [
                    {
                        name: 'i0',
                        label: '대상 변수명',
                        type: 'int',
                        required: false
                    },
                    {
                        name: 'kind',
                        type: 'var',
                        label: '차트 유형'
                    },
                    {
                        name: 'z',
                        type: 'var',
                        label: 'z축 데이터'
                    }
                ],
                variable: [
                    {
                        name: 'extent', // [xmin, xmax, ymin, ymax]
                        type: 'var'
                    },
                    {
                        name: 'origin',
                        type: 'text'
                    },
                    {
                        name: 'cmap',
                        type: 'text'
                    }
                ]
            }
        };
        this.package = this.plotPackage['plot'];
        
        this.optionalPackage = {
            'title': {
                code: '${i0}.set_title(${title})',
                code2: 'plt.title(${title})',
                input: [
                    {
                        name: 'i0',
                        type: 'var',
                        required: false
                    },
                    {
                        name: 'title',
                        type: 'text',
                        required: false
                    }
                ]
            },
            'xlabel': {
                code: '${i0}.set_xlabel(${xlabel})',
                code2: 'plt.xlabel(${xlabel})',
                input: [
                    {
                        name: 'i0',
                        type: 'var',
                        required: false
                    },
                    {
                        name: 'xlabel',
                        type: 'var',
                        required: false
                    }
                ]
            },
            'ylabel': {
                code: '${i0}.set_ylabel(${ylabel})',
                code2: 'plt.ylabel(${ylabel})',
                input: [
                    {
                        name: 'i0',
                        type: 'var',
                        required: false
                    },
                    {
                        name: 'ylabel',
                        type: 'var',
                        required: false
                    }
                ]
            },
            'xlim': {
                code: '${i0}.set_xlim(${xlim})',
                code2: 'plt.xlim(${xlim})',
                input: [
                    {
                        name: 'i0',
                        type: 'var',
                        required: false
                    },
                    {
                        name: 'xlim',
                        type: 'var',
                        required: false
                    }
                ]
            },
            'ylim': {
                code: '${i0}.set_ylim(${ylim})',
                code2: 'plt.ylim(${ylim})',
                input: [
                    {
                        name: 'i0',
                        type: 'var',
                        required: false
                    },
                    {
                        name: 'ylim',
                        type: 'var',
                        required: false
                    }
                ]
            },
            'legend': {
                code: '${i0}.legend(${v})',
                code2: 'plt.legend(${v})',
                input: [
                    {
                        name: 'i0',
                        type: 'var'
                    }
                ],
                variable: [
                    {
                        key: 'title',
                        name: 'legendTitle',
                        type: 'text'
                    },
                    {
                        key: 'label',
                        name: 'legendLabel',
                        type: 'var'
                    },
                    {
                        key: 'loc',
                        name: 'legendLoc',
                        type: 'text',
                        component: 'option_select',
                        default: 'best'
                    }
                ]
            }
        };
        // plot 종류
        this.plotKind = [
            'plot', 'bar', 'barh', 'hist', 'boxplot', 'stackplot',
            'pie', 'scatter', 'hexbin', 'contour', 'imshow', 'errorbar'
        ];
        this.plotKindLang = {
            'plot': '플롯',
            'bar': '바 차트',
            'barh': '가로 바',
            'hist': '히스토그램',
            'boxplot': '박스 플롯',
            'stackplot': '스택 플롯',
            'pie': '파이 차트',
            'scatter': '스캐터 플롯',
            'hexbin': '헥스빈 플롯',
            'contour': '컨투어 플롯',
            'imshow': '이미지 플롯',
            'errorbar': '오차 막대'
        };
        // cmap 종류
        this.cmap = [
            '', 'viridis', 'plasma', 'inferno', 'magma', 'cividis'
            , 'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c'
        ];
    }



    /**
     * vpFuncJS 에서 상속
     */
    MatplotPackage.prototype = Object.create(vpFuncJS.VpFuncJS.prototype);

    /**
     * 유효성 검사
     * @returns 유효성 검사 결과. 적합시 true
     */
    MatplotPackage.prototype.optionValidation = function() {
        return true;

        // 부모 클래스 유효성 검사 호출.
        // vpFuncJS.VpFuncJS.prototype.optionValidation.apply(this);
    }


    /**
     * html 내부 binding 처리
     */
    MatplotPackage.prototype.initHtml = function() {
        this.showFunctionTitle();
        
        // 차트 서브플롯 페이지 구성
        this.bindSubplotOption1();
        this.bindCmapSelector();

        this.bindSubplotOption2();

        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "pandas/commonPandas.css");
        this.loadCss(Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.STYLE_PATH + "matplotlib/plot.css");
    }

    /**
     * 선택한 패키지명 입력
     */
    MatplotPackage.prototype.showFunctionTitle = function() {
        $(this.wrapSelector('.vp_functionName')).text(funcOptProp.funcName);
    }

    /**
     * 서브플롯 옵션 페이지 구성
     */
    MatplotPackage.prototype.bindSubplotOption1 = function() {
        var that = this;

        // 차트 추가 사용 여부 이벤트
        $(this.wrapSelector('#disableChart')).change(function() {
            var checked = $(this).prop('checked');
            if (checked == true) {
                // 차트 추가 안 함
                $(that.wrapSelector('#vp_plotSetting table')).hide();
                $(that.wrapSelector('#vp_userOption')).hide();
            } else {
                // 차트 추가 함
                $(that.wrapSelector('#vp_plotSetting table')).show();
                $(that.wrapSelector('#vp_userOption')).show();
            }
        });

        // 차트 유형 선택지 구성
        this.bindKindSelector();

        // 색상 사용여부
        $(this.wrapSelector('#useColor')).change(function() {
            var checked = $(this).prop('checked');
            if (checked == true) {
                // 색상 선택 가능하게
                $(that.wrapSelector('#color')).removeAttr('disabled');
            } else {
                $(that.wrapSelector('#color')).attr('disabled', 'true');
            }
        })

        // TODO: 마커 이미지 표시 (또는 hover에 표시)
        var optionTagList = $(this.wrapSelector('#markerSelector option'));
        // [0] 직접입력 제외
        for (var i = 1; i < optionTagList.length; i++) {
            // 이미지 파일명
            var imgFile = $(optionTagList[i]).data('img');
            // 이미지 url 바인딩
            var url = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.RESOURCE_PATH + 'matplotlib/' + imgFile;
            $(optionTagList[i]).attr({
                'data-img': url
            });
        }

        // 마커 : 직접입력 선택 시 input 태그 활성화
        $(this.wrapSelector('#markerSelector')).change(function() {
            var selected = $(this).val();
            if (selected == "marker") {
                $(this).parent().find('#marker').show();
                $(this).parent().find('#marker').val('');
            } else {
                $(this).parent().find('#marker').hide();
                $(this).parent().find('#marker').val(selected);
            }
        });

        // 사용자 옵션 구성
        this.bindUserOption();

    }

    /**
     * 서브플롯 옵션 페이지2 구성
     */
    MatplotPackage.prototype.bindSubplotOption2 = function() {
        var that = this;

        // 범례 표시 여부 체크박스
        $(this.wrapSelector('#legend')).change(function() {
            var checked = $(this).prop('checked');

            if (checked == true) {
                $(that.wrapSelector('#legendbox')).removeClass('folded');
            } else {
                $(that.wrapSelector('#legendbox')).addClass('folded');
            }
        });
    };

    /**
     * 사용자 옵션 추가 페이지 이벤트
     */
    MatplotPackage.prototype.bindUserOption = function() {
        var that = this;
        $(this.wrapSelector('#vp_addOption')).click(function() {
            // 옵션 추가
            var tagTr = document.createElement('tr');
            var tagTdKey = document.createElement('td');
            var tagTdValue = document.createElement('td');
            var tagInputKey = document.createElement('input');
            $(tagInputKey).attr({
                type: 'text'
            });
            var tagInputValue = document.createElement('input');
            $(tagInputValue).attr({
                type: 'text'
            });

            var tagTdDel = document.createElement('td');
            var tagBtnDel = document.createElement('input');
            $(tagBtnDel).attr({
                type: 'button',
                value: 'X'
            });
            $(tagBtnDel).click(function() {
                // X 버튼과 동일한 행 삭제
                $(this).parent().parent().remove();
            });
            
            $(tagTdKey).append(tagInputKey);
            $(tagTdValue).append(tagInputValue);
            $(tagTdDel).append(tagBtnDel);
            $(tagTr).append(tagTdKey);
            $(tagTr).append(tagTdValue);
            $(tagTr).append(tagTdDel);

            $(that.wrapSelector('#vp_userOption table tr:last')).before(tagTr);
        });
    }

    /**
     * 차트 유형 선택지 구현
     */
    MatplotPackage.prototype.bindKindSelector = function() {
        // 차트유형 selector 동적 구성
        var selector = $(this.wrapSelector('#kind'));
        var that = this;
        this.plotKind.forEach(kind => {
            var option = document.createElement('option');
            $(option).attr({
                id: kind,
                name: 'kind',
                value: kind
            });
            var span = document.createElement('span');
            $(span).attr({
                // class="vp-multilang" data-caption-id="imshow"
                class: 'vp-multilang',
                'data-caption-id':kind
            });
            span.append(document.createTextNode(that.plotKindLang[kind]))
            option.appendChild(span);
            selector.append(option);
        });

        // 차트유형 선택지에 맞게 옵션 표시
        $(selector).change(function() {
            var kind = $(this).val();
            var package = that.plotPackage[kind];
            if (package == undefined) package = that.plotPackage['plot'];

            // 모두 숨기기 (단, 대상 변수 입력란과 차트 유형 선택지 제외)
            $(that.wrapSelector('#vp_plotSetting table tr:gt(2)')).hide();

            // 해당 옵션에 있는 선택지만 보이게 처리
            package.input.forEach(obj => {
                $(that.wrapSelector('#' + obj.name)).closest('tr').show();
            });
            package.variable.forEach(obj => {
                $(that.wrapSelector('#' + obj.name)).closest('tr').show();
            });
        });

        // 플롯 차트 옵션으로 초기화
        var plotPackage = this.plotPackage['plot'];
        // 모두 숨기기 (단, 대상 변수 입력란과 차트 유형 선택지 제외)
        $(this.wrapSelector('#vp_plotSetting table tr:gt(2)')).hide();

        // 해당 옵션에 있는 선택지만 보이게 처리
        plotPackage.input.forEach(obj => {
            $(this.wrapSelector('#' + obj.name)).closest('tr').show();
        });
        plotPackage.variable.forEach(obj => {
            $(this.wrapSelector('#' + obj.name)).closest('tr').show();
        });
    }

    /**
     * 색상 스타일 선택지 구현
     */
    MatplotPackage.prototype.bindCmapSelector = function() {
        // 기존 cmap 선택하는 select 태그 안보이게
        var cmapSelector = this.wrapSelector('#cmap');
        $(cmapSelector).hide();

        // cmap 데이터로 cmap selector 동적 구성
        this.cmap.forEach(ctype => {
            var option = document.createElement('option');
            $(option).attr({
                'name': 'cmap',
                'value': ctype
            });
            $(option).text(ctype == ''?'선택 안 함':ctype);
            $(cmapSelector).append(option);
        });

        // cmap 데이터로 팔레트 div 동적 구성
        this.cmap.forEach(ctype => {
            var divColor = document.createElement('div');
            $(divColor).attr({
                'class': 'vp-plot-cmap-item',
                'data-cmap': ctype,
                'data-url': 'pandas/cmap/' + ctype + '.JPG',
                'title': ctype
            });
            $(divColor).text(ctype == ''?'선택 안 함':ctype);
            
            // 이미지 url 바인딩
            var url = Jupyter.notebook.base_url + vpConst.BASE_PATH + vpConst.RESOURCE_PATH + 'pandas/cmap/' + ctype + '.JPG';
            $(divColor).css({
                'background-image' : 'url(' + url + ')'
            })

            var selectedCmap = this.wrapSelector('#vp_selectedCmap');

            // 선택 이벤트 등록
            $(divColor).click(function() {
                if (!$(this).hasClass('selected')) {
                    $(this).parent().find('.vp-plot-cmap-item.selected').removeClass('selected');
                    $(this).addClass('selected');
                    // 선택된 cmap 이름 표시
                    $(selectedCmap).text(ctype == ''?'선택 안 함':ctype);
                    // 선택된 cmap data-caption-id 변경
                    $(selectedCmap).attr('data-caption-id', ctype);
                    // select 태그 강제 선택
                    $(cmapSelector).val(ctype).prop('selected', true);
                }
            });
            $(this.wrapSelector('#vp_plotCmapSelector')).append(divColor);
        });

        // 선택 이벤트
        $(this.wrapSelector('.vp-plot-cmap-wrapper')).click(function() {
            $(this).toggleClass('open');
        });
    }

    /**
     * 간단 코드 변환기
     * @param {string} code 코드 
     * @param {Array} input 변수 목록
     */
    MatplotPackage.prototype.simpleCodeGenerator = function(code, input, variable=[]) {
        input.forEach(obj => {
            var val = pdGen.vp_getTagValue(this.uuid, obj);
            code = code.split('${' + obj.name + '}').join(val);
        });
        var opt_params = '';
        variable.forEach(obj => {
            var val = pdGen.vp_getTagValue(this.uuid, obj);
            
            if (val != '') {
                if (obj.type == 'text') {
                    val = '"'+val+'"';
                } else if (obj.type == 'list') {
                    val = '['+val+']';
                }
                opt_params += ', ' + obj.key + '=' + val;
            }
        });
        code = code.split('${v}').join(opt_params);

        // () 함수 파라미터 공간에 input 없을 경우 (, ${v}) 와 같은 형태로 출력되는 것 방지
        code = code.split('(, ').join('(');

        return code;
    }

    /**
     * 코드 생성
     * @param {boolean} exec 실행여부
     */
    MatplotPackage.prototype.generateCode = function(exec) {
        if (!this.optionValidation()) return;

        try {
            var sbCode = new sb.StringBuilder();

            // 코드 생성 여부 : 코드 생성된 파트가 있을 때만 추가
            var doGenerate = false;
            
            // add prefix code
            var prefixCode = $(this.wrapSelector('#vp_prefixBox textarea')).val();
            if (prefixCode.length > 0) {
                sbCode.appendLine(prefixCode);
            }

            // 대상 변수가 입력되어 있지 않으면 plot(plt) 포커스에 차트 그리기
            var i0Input = $(this.wrapSelector('#i0_input')).val();
            var usePlotFunction = (i0Input == ''); // 대상 변수로 plt 를 사용할지 여부

            // 차트 생성 안 함에 체크 안되어 있을 경우에만 새 차트 생성
            var disableChart = $(this.wrapSelector('#disableChart')).prop('checked');
            if (disableChart == false) {
                doGenerate = true;
                
                // 패키지 복사
                var kind = $(this.wrapSelector('#kind')).val();
                var package = this.plotPackage[kind];
                // 원하는 패키지가 없으면 기본 플롯 옵션 불러오기
                if (package == undefined) {
                    package = this.plotPackage['plot'];
                }
                package = JSON.parse(JSON.stringify(package));

                if (usePlotFunction) {
                    $(this.wrapSelector('#i0')).val('plt');
                    i0Input = 'plt';
                } else {
                    $(this.wrapSelector('#i0')).val(i0Input);
                }
                // 색상 사용 안하면 코드에 표시되지 않도록
                if ($(this.wrapSelector('#useColor')).prop('checked') != true) {
                    var idx = package.variable.findIndex(function(item) {return item.name === 'color'});
                    if (idx > -1) {
                        package.variable.splice(idx, 1);
                    }
                }

                // 사용자 옵션 설정값 가져오기
                var userOption = new sb.StringBuilder();
                $(this.wrapSelector('#vp_userOption table tr:gt(0):not(:last)')).each(function() {
                    var key = $(this).find('td:nth-child(1) input').val();
                    var val = $(this).find('td:nth-child(2) input').val();
                    if (key != '' && val != '') {
                        userOption.appendFormat(', {0}={1}', key, val);
                    } else {
                        throw '사용자 옵션 키/값을 입력하거나 삭제해 주세요.';
                    }
                });

                // 플롯 구성 코드 생성
                var plotCode = pdGen.vp_codeGenerator(this.uuid, package, userOption.toString());
                if (plotCode == null) return "BREAK_RUN"; // 코드 생성 중 오류 발생
                sbCode.append(plotCode);

                // 꼬리 코드 입력
                if (package.tailCode != undefined) {
                    sbCode.append('\n' + package.tailCode.split('${i0}').join(i0Input));
                }
            }

            // 추가 구성 코드 생성
            var optPackList = ['title', 'xlabel', 'ylabel', 'xlim', 'ylim'];
            for (var i = 0; i < optPackList.length; i++) {
                var opt = optPackList[i];
                // 주요 값이 없으면 패스
                if ($(this.wrapSelector('#'+opt)).val() == '') {
                    continue;
                } 

                var pack = this.optionalPackage[opt];
                var code = '';
                
                if (usePlotFunction) {
                    // plt 함수 사용
                    code = this.simpleCodeGenerator(pack.code2, pack.input);
                } else {
                    // 대상 변수(axes) 함수 사용
                    code = this.simpleCodeGenerator(pack.code, pack.input);
                }
                if (code != '') {
                    doGenerate = true;
                    sbCode.append('\n' + code);
                }
            }

            // 범례 코드 생성
            // 범례 패키지 가져오기
            var legendPackage = this.optionalPackage['legend'];
            if ($(this.wrapSelector('#legend')).prop('checked') == true) {
                doGenerate = true;

                var legendCode = '';
                if (usePlotFunction) {
                    // plt 함수 사용
                    legendCode = this.simpleCodeGenerator(legendPackage.code2, [], legendPackage.variable);
                } else {
                    // 대상 변수(axes) 함수 사용
                    legendCode = this.simpleCodeGenerator(legendPackage.code, legendPackage.input);
                }
                sbCode.append('\n' + legendCode);
            }
            
            // cell metadata 작성하기
            // pdGen.vp_setCellMetadata(_VP_CODEMD);

            // add postfix code
            var postfix = $(this.wrapSelector('#vp_postfixBox textarea')).val();
            if (postfix.length > 0) {
                sbCode.appendLine('');
                sbCode.append(postfix);
            }

            // 코드 추가 및 실행
            if (doGenerate) {
                this.cellExecute(sbCode.toString(), exec);
            } else {
                throw '생성할 코드가 없습니다.';
            }
        } catch (exmsg) {
            // 에러 표시
            vpCommon.renderAlertModal(exmsg);
            return "BREAK_RUN"; // 코드 생성 중 오류 발생
        }
    }

    return {
        initOption: initOption
    };
});