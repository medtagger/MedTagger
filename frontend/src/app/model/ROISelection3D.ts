import {ScanSelection} from './ScanSelection';
import {SliceSelection} from './SliceSelection';

export class ROISelection3D implements ScanSelection<SliceSelection> {
    _elements: SliceSelection[];

    constructor(elements?: SliceSelection[]) {
        this._elements = elements;
    }

    public get coordinates(): Object[] {
        const coordinatesArray: Object[] = [];
        this._elements.forEach((element: SliceSelection) => {
            coordinatesArray.push(element.getCoordinates());
        });
        return coordinatesArray;
    }

    toJSON(): Object {
        const jsonObject: { elements: Object[] } = {elements: []};

        if (this._elements) {
            this._elements.forEach((element: SliceSelection) => {
                jsonObject.elements.push(element.toJSON());
            });
        }

        return jsonObject;
    }
}
