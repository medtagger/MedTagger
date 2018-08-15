export enum SelectorActionType {
    BUTTON,
    COLOR
}

export class SelectorAction {
    name: string;
    enable: () => boolean;
    trigger: () => void;
    isActive: boolean;
    type: SelectorActionType;

    constructor(name: string, enable: () => boolean, trigger: () => void,
                type: SelectorActionType, isActive?: boolean) {
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
