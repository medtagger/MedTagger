import {LabelSelection} from './LabelSelection';
import {SliceSelection} from './SliceSelection';

export class Label {
  labelId: string;
  scanId: string;
  labelStatus: string;
  labelSelections: SliceSelection[];

  constructor(labelId: string, scanId: string, status: string, selections: SliceSelection[]) {
    this.labelId = labelId;
    this.scanId = scanId;
    this.labelStatus = status;
    // const labels: LabelSelection[] = [];
    this.labelSelections = selections;
    // selections.forEach((selection: any) => {
    //   labels.push(new SliceSelection(selection.x, selection.y, selection.slice_index, selection.width, selection.height));
    // });
    // this.labelSelections = labels;
  }
}
