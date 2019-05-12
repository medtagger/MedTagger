import { SliceSelection } from '../../model/selections/SliceSelection';
import { ToolAction } from '../../model/ToolAction';
import { DrawingContext } from './DrawingContext';

export interface Tool<CustomSliceSelection extends SliceSelection> {

    setDrawingContext(drawingContext: DrawingContext): void;

    drawSelection(selection: CustomSliceSelection): any;

    onMouseDown(event: MouseEvent): void;

    onMouseMove(event: MouseEvent): void;

    onMouseUp(event: MouseEvent): void;

    getToolName(): string;

    getActions(): Array<ToolAction>;

    canChangeSlice(): boolean;

    reset(): void;
}
