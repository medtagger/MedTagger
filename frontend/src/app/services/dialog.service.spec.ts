import {ComponentFixture, inject, TestBed} from '@angular/core/testing';
import {
    MatDialogModule,
    MatDialogRef,
    MatFormFieldModule,
    MatInputModule
} from '@angular/material';
import {DialogService} from './dialog.service';
import {Component} from '@angular/core';
import {NoopAnimationsModule} from '@angular/platform-browser/animations';
import {InfoDialogComponent} from '../dialogs/info-dialog.component';
import {OverlayContainer} from '@angular/cdk/overlay';
import {BrowserDynamicTestingModule} from '@angular/platform-browser-dynamic/testing';
import {InputDialogComponent} from '../dialogs/input-dialog.component';
import {ReactiveFormsModule} from '@angular/forms';
import { TranslateService } from '@ngx-translate/core';
import { TranslateServiceStub } from '../mocks/TranslateServiceStub';

@Component({
    template: ''
})
class NoopComponent {
}

describe('Service: DialogService', () => {
    const DIALOG_EXAMPLE = {
        title: 'Example title',
        content: 'Example content',
        buttonText: 'Example button text',
        input: 'Example user input'
    };

    let noop: ComponentFixture<NoopComponent>;
    let overlayContainer: HTMLElement;

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [
                MatDialogModule,
                MatFormFieldModule,
                MatInputModule,
                NoopAnimationsModule,
                ReactiveFormsModule
            ],
            declarations: [NoopComponent, InfoDialogComponent, InputDialogComponent],
            providers: [
                DialogService,
                {
                    provide: OverlayContainer, useFactory: () => {
                        overlayContainer = document.createElement('div');
                        return {getContainerElement: () => overlayContainer};
                    }
                },
                {
                    provide: TranslateService,
                    useClass: TranslateServiceStub
                }
            ]
        });

        TestBed.overrideModule(BrowserDynamicTestingModule, {
            set: {
                entryComponents: [InfoDialogComponent, InputDialogComponent],
            }
        });

        TestBed.compileComponents();

        noop = TestBed.createComponent(NoopComponent);
    });

    it('shows info dialog', inject([DialogService],
        (service: DialogService) => {

            const dialog: MatDialogRef<any> = service.openInfoDialog(
                DIALOG_EXAMPLE.title,
                DIALOG_EXAMPLE.content,
                DIALOG_EXAMPLE.buttonText
            );

            noop.detectChanges();

            const title = overlayContainer.querySelector('#info-dialog-title');
            const content = overlayContainer.querySelector('#info-dialog-content');
            const button = overlayContainer.querySelector('#info-dialog-button');

            expect(title.textContent).toBe(DIALOG_EXAMPLE.title);
            expect(content.textContent).toBe(DIALOG_EXAMPLE.content);
            expect(button.textContent).toBe(DIALOG_EXAMPLE.buttonText);

            dialog.close();
        }
    ));

    it('shows input dialog', inject([DialogService],
        (service: DialogService) => {

            const dialog: MatDialogRef<any> = service.openInputDialog(
                DIALOG_EXAMPLE.title,
                DIALOG_EXAMPLE.content,
                DIALOG_EXAMPLE.input,
                DIALOG_EXAMPLE.buttonText
            );

            noop.detectChanges();

            const title = overlayContainer.querySelector('#input-dialog-title');
            const content = overlayContainer.querySelector('#input-dialog-content');
            const textarea: HTMLTextAreaElement = overlayContainer.querySelector('#input-dialog-textarea');
            const button = overlayContainer.querySelector('#input-dialog-button');

            expect(title.textContent).toBe(DIALOG_EXAMPLE.title);
            expect(content.textContent).toBe(DIALOG_EXAMPLE.content);
            expect(textarea.value).toBe(DIALOG_EXAMPLE.input);
            expect(button.textContent).toBe(DIALOG_EXAMPLE.buttonText);

            dialog.close();
        }
    ));

});
