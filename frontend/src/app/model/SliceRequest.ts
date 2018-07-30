export class SliceRequest {
    _slice: number;
    _reversed: boolean;

    constructor(slice: number, reversed: boolean = false) {
        this._slice = slice;
        this._reversed = reversed;
    }

    public get slice() {
        return this._slice;
    }

    public get reversed() {
        return this._reversed;
    }
}
