import {ROISelection2D} from './ROISelection2D';

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
}
