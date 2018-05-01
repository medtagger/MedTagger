export interface SliceSelection {
    sliceIndex: number;
	pinned: boolean;
	hidden: boolean;

    scaleToView(scalarX: number, scalarY: number): void;
}
