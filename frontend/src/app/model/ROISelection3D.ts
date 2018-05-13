import {ROISelection2D} from './ROISelection2D';
import {SelectionData} from './SelectionData';
import {ScanSelection} from './ScanSelection';

export class ROISelection3D implements ScanSelection<ROISelection2D> {
    _elements: ROISelection2D[];

    constructor(elements?: ROISelection2D[]) {
        this._elements = elements;
    }

    public get coordinates(): Object[] {
        const coordinatesArray: Object[] = [];
        this._elements.forEach((element: ROISelection2D) => {
            coordinatesArray.push(element.coordinates);
        });
        return coordinatesArray;
    }

    toJSON(): Object {
        let jsonObject: { elements: SelectionData[] } = {elements: undefined};
        jsonObject.elements = [];
        if (this._elements) {
            this._elements.forEach((element: ROISelection2D) => {
                jsonObject.elements.push(element.toJSON());
            });
        }

        return jsonObject;
    }
}
