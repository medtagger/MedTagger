export class LabelTag {
    name: string;
    key: string;
    tools: Array<string>;
    hidden: boolean;

    constructor(name: string, key: string, tools: Array<string>) {
        this.name = name;
        this.key = key;
        this.tools = tools;
        this.hidden = false;
    }
}
