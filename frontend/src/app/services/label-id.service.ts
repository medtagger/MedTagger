import {Injectable} from '@angular/core';

@Injectable()
export class LabelIdService {
    private idCounter: number;

    constructor() {
        this.resetIdCounter();
    }

    public getLastId(): number {
        return this.idCounter;
    }

    public getNextId(): number {
        return this.idCounter++;
    }

    public resetIdCounter(): void {
        this.idCounter = 0;
    }
}