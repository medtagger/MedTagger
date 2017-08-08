import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-marker-page',
  templateUrl: './marker-page.component.html'
})
export class MarkerPageComponent implements OnInit {

  constructor() {
  }

  ngOnInit() {
    console.log('MarkerPage init');
  }

}
