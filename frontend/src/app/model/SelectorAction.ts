export class SelectorAction {

    name: string;
    enable: () => boolean;
    trigger: () => void;
    isActive: boolean;

    constructor(name: string, enable: () => boolean, trigger: () => void, isActive?: boolean) {
        this.name = name;
        this.enable = enable;
        this.isActive = isActive;
        this.trigger = () => {
            trigger();
            if (this.isActive !== undefined) {
                this.isActive = true;
            }
        };
    }
}
