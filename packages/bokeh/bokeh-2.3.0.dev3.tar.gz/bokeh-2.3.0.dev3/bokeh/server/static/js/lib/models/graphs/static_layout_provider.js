import { LayoutProvider } from "./layout_provider";
import { NumberArray } from "../../core/types";
export class StaticLayoutProvider extends LayoutProvider {
    constructor(attrs) {
        super(attrs);
    }
    static init_StaticLayoutProvider() {
        this.define(({ Number, Tuple, Dict }) => ({
            graph_layout: [Dict(Tuple(Number, Number)), {}],
        }));
    }
    get_node_coordinates(node_source) {
        var _a;
        const index = (_a = node_source.data.index) !== null && _a !== void 0 ? _a : [];
        const n = index.length;
        const xs = new NumberArray(n);
        const ys = new NumberArray(n);
        for (let i = 0; i < n; i++) {
            const point = this.graph_layout[index[i]];
            const [x, y] = point !== null && point !== void 0 ? point : [NaN, NaN];
            xs[i] = x;
            ys[i] = y;
        }
        return [xs, ys];
    }
    get_edge_coordinates(edge_source) {
        var _a, _b;
        const starts = (_a = edge_source.data.start) !== null && _a !== void 0 ? _a : [];
        const ends = (_b = edge_source.data.end) !== null && _b !== void 0 ? _b : [];
        const n = Math.min(starts.length, ends.length);
        const xs = [];
        const ys = [];
        const has_paths = edge_source.data.xs != null && edge_source.data.ys != null;
        for (let i = 0; i < n; i++) {
            const in_layout = this.graph_layout[starts[i]] != null && this.graph_layout[ends[i]] != null;
            if (has_paths && in_layout) {
                xs.push(edge_source.data.xs[i]);
                ys.push(edge_source.data.ys[i]);
            }
            else {
                let start, end;
                if (in_layout) {
                    start = this.graph_layout[starts[i]];
                    end = this.graph_layout[ends[i]];
                }
                else {
                    start = [NaN, NaN];
                    end = [NaN, NaN];
                }
                xs.push([start[0], end[0]]);
                ys.push([start[1], end[1]]);
            }
        }
        return [xs, ys];
    }
}
StaticLayoutProvider.__name__ = "StaticLayoutProvider";
StaticLayoutProvider.init_StaticLayoutProvider();
//# sourceMappingURL=static_layout_provider.js.map