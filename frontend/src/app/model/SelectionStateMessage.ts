// Simple message format for label-explorer <-> marker <-> selector communication
export class SelectionStateMessage {
	sliceId: number;
	toDelete: boolean;

	constructor(sliceId: number, toDelete?: boolean) {
		this.sliceId = sliceId;
		this.toDelete = toDelete;
	}
}