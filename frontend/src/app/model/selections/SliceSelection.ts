import { LabelTag } from './../labels/LabelTag';

export enum SliceSelectionType {
    NORMAL,
    DRAFT,
    ARCHIVED
}

export abstract class SliceSelection {

    private static nextId = 1;

    public sliceIndex: number;
    public pinned = false;
    public hidden = false;
    public labelTool: string;
    public labelTag: LabelTag;
    public type: SliceSelectionType;

    private id: number = SliceSelection.nextId++;

    public static resetIdCounter(): void {
        this.nextId = 1;
    }

    constructor(sliceIndex: number, labelTool: string, labelTag: LabelTag, type: SliceSelectionType) {
        this.sliceIndex = sliceIndex;
        this.labelTool = labelTool;
        this.labelTag = labelTag;
        this.type = type;
    }

    public getId(): number {
        return this.id;
    }

    protected setId(newId: number): void {
        this.id = newId;
    }

    public abstract toJSON(): Object;
    public getAdditionalData(): Object {
        return {};
    }
}
