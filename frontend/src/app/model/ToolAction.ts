export enum ToolActionType {
    BUTTON,
    COLOR
}

export class ToolAction {
    name: string;
    enable: () => boolean;
    trigger: () => void;
    isActive: boolean;
    type: ToolActionType;

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
