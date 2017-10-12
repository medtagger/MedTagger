import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-marker-page',
  templateUrl: './marker-page.component.html',
})
export class MarkerPageComponent implements OnInit {
  public currentImageNr: number;
  private imageBatch: string[];

  constructor() {
    this.currentImageNr = 0;
  }

  ngOnInit() {
    console.log('MarkerPage init');
  }

}
