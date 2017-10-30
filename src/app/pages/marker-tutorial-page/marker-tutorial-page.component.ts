import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators, FormGroup } from "@angular/forms";


@Component({
  selector: 'marker-tutorial-page',
  templateUrl: './marker-tutorial-page.component.html',
  styleUrls: ['./marker-tutorial-page.component.scss']
})
export class MarkerTutorialPageComponent implements OnInit {

  formGroup: FormGroup;

  constructor(private _formBuilder: FormBuilder) { }

  ngOnInit() {
    this.formGroup = this._formBuilder.group({});
  }

}
