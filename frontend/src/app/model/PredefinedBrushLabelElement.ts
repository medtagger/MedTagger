import {BinaryConverter} from '../utils/BinaryConverter';

export class PredefinedBrushLabelElement {
    private readonly _scan_id: string;
    private readonly _tag_key: string;
    private readonly _index: number;
    private readonly _source: string;

    constructor(scan_id: string, tag_key: string, index: number, source: ArrayBuffer | string) {
        this._scan_id = scan_id;
        this._tag_key = tag_key;
        this._index = index;
        if (source instanceof ArrayBuffer) {
            this._source = BinaryConverter.byteToBase64(source);
        } else if (typeof String) {
            this._source = source;
        } else {
            this._source = undefined;
        }
    }

    public get scan_id() {
        return this._scan_id;
    }

    public get tag_key() {
        return this._tag_key;
    }

    public get index() {
        return this._index;
    }

    public get source() {
        return this._source;
    }
}
