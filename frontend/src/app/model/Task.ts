export class Task {
    key: string;
    name: string;
    imagePath: string;

    constructor(key: string, name: string, imagePath: string) {
        this.key = key;
        this.name = name;
        this.imagePath = imagePath;
    }
}
