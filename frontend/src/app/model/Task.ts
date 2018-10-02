import {LabelTag} from './labels/LabelTag';

export class Task {
    id: number;
    key: string;
    name: string;
    imagePath: string;
    tags: Array<LabelTag>;
    datasets_keys: Array<string>;

    constructor(id: number, key: string, name: string, imagePath: string, tags: Array<LabelTag>,
                datasets_keys: Array<string>) {
        this.id = id;
        this.key = key;
        this.name = name;
        this.imagePath = imagePath;
        this.tags = tags;
        this.datasets_keys = datasets_keys;
    }
}
