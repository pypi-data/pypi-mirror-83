import { InputWidget, InputWidgetView } from "./input_widget";
import { textarea } from "../../core/dom";
import { bk_input } from "../../styles/widgets/inputs";
export class TextAreaInputView extends InputWidgetView {
    connect_signals() {
        super.connect_signals();
        this.connect(this.model.properties.name.change, () => { var _a; return this.input_el.name = (_a = this.model.name) !== null && _a !== void 0 ? _a : ""; });
        this.connect(this.model.properties.value.change, () => this.input_el.value = this.model.value);
        this.connect(this.model.properties.disabled.change, () => this.input_el.disabled = this.model.disabled);
        this.connect(this.model.properties.placeholder.change, () => this.input_el.placeholder = this.model.placeholder);
        this.connect(this.model.properties.rows.change, () => this.input_el.rows = this.model.rows);
        this.connect(this.model.properties.cols.change, () => this.input_el.cols = this.model.cols);
        this.connect(this.model.properties.max_length.change, () => this.input_el.maxLength = this.model.max_length);
    }
    render() {
        super.render();
        this.input_el = textarea({
            class: bk_input,
            name: this.model.name,
            disabled: this.model.disabled,
            placeholder: this.model.placeholder,
            cols: this.model.cols,
            rows: this.model.rows,
            maxLength: this.model.max_length,
        });
        this.input_el.textContent = this.model.value;
        this.input_el.addEventListener("change", () => this.change_input());
        this.group_el.appendChild(this.input_el);
    }
    change_input() {
        this.model.value = this.input_el.value;
        super.change_input();
    }
}
TextAreaInputView.__name__ = "TextAreaInputView";
export class TextAreaInput extends InputWidget {
    constructor(attrs) {
        super(attrs);
    }
    static init_TextAreaInput() {
        this.prototype.default_view = TextAreaInputView;
        this.define(({ Int, String }) => ({
            value: [String, ""],
            value_input: [String, ""],
            placeholder: [String, ""],
            cols: [Int, 20],
            rows: [Int, 2],
            max_length: [Int, 500],
        }));
    }
}
TextAreaInput.__name__ = "TextAreaInput";
TextAreaInput.init_TextAreaInput();
//# sourceMappingURL=textarea_input.js.map