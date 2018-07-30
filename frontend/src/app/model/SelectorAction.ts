export class SelectorAction {

    name: string;
    enable: () => boolean;
    trigger: () => void;

    constructor(name: string, enable: () => boolean, trigger: () => void) {
        this.name = name;
        this.enable = enable;
        this.trigger = trigger;
    }
}
