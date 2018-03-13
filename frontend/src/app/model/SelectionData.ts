export class SelectionData extends Object {
    slice_index: number;
    x: number;
    y: number;
    width: number;
    height: number;

    constructor(index: number, x: number, y: number, width: number, height: number) {
        super();
        this.slice_index = index;
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }
}
