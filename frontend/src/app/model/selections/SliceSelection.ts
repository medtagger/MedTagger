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
    public getAdditionalData(): Object {
        return {};
    }

    protected static base64toBlob(base64: string, dataType: string = 'image/png'): Blob {
        let byteString = atob(base64.split(',')[1]);
        let buffer = new ArrayBuffer(byteString.length);
        let array = new Uint8Array(buffer);
        for (let i = 0; i < byteString.length; i++) {
            array[i] = byteString.charCodeAt(i);
        }
        return new Blob([buffer], {type: dataType});
    }
}
