export interface ScanSelection<SliceSelection> {
    _selections: SliceSelection[];

    toJSON(scalar: number): Object;
}
