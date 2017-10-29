import {ROISelection2D} from './ROISelection2D';
import {SelectionData} from './SelectionData';

export class ROISelection3D {
  _roiSelections: ROISelection2D[];

  constructor(selections: ROISelection2D[]) {
    this._roiSelections = selections;
  }

  public get coordinates() {
    const coordinatesArray: Object[] = [];
    this._roiSelections.forEach((selection: ROISelection2D) => {
      coordinatesArray.push(selection.coordinates);
    });
    return coordinatesArray;
  }

  public toJSON(): {selections: SelectionData[]} {
    const jsonObject: {selections: SelectionData[]} = {selections: undefined};
    jsonObject.selections = [];
    this._roiSelections.forEach((selection: ROISelection2D) => {
      jsonObject.selections.push(selection.toJSON());
    });

    return jsonObject;
  }
}
