import { List } from 'immutable';
import { Point } from './Point';


/**
 * Class tasked with manipulating zoom levels and interaction
 * between user mouse and marker
 */
export class MarkerZoomHandler {
    private static readonly MOUSE_WHEEL_BUTTON_ID = 1;
    private dragActive: boolean;
    private currentZoomLevelIndex: number;
    private zoomLevels: List<number>;
    private dragPoint: Point;

    constructor() {
        this.dragActive = false;
        this.zoomLevels = List([1.0, 2.0, 4.0, 8.0]);
        this.currentZoomLevelIndex = 0;
        this.dragPoint = null;
    }

    public getZoomLevel(): number {
        return this.zoomLevels.get(this.currentZoomLevelIndex);
    }

    /**
     *  Incrementing zoom level and returning new value
     */
    public zoomIn(): number {
        return this.zoomLevels.get(++this.currentZoomLevelIndex);

    }

    /**
     *  Decrementing zoom level and returning new value
     */
    public zoomOut(): number {
        return this.zoomLevels.get(--this.currentZoomLevelIndex);
    }

    public zoomInAvailable(): boolean {
        return this.currentZoomLevelIndex < this.zoomLevels.size - 1;
    }

    public zoomOutAvailable(): boolean {
        return this.currentZoomLevelIndex > 0;
    }

    /**
     *  Handling mouse down key as a part of zoom operation
     *
     *  @param event - Plain js MouseEvent
     *  @param workspace - HTMLDivElement to zoom
     *  @returns Flag that indicates successfull zoom operation
     */
    public mouseDownHandler(event: MouseEvent, workspace: HTMLDivElement): boolean {
        if (event.button === MarkerZoomHandler.MOUSE_WHEEL_BUTTON_ID && this.zoomOutAvailable) {
            console.log('MarkerZoomHandler | mouseDownHandler | wheel button clicked');
            this.dragActive = true;
            this.dragPoint = new Point(event.clientX + workspace.scrollLeft, event.clientY + workspace.scrollTop);
        }

        return false;
    }

    /**
     *  Handling mouse move key as a part of zoom operation
     *
     *  @param event - Plain js MouseEvent
     *  @param workspace - HTMLDivElement to zoom
     *  @returns Flag that indicates successfull zoom operation
     */
    public mouseMoveHandler(event: MouseEvent, workspace: HTMLDivElement): boolean {
        if (this.dragActive) {
            console.log('MarkerZoomHandler | mouseMoveHandler | wheel button clicked');
            const changeX = this.dragPoint.x - event.clientX;
            const changeY = this.dragPoint.y - event.clientY;

            workspace.scrollLeft = changeX;
            workspace.scrollTop = changeY;
        }

        return false;
    }

    /**
     *  Handling mouse up key as a part of zoom operation
     *
     *  @param event - Plain js MouseEvent
     *  @param workspace - HTMLDivElement to zoom
     *  @returns Flag that indicates successfull zoom operation
     */
    public mouseUpHandler(event: MouseEvent, workspace: HTMLDivElement): boolean {
        let zoomChanged = false;

        if (this.dragActive && event.button === MarkerZoomHandler.MOUSE_WHEEL_BUTTON_ID) {
            console.log('MarkerZoomHandler | mouseUpHandler | wheel button clicked');

            zoomChanged = true;
            this.dragActive = false;
            this.dragPoint = null;
        }

        return zoomChanged;
    }
}
