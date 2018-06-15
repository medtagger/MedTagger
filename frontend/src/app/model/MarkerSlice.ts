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
            this._source = MarkerSlice.byteToBase64(source);
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

    public isLastInBatch() : Boolean {
        return this._index == this._lastInBatch;
    }

    private static byteToBase64(byteImage: ArrayBuffer): string {
        const bytes = new Uint8Array(byteImage);
        let binary = '';
        for (let i = 0; i < bytes.byteLength; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return 'data:image/png;base64,' + btoa(binary);
    }
}
