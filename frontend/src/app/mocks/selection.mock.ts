import { SliceSelection, SliceSelectionType } from '../model/selections/SliceSelection';
import { LabelTag } from '../model/labels/LabelTag';

export class SelectionMock extends SliceSelection {
    constructor(sliceIndex: number,
                labelTool: string,
                labelTag: LabelTag) {
        super(sliceIndex, labelTool, labelTag, SliceSelectionType.NORMAL);
    }

    getAdditionalData(): Object {
        return {
            EXAMPLE_PARAM_1: 1337,
            EXAMPLE_PARAM_2: this.labelTool + this.labelTag.key,
            EXAMPLE_PARAM_3: {
                EXAMPLE_PARAM_3_1: 'Example'
            }
        };
    }

    toJSON(): Object {
        return {
            'width': 1,
            'height': 1,
            'slice_index': this.sliceIndex,
            'tag': this.labelTag.key,
            'tool': this.labelTool
        };
    }
}
