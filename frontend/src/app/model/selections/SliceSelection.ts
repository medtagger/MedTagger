export abstract class SliceSelection {

    private static nextId = 1;

    public sliceIndex: number;
    public pinned: boolean;
    public hidden: boolean;
    public label_tool: string;
    public label_tag: string;

    private id: number = SliceSelection.nextId++;

    public static resetIdCounter(): void {
        this.nextId = 1;
    }

    public getId(): number {
        return this.id;
    }

    public abstract toJSON(): Object;
}
