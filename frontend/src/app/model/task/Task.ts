import { LabelTag } from '../labels/LabelTag';
import { TaskResponse } from '../../services/task.service';
import { TaskStatus } from './TaskStatus';
import { TaskDescription } from './TaskDescription';

export class Task {
    private _id: number;
    private _key: string;
    private _name: string;
    private _imagePath: string;
    private _tags: Array<LabelTag>;
    private _datasetsKeys: Array<string>;
    private _availableScans: number;
    private _description: string;
    private _labelExamples: Array<string>;

    constructor(taskResponse: TaskResponse, tags: Array<LabelTag>) {
        this._id = taskResponse.task_id;
        this._key = taskResponse.key;
        this._name = taskResponse.name;
        this._imagePath = taskResponse.image_path;
        this._datasetsKeys = taskResponse.datasets_keys;
        this._availableScans = taskResponse.number_of_available_scans;
        this._description = taskResponse.description;
        this._labelExamples = taskResponse.label_examples;
        this._tags = tags;
    }

    public get key(): string {
        return this._key;
    }

    public get name(): string {
        return this._name;
    }

    public get imagePath(): string {
        return this._imagePath;
    }

    public get tags(): Array<LabelTag> {
        return this._tags;
    }

    public getStatus(): TaskStatus {
        if (!!this._availableScans) {
            return new TaskStatus(this._availableScans);
        } else {
            return null;
        }
    }

    public getDescription(): TaskDescription {
        if (!!this._description && !!this._labelExamples) {
            return new TaskDescription(this._description, this._labelExamples);
        } else {
            return null;
        }
    }
}
