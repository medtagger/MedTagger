import {Injectable} from '@angular/core';

import {environment} from '../../environments/environment';
import {HttpClient} from '@angular/common/http';
import {Task} from '../model/Task';
import {Point} from '../model/Point';
import {Label} from '../model/labels/Label';
import {LabelTag} from '../model/labels/LabelTag';
import {SliceSelection} from '../model/selections/SliceSelection';
import {RectangleSelection} from '../model/selections/RectangleSelection';
import {PointSelection} from '../model/selections/PointSelection';
import {ChainSelection} from '../model/selections/ChainSelection';
import {BrushSelection} from '../model/selections/BrushSelection';

export interface RandomLabelResponse {
    label_id: string;
    scan_id: string;
    task_id: string;
    status: string;
    elements: Array<Object>;
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

    private convertElements(rawElements: Array<Object>, task: Task): Array<SliceSelection> {
        const elements: Array<SliceSelection> = [];
        rawElements.forEach((element: any) => {
            const labelTag = this.getLabelTagByKey(element.tag, task);
            switch (element.tool) {
                case 'RECTANGLE':
                    elements.push(new RectangleSelection(element.x, element.y, element.slice_index, labelTag, element.width, element.height));
                    break;
                case 'POINT':
                    elements.push(new PointSelection(element.x, element.y, element.slice_index, labelTag));
                    break;
                case 'CHAIN':
                    const points: Array<Point> = [];
                    element.points.forEach((point) => {
                        points.push(new Point(point.x, point.y));
                    });
                    elements.push(new ChainSelection(points, element.loop, element.slice_index, labelTag));
                    break;
                case 'BRUSH':
                    // Image for Brush will be loaded dynamically together with Slice Images
                    elements.push(new BrushSelection(undefined, element.slice_index, labelTag));
                    break;
                default:
                    console.error('LabelsService | convertElements | Unsupported Tool: ', element.tool);
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
                _ => {
                    resolve();
                },
                error => {
                    reject(error);
                }
            );
        });
    }
}
