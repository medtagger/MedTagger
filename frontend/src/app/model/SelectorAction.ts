export enum SelectorActionType {
    BUTTON,
    SLIDER,
    COLOR_PICKER
}

export class SelectorAction {
    name: string;
    enable: () => boolean;
    trigger: (data?: any) => void;
    isActive: boolean;
    type: SelectorActionType;
    options: object;

    constructor(name: string, enable: () => boolean, trigger: (data?: any) => void,
                type: SelectorActionType, isActive?: boolean, options?: object) {
        this.name = name;
        this.enable = enable;
        this.isActive = isActive;
        this.trigger = (data) => {
            trigger(data);
            if (this.isActive !== undefined) {
                this.isActive = true;
            }
        };
        this.type = type;
        this.options = options;
    }
}
