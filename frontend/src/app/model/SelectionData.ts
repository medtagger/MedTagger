export class SelectionData extends Object {
    slice_index: number;
    x: number;
    y: number;
    width: number;
    height: number;
    tag: string;
    tool: string;

    constructor(index: number, x: number, y: number, width: number, height: number, tag: string, tool: string) {
        super();
        this.slice_index = index;
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.tool = tool;
        this.tag = tag;
    }
}
