import { MarkerAction } from './MarkerAction';

export class PinMarkerAction extends MarkerAction {

    public pinned: boolean;

    public constructor(pinned: boolean) {
        super();
        this.pinned = pinned;
    }

    public execute(): void {
    }

    public revert(): void {
    }
}
