define([], function () {
    var CodeLineArrayEditor = function() {
        this.pythonComPageRendererThis;
        this.importPackageThis;
        this.prevUUID;
        this.currUUID;
    }

    CodeLineArrayEditor.prototype.setPythonComPageRendererThis = function(pythonComPageRendererThis) {
        this.pythonComPageRendererThis = pythonComPageRendererThis;
    }

    CodeLineArrayEditor.prototype.getPythonComPageRendererThis = function() {
        return this.pythonComPageRendererThis;
    }

    CodeLineArrayEditor.prototype.setImportPackageThis = function(importPackageThis) {
        this.importPackageThis = importPackageThis;
    }

    CodeLineArrayEditor.prototype.getImportPackageThis = function() {
        return this.importPackageThis;
    }

    return CodeLineArrayEditor;
});