import { TestAppPage } from './app.po';

describe('test-main App', () => {
  let page: TestAppPage;

  beforeEach(() => {
    page = new TestAppPage();
  });

  it('should display welcome message', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('Welcome to main!');
  });
});
