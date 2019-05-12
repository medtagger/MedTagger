import { BinaryConverter } from '../utils/BinaryConverter';

export class MarkerSlice {
    private readonly _id: number;
    private readonly _index: number;
    private readonly _lastInBatch: number;
    private readonly _source: string;

    constructor(id: string, index: number, lastInBatch: number, source: ArrayBuffer | string) {
        this._id = +id;
        this._index = index;
        this._lastInBatch = lastInBatch;
        if (source instanceof ArrayBuffer) {
            this._source = BinaryConverter.byteToBase64(source);
        } else if (typeof String) {
            this._source = source;
        } else {
            this._source = undefined;
        }
    }

    public get id() {
        return this._id;
    }

    public get index() {
        return this._index;
    }

    public get source() {
        return this._source;
    }

    public isLastInBatch(): boolean {
        return this._index === this._lastInBatch;
    }
}
