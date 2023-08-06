/*!
 * jQuery Mousewheel 3.1.13
 *
 * Copyright jQuery Foundation and other contributors
 * Released under the MIT license
 * http://jquery.org/license
 */
function fontSize(element) {
    const value = getComputedStyle(element).fontSize;
    if (value != null)
        return parseInt(value, 10);
    return null;
}
function lineHeight(element) {
    var _a, _b, _c;
    const parent = (_a = element.offsetParent) !== null && _a !== void 0 ? _a : document.body;
    return (_c = (_b = fontSize(parent)) !== null && _b !== void 0 ? _b : fontSize(element)) !== null && _c !== void 0 ? _c : 16;
}
function pageHeight(element) {
    return element.clientHeight; // XXX: should be content height?
}
export function getDeltaY(event) {
    let deltaY = -event.deltaY;
    if (event.target instanceof HTMLElement) {
        switch (event.deltaMode) {
            case event.DOM_DELTA_LINE:
                deltaY *= lineHeight(event.target);
                break;
            case event.DOM_DELTA_PAGE:
                deltaY *= pageHeight(event.target);
                break;
        }
    }
    return deltaY;
}
//# sourceMappingURL=wheel.js.map