// Simple message format for label-explorer <-> marker <-> selector communication
export class SelectionStateMessage {
    selectionId: number;
    sliceId: number;
    toDelete: boolean;

    constructor(selectionId: number, sliceId: number, toDelete?: boolean) {
        this.selectionId = selectionId;
        this.sliceId = sliceId;
        this.toDelete = toDelete;
    }
}
