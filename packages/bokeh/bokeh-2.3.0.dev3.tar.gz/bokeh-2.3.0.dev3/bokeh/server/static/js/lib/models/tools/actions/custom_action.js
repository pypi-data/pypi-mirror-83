import { ActionTool, ActionToolView, ActionToolButtonView } from "./action_tool";
import { bk_toolbar_button_custom_action } from "../../../styles/toolbar";
export class CustomActionButtonView extends ActionToolButtonView {
    css_classes() {
        return super.css_classes().concat(bk_toolbar_button_custom_action);
    }
}
CustomActionButtonView.__name__ = "CustomActionButtonView";
export class CustomActionView extends ActionToolView {
    doit() {
        var _a;
        (_a = this.model.callback) === null || _a === void 0 ? void 0 : _a.execute(this.model);
    }
}
CustomActionView.__name__ = "CustomActionView";
export class CustomAction extends ActionTool {
    constructor(attrs) {
        super(attrs);
        this.tool_name = "Custom Action";
        this.button_view = CustomActionButtonView;
    }
    static init_CustomAction() {
        this.prototype.default_view = CustomActionView;
        this.define(({ Any, String, Nullable }) => ({
            action_tooltip: [String, "Perform a Custom Action"],
            callback: [Nullable(Any /*TODO*/)],
            icon: [String],
        }));
    }
    get tooltip() {
        return this.action_tooltip;
    }
}
CustomAction.__name__ = "CustomAction";
CustomAction.init_CustomAction();
//# sourceMappingURL=custom_action.js.map