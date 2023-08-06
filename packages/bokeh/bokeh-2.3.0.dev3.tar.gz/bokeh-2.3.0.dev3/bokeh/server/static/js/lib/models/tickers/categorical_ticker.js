import { Ticker } from "./ticker";
export class CategoricalTicker extends Ticker {
    constructor(attrs) {
        super(attrs);
    }
    get_ticks(start, end, range, _cross_loc) {
        var _a, _b;
        const majors = this._collect(range.factors, range, start, end);
        const tops = this._collect((_a = range.tops) !== null && _a !== void 0 ? _a : [], range, start, end);
        const mids = this._collect((_b = range.mids) !== null && _b !== void 0 ? _b : [], range, start, end);
        return {
            major: majors,
            minor: [],
            tops,
            mids,
        };
    }
    _collect(factors, range, start, end) {
        const result = [];
        for (const factor of factors) {
            const coord = range.synthetic(factor);
            if (coord > start && coord < end)
                result.push(factor);
        }
        return result;
    }
}
CategoricalTicker.__name__ = "CategoricalTicker";
//# sourceMappingURL=categorical_ticker.js.map