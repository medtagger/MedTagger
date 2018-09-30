import {SliceSelection} from '../model/selections/SliceSelection';
import {LabelTag} from '../model/labels/LabelTag';

export class SelectionMock extends SliceSelection {
    constructor(sliceIndex: number,
                label_tool: string,
                label_tag: LabelTag) {
        super();

        this.sliceIndex = sliceIndex;
        this.label_tag = label_tag;
        this.label_tool = label_tool;

        this.pinned = false;
        this.hidden = false;
    }

    getAdditionalData(): Object {
        return {
            EXAMPLE_PARAM_1: 1337,
            EXAMPLE_PARAM_2: this.label_tool + this.label_tag.key,
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
            'tag': this.label_tag.key,
            'tool': this.label_tool
        };
    }
}
