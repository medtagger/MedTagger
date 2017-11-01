import {LabelSelection} from './LabelSelection';

export class Label {
  labelId: string;
  scanId: string;
  labelStatus: string;
  labelSelections: LabelSelection[];

  constructor(labelId: string, scanId: string, status: string, selections: any[]) {
    this.labelId = labelId;
    this.scanId = scanId;
    this.labelStatus = status;
    const labels: LabelSelection[] = [];
    selections.forEach((selection: any) => {
      labels.push(new LabelSelection(selection.x, selection.y, selection.slice_index, selection.width, selection.height));
    });
    this.labelSelections = labels;
  }
}
