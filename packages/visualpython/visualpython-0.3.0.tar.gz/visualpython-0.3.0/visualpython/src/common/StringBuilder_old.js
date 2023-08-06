class StringBuilder {
    constructor() {
        this.buffer = new Array();
    }

    /**
     * 문자열 추가.
     * @param {String} str 추가할 문자열
     */
    append(str) {
        this.buffer[this.buffer.length] = str;
    }

    /**
     * 문자열 추가하고 줄바꿈.
     * @param {String} str 추가할 문자열
     */
    appendLine(str) {
        this.append((str == null ? "" : str) + "\n");
    }

    /**
     * 문자열 포멧형 추가.
     */
    appendFormat() {
        var cnt = arguments.length;
        if (cnt < 2) 
            return "";

        var str = arguments[0];
        for (var idx = 1; idx < cnt; idx++)
            str = str.replace("{" + (idx - 1) + "}", arguments[idx]);
        this.buffer[this.buffer.length] = str;
    }

    /**
     * 문자열 포멧형 추가하고 줄바꿈.
     */
    appendFormatLine() {
        var cnt = arguments.length;
        if (cnt < 2) 
            return "";

        var str = arguments[0];
        for (var idx = 1; idx < cnt; idx++)
            str = str.replace("{" + (idx - 1) + "}", arguments[idx]);
        this.buffer[this.buffer.length] = str + "\n";
    }

    /**
     * 문자열 변환.
     * @param {String} from 변경 대상 문자열
     * @param {String} to 변경될 문자열 
     */
    replace(from, to) {
        for (var i = this.buffer.length - 1; i >= 0; i--)
            this.buffer[i] = this.buffer[i].replace(new RegExp(from, "g"), to);
    }

    /**
     * 문자열 반환.
     */
    toString() {
        return this.buffer.join("");
    }

    /**
     * 버퍼 초기화
     */
    clear() {
        this.buffer = new Array();
    }
}