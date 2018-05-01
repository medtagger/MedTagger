import {ROISelection2D} from '../../model/ROISelection2D';
import {Selector} from './Selector';
import {EventEmitter} from "@angular/core";
import {SelectorBase} from "./SelectorBase";
import {SliceSelection} from "../../model/SliceSelection";

export class RectROISelector extends SelectorBase<ROISelection2D> {
	readonly STYLE = {
		SELECTION_FONT_SIZE: 14,
		SELECTION_LINE_DENSITY: [6],
		CURRENT_SELECTION_COLOR: '#ff0000',
		OTHER_SELECTION_COLOR: '#256fde',
		ARCHIVED_SELECTION_COLOR: '#5f27e5'
	};

	constructor(canvas: HTMLCanvasElement) {
		super();
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

	public redrawSelections(): void {
		this.clearCanvasSelection();

		this.drawPreviousSelections();
	}
}
