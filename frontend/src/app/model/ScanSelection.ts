export interface ScanSelection<SliceSelection> {
    _selections: SliceSelection[];

    toJSON(): Object;
}
