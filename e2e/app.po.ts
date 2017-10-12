import { browser, by, element } from 'protractor';

export class TestAppPage {
  navigateTo() {
    return browser.get('/');
  }

  getParagraphText() {
    return element(by.css('main-root h1')).getText();
  }
}
