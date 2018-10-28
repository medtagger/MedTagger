export class PredefinedLabelToUpload {
    taskKey: string = undefined;
    label: Object = undefined;
    neededFiles: Array<string> = [];

    constructor(taskKey: string, label: Object) {
        this.taskKey = taskKey;
        this.label = label;
        this.label['elements'].forEach((labelElement: Object) => {
            if (labelElement['tool'] === 'BRUSH') {
                this.neededFiles.push(labelElement['image_key']);
            }
        });
    }
}

export function handlePredefinedLabelFile(file: File): Promise<[string, PredefinedLabelToUpload]> {
    return new Promise(((resolve, reject) => {
        const fileReader: FileReader = new FileReader();
        fileReader.onloadend = (e: ProgressEvent) => {
            try {
                const taskKey = file.name.split('.json')[0];
                const fileContent: string = String.fromCharCode.apply(null, new Uint8Array(fileReader.result));
                const predefinedLabel = new PredefinedLabelToUpload(taskKey, JSON.parse(fileContent));
                resolve([taskKey, predefinedLabel]);
            } catch (ex) {
                console.error('Invalid JSON file!', ex);
                reject();
            }
        };
        fileReader.readAsArrayBuffer(file);
    }));
}
