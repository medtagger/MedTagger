import {Component, OnInit} from '@angular/core';
import {MatSnackBar, MatIconRegistry} from '@angular/material';
import {DomSanitizer} from '@angular/platform-browser';

import {ScanService} from "../../services/scan.service";

@Component({
  selector: 'app-category-page',
  templateUrl: './category-page.component.html',
  providers: [ScanService],
  styleUrls: ['./category-page.component.scss']
})
export class CategoryPageComponent implements OnInit {

  categories = [];

  constructor(private iconRegistry: MatIconRegistry, private sanitizer: DomSanitizer, private scanService: ScanService,
              public snackBar: MatSnackBar) {
  }

  ngOnInit() {
    this.scanService.getAvailableCategories().then((categories) => {
      this.categories = categories;
      console.log(categories);
      for (let category of categories) {
        this.iconRegistry.addSvgIcon(category.key, this.sanitizer.bypassSecurityTrustResourceUrl(category.imagePath));
      }
    }, () => {
      this.snackBar.open("Błąd podczas pobierania kategorii", "Zamknij", {
        duration: 5000,
      });
    });
  }
}
