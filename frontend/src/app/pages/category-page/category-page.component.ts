import {Component, OnInit} from '@angular/core';
import {MatSnackBar, MatIconRegistry} from '@angular/material';
import {DomSanitizer} from '@angular/platform-browser';

import {ScanService} from '../../services/scan.service';

@Component({
    selector: 'app-category-page',
    templateUrl: './category-page.component.html',
    providers: [ScanService],
    styleUrls: ['./category-page.component.scss']
})
export class CategoryPageComponent implements OnInit {

    categories = [];
    downloadingCategoriesInProgress = false;
    constructor(private iconRegistry: MatIconRegistry, private sanitizer: DomSanitizer, private scanService: ScanService,
                public snackBar: MatSnackBar) {
    }

    ngOnInit() {
      this.downloadingCategoriesInProgress = true;
        this.scanService.getAvailableCategories().then((categories) => {
            this.categories = categories;
            for (const category of categories) {
                this.iconRegistry.addSvgIcon(category.key, this.sanitizer.bypassSecurityTrustResourceUrl(category.imagePath));
            }
        }, () => {
            this.downloadingCategoriesInProgress = false;
            this.snackBar.open('There was an error while downloading categories', 'Close', {
                duration: 5000,
            });
        });
    }
}
