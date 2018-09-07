export class LabelTag {
    key: string;
    name: string;
    tools: Array<string>;
    hidden: boolean;

    constructor(key: string, name: string, tools: Array<string>) {
        this.key = key;
        this.name = name;
        this.tools = tools;
        this.hidden = false;
    }
}
