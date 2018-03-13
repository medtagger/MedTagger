import {ROISelection2D} from './ROISelection2D';
import {SelectionData} from './SelectionData';
import {ScanSelection} from './ScanSelection';

export class ROISelection3D implements ScanSelection<ROISelection2D> {
    _selections: ROISelection2D[];

    constructor(selections?: ROISelection2D[]) {
        this._selections = selections;
    }

    public get coordinates(): Object[] {
        const coordinatesArray: Object[] = [];
        this._selections.forEach((selection: ROISelection2D) => {
            coordinatesArray.push(selection.coordinates);
        });
        return coordinatesArray;
    }

    toJSON(): Object {
        let jsonObject: { selections: SelectionData[] } = {selections: undefined};
        jsonObject.selections = [];
        if (this._selections) {
            this._selections.forEach((selection: ROISelection2D) => {
                jsonObject.selections.push(selection.toJSON());
            });
        }

        return jsonObject;
    }
}
