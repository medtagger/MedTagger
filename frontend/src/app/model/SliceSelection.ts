export abstract class SliceSelection {

    private static nextId = 0;

    public sliceIndex: number;
    public pinned: boolean;
    public hidden: boolean;
    public label_tool: string;
    public label_tag: string;

    private id: number = SliceSelection.nextId++;

    public getId(): number {
        return this.id;
    }

    public abstract getCoordinates();

    public abstract toJSON(): Object;
}
