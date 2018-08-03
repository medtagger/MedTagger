import {LabelTag} from "./LabelTag";

export class Task {
    id: number;
    key: string;
    name: string;
    imagePath: string;
    tags: Array<LabelTag>;

    constructor(id: number, key: string, name: string, imagePath: string, tags: Array<LabelTag>) {
        this.id = id;
        this.key = key;
        this.name = name;
        this.imagePath = imagePath;
        this.tags = tags;
    }
}
