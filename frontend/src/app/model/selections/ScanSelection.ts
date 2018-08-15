export interface ScanSelection<SliceSelection> {
    _elements: SliceSelection[];

    toJSON(): Object;
    getAdditionalData(): Object;
}
