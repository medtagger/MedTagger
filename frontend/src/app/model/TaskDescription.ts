export class TaskDescription {
    private description: string;
    private imageExamples: Array<any>;

    constructor(description: string, imageExamples: Array<any>) {
        this.description = description;
        this.imageExamples = imageExamples;
    }
}