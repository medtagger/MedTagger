import {ROISelection2D} from '../../model/ROISelection2D';
import {Selector} from './Selector';
import {EventEmitter} from "@angular/core";
import {SliceSelection} from "../../model/SliceSelection";

export class RectROISelector implements Selector<ROISelection2D> {
	readonly STYLE = {
		SELECTION_FONT_SIZE: 14,
		SELECTION_LINE_DENSITY: [6],
		CURRENT_SELECTION_COLOR: '#ff0000',
		OTHER_SELECTION_COLOR: '#256fde',
		ARCHIVED_SELECTION_COLOR: '#5f27e5'
	};

	selectedArea: ROISelection2D;
	selections: Map<number, ROISelection2D>;
	archivedSelections: Array<ROISelection2D>;
	canvasCtx: CanvasRenderingContext2D;
	protected currentSlice;
	protected mouseDrag = false;
	protected canvasPosition: ClientRect;
	canvasSize: { width: number, height: number };

	public stateChange: EventEmitter<number>;

	constructor(canvas: HTMLCanvasElement) {
		this.canvasCtx = canvas.getContext('2d');
		this.canvasSize = {
			width: canvas.width,
			height: canvas.height
		};
		this.selections = new Map<number, ROISelection2D>();
		this.archivedSelections = [];
		this.selectedArea = undefined;
		this.currentSlice = undefined;
		this.stateChange = new EventEmitter<number>();
	}

	public getStateChangeEmitter(): EventEmitter<number> {
		return this.stateChange;
	}

	public getSelections(): ROISelection2D[] {
		return Array.from(this.selections.values());
	}

	public formArchivedSelections(selectionMap: ROISelection2D[]): ROISelection2D[] {
		selectionMap.forEach((selection: ROISelection2D) => {
			selection.scaleToView(this.canvasSize.width, this.canvasSize.height);
			this.drawSelection(selection, this.STYLE.ARCHIVED_SELECTION_COLOR);
			console.log('RectROISelector | scaleToView selection: ', selection);
		});
		return selectionMap;
	}

	public drawPreviousSelections(): void {
		console.log('RectROISelector | drawPreviousSelections | selection: ', this.selections);
		this.selections.forEach((selection: ROISelection2D) => {
			let color: string;
			let isCurrent: boolean = (selection.sliceIndex === this.currentSlice);
			if (isCurrent) {
				color = this.STYLE.CURRENT_SELECTION_COLOR;
			} else {
				color = this.STYLE.OTHER_SELECTION_COLOR;
			}
			if((selection.pinned || isCurrent) && (!selection.hidden)) {
				this.drawSelection(selection, color);
			}
		});
		console.log('RectROISelector | drawPreviousSelections | archived: ', this.archivedSelections);
		//TODO: decide whether to draw archived selections or not
		// this.archivedSelections.forEach((selection: ROISelection2D) => {
		// 	this.drawSelection(selection, this.STYLE.ARCHIVED_SELECTION_COLOR);
		// });
	}

	public drawSelection(selection: ROISelection2D, color: string): void {
		console.log('RectROISelector | drawSelection | selection: ', selection);
		this.canvasCtx.strokeStyle = color;
		this.canvasCtx.setLineDash(this.STYLE.SELECTION_LINE_DENSITY);
		this.canvasCtx.strokeRect(selection.positionX, selection.positionY,
			selection.width, selection.height);

		const fontSize = this.STYLE.SELECTION_FONT_SIZE;
		this.canvasCtx.font = `${fontSize}px Arial`;
		this.canvasCtx.fillStyle = color;
		this.canvasCtx.fillText(selection.sliceIndex.toString(), selection.positionX + (fontSize / 4), selection.positionY + fontSize);
	}

	public onMouseDown(event: MouseEvent): void {
		console.log('RectROISelector | startMouseSelection | event: ', event);
		const selectionStartX = (event.clientX) - this.canvasPosition.left;
		const selectionStartY = (event.clientY) - this.canvasPosition.top;
		this.selectedArea = new ROISelection2D(selectionStartX, selectionStartY, this.currentSlice, this.canvasSize.width, this.canvasSize.height);
		this.selections.delete(this.currentSlice);
		this.mouseDrag = true;
	}

	public onMouseMove(mouseEvent: MouseEvent): void {
		if (this.mouseDrag && this.selectedArea) {
			console.log('RectROISelector | drawSelectionRectangle | onmousemove clienXY: ', mouseEvent.clientX, mouseEvent.clientY);
			this.updateSelection(mouseEvent);
			this.clearCanvasSelection();

			this.drawSelection(this.selectedArea, this.STYLE.CURRENT_SELECTION_COLOR);
		}
	}

	public updateSelection(event: MouseEvent): void {
		console.log('RectROISelector | updateSelection | event: ', event);

		if (this.selectedArea) {
			const newWidth = (event.clientX - this.canvasPosition.left) - this.selectedArea.positionX;
			const newHeight = (event.clientY - this.canvasPosition.top) - this.selectedArea.positionY;

			this.selectedArea.updateWidth(newWidth);
			this.selectedArea.updateHeight(newHeight);
		}
	}

	private checkSquareSelection(): boolean {
		return !!this.selectedArea && this.selectedArea.height != 0 && this.selectedArea.width != 0;
	}

	public onMouseUp(event: MouseEvent): void {
		if (this.mouseDrag) {
			this.mouseDrag = false;
			if (this.checkSquareSelection()) {
				this.addCurrentSelection();
			} else {
				this.clearSelectedArea();
				this.clearCanvasSelection();
			}
		}
	}

	public clearCanvasSelection(): void {
		console.log("RectROISelector | clearCanvasSelection");
		this.canvasCtx.clearRect(0, 0, this.canvasSize.width, this.canvasSize.height);
		this.drawPreviousSelections();
	}

	public clearData(): void {
		this.selectedArea = undefined;
		this.selections = new Map<number, ROISelection2D>();
		this.archivedSelections = [];
		this.stateChange = new EventEmitter<number>();
		this.clearCanvasSelection();
	}

	public addCurrentSelection(): void {
		if (this.selectedArea) {
			console.log("RectROISelector | addCurrentSelection");
			this.selections.set(this.currentSlice, this.selectedArea);
			this.stateChange.emit(this.currentSlice);
			this.clearSelectedArea();
		}
	}

	private clearSelectedArea() {
		this.selectedArea = undefined;
	}

	public updateCurrentSlice(currentSliceId: number): void {
		this.currentSlice = currentSliceId;
	}

	public updateCanvasPosition(canvasRect: ClientRect) {
		this.canvasPosition = canvasRect;
	}

	public hasArchivedSelections(): boolean {
		return this.archivedSelections.length > 0;
	}

	public hasValidSelection(): boolean {
		return this.selections.size >= 1;
	}

	public hasSliceSelection(): boolean {
		return !!this.selections.get(this.currentSlice) || !!this.selectedArea;
	}

	public archiveSelections(selectionMap?: Array<ROISelection2D>): void {
		if (!selectionMap) {
			selectionMap = Array.from(this.selections.values());
		}
		selectionMap.forEach((value: ROISelection2D) => {
			this.archivedSelections.push(value);
		});
	}

	public removeCurrentSelection(): void {
		if (this.hasSliceSelection()) {
			this.selections.delete(this.currentSlice);
			this.selectedArea = undefined;

			this.clearCanvasSelection();
		}
	}

	public clearSelections() {
		this.selections.clear();
	}

	public updateCanvasHeight(height: number): void {
		if (height && height > 0) {
			this.canvasSize.height = height;
		} else {
			console.warn('RectROISelector | updateCanvasHeight - non numeric/positive height provided', height);
		}
	}

	public updateCanvasWidth(width: number): void {
		if (width && width > 0) {
			this.canvasSize.width = width;
		} else {
			console.warn('RectROISelector | updateCanvasWidth - non numeric/positive width provided', width);
		}
	}

	public removeSelection(selectionId: number): void {
		if(selectionId == this.currentSlice) {
			this.removeCurrentSelection();
		} else {
			this.selections.delete(selectionId);
			this.clearCanvasSelection();
		}
	}

	public hideSelection(selectionId: number, newValue: boolean): void {
		let selection: SliceSelection = this.selections.get(selectionId);
		if(selection) {
			if (selection.hidden != newValue) {
				selection.hidden = newValue;
				this.redrawSelections();
			}
		} else {
			console.warn('RectROISelector | hideSelection | cannot hide non present selection!');
		}
	}

	public pinSelection(selectionId: number, newValue: boolean): void {
		let selection: SliceSelection = this.selections.get(selectionId);
		if(selection) {
			if (selection.pinned != newValue) {
				selection.pinned = newValue;
				this.redrawSelections();
			}
		} else {
			console.warn('RectROISelector | hideSelection | cannot pin non present selection!');
		}
	}

	private redrawSelections(): void {
		this.clearCanvasSelection();

		this.drawPreviousSelections();
	}
}
