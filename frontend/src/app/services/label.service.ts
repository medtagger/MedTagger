import {Injectable} from '@angular/core';

import {environment} from '../../environments/environment';
import {Label} from '../model/labels/Label';
import {HttpClient} from '@angular/common/http';
import {SliceSelection} from '../model/selections/SliceSelection';
import {LabelTag} from "../model/labels/LabelTag";
import {ROISelection2D} from "../model/selections/ROISelection2D";
import {Task} from "../model/Task";

interface RandomLabelResponse {
    label_id: string;
    scan_id: string;
    task_id: string;
    status: string;
    elements: Array<SliceSelection>;
    labeling_time: number;
    comment: string;
}

@Injectable()
export class LabelService {

    constructor(private http: HttpClient) {}

    private getLabelTagByKey(tagKey: string, task: Task): LabelTag {
        for (let i = 0; i < task.tags.length; i++) {
            const tag = task.tags[i];
            if (tag.key === tagKey) {
                return tag;
            }
        }
    }

    private convertElements(rawElements: any, task: Task): Array<SliceSelection> {
        const elements: Array<SliceSelection> = [];
        rawElements.forEach((element: any) => {
            if (element.tool === 'RECTANGLE') {
                const labelTag = this.getLabelTagByKey(element.tag, task);
                elements.push(new ROISelection2D(element.x, element.y, element.slice_index, labelTag, element.width, element.height));
            }
        });
        return elements;
    }

    getRandomLabel(task: Task): Promise<Label> {
        return new Promise((resolve, reject) => {
            this.http.get<RandomLabelResponse>(environment.API_URL + '/labels/random').toPromise().then(
                response => {
                    console.log('LabelsService | getRandomLabel | response: ', response);
                    resolve(new Label(response.label_id, response.scan_id, response.status,
                                      this.convertElements(response.elements, task), response.labeling_time, response.comment));
                },
                error => {
                    console.log('LabelsService | getRandomLabel | error: ', error);
                    reject(error);
                }
            );
        });
    }

    getLabelByID(labelID: string, task: Task): Promise<Label> {
        return new Promise((resolve, reject) => {
            this.http.get<RandomLabelResponse>(environment.API_URL + '/labels/' + labelID).toPromise().then(
                response => {
                    console.log('LabelsService | getLabelByID | response: ', response);
                    resolve(new Label(response.label_id, response.scan_id, response.status,
                                      this.convertElements(response.elements, task), response.labeling_time, response.comment));
                },
                error => {
                    console.log('LabelsService | getLabelByID | error: ', error);
                    reject(error);
                }
            );
        });
    }

    changeStatus(labelId: string, status: string) {
        return new Promise((resolve, reject) => {
            const payload = {'status': status};
            this.http.put(environment.API_URL + '/labels/' + labelId + '/status', payload).toPromise().then(
                response => {
                    resolve();
                },
                error => {
                    reject(error);
                }
            );
        });
    }
}
