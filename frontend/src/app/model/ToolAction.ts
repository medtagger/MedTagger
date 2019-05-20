export enum ToolActionType {
    BUTTON
}

export class ToolAction {
    name: string;
    enable: () => boolean;
    trigger: () => void;
    isActive: boolean;
    type: ToolActionType;

    /**
     * Actions associated with current tool
     *
     * @param name - Locale asset name that will be rendered on action chip, pattern TOOL.ACTION e.g. BRUSH.ERASER
     * @param enable - Condition connected with action activation
     * @param trigger - Function connected with action interaction (e.g. button click function)
     * @param type - Value from ToolActionType enum
     * @param isActive - Should it be active upon creation
     */
    constructor(name: string, enable: () => boolean, trigger: () => void,
                type: ToolActionType, isActive?: boolean) {
        this.name = name;
        this.enable = enable;
        this.isActive = isActive;
        this.trigger = () => {
            trigger();
            if (this.isActive !== undefined) {
                this.isActive = true;
            }
        };
        this.type = type;
    }
}
