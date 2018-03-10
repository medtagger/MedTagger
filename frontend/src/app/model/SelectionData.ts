export class SelectionData {
    slice_index: number;
    x: number;
    y: number;
    width: number;
    height: number;

    constructor(index: number, x: number, y: number, width: number, height: number) {
        this.slice_index = index;
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }
}
