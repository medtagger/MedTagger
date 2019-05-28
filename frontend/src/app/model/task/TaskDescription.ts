export class TaskDescription {
    private _description: string;
    private _imageExamples: Array<string>;

    constructor(description: string, imageExamples: Array<string>) {
        this._description = description;
        this._imageExamples = imageExamples;
    }

    public get description(): string {
        return this._description;
    }

    public get imageExamples(): Array<string> {
        return this._imageExamples;
    }
}
