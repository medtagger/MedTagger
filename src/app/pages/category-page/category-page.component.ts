import {Component, OnInit} from '@angular/core';
import {Router} from '@angular/router';
import {MatIconRegistry} from '@angular/material';
import {DomSanitizer} from '@angular/platform-browser';

@Component({
  selector: 'app-category-page',
  templateUrl: './category-page.component.html',
  styleUrls: ['./category-page.component.scss']
})
export class CategoryPageComponent implements OnInit {

  constructor(private routerService: Router, iconRegistry: MatIconRegistry, sanitizer: DomSanitizer) {
    iconRegistry.addSvgIcon('kidneys', sanitizer.bypassSecurityTrustResourceUrl('../../../assets/icon/kidneys_category_icon.svg'));
    iconRegistry.addSvgIcon('liver', sanitizer.bypassSecurityTrustResourceUrl('../../../assets/icon/liver_category_icon.svg'));
    iconRegistry.addSvgIcon('hearth', sanitizer.bypassSecurityTrustResourceUrl('../../../assets/icon/hearth_category_icon.svg'));
    iconRegistry.addSvgIcon('lungs', sanitizer.bypassSecurityTrustResourceUrl('../../../assets/icon/lungs_category_icon.svg'));
  }

  ngOnInit() {
  }
}
