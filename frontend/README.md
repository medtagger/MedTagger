# Frontend

Repository contains Typescript+Angular 4 code building front side of the project. 

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 1.4.7.

## Project structure:

- `e2e`: End-to-End tests directory.
- `src`: Main project source dir
  - `app`: Main application source dir
    - `page`: Directory connected with single page (logic + presentation)
    - `components`: Components used in pages, feature components
    - `model`: Data classes used in project
    - `main`: Application definitions, app component
    - `services`: Injectable services and providers
  - `assets`: Page assets
  - `environments`: Env declarations
- `.angular-cli.json`: main project config file
- `.package.json`: dependencies config file also containing versioning, licensing and CLI-commands connected with project

Structure presented above is temporary. Watch out for updates.


## Setting up environment

### Requirements:

- NodeJS 6.10+ LTS [Download](https://nodejs.org/en/download)
- Angular CLI 1.2.7   
`npm install -g @angular/cli@1.4.7` (It will install CLI tool globally in 1.2.7 version.)

### Running project

- Clone this repository
- Go to root directory of repository (where `package.json` is located) and run `npm install`.  
 All of the project dependencies should fetched via npm. (this can take a while...)

- Run the dev server by `ng serve` command


## Development server

Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. In case you want to use custom host and port, use `--host` and `--port` flags.  
Example: `ng serve --host 0.0.0.0 --port 4201`   
The app will automatically reload if you change any of the source files.

## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `-prod` flag for a production build.

## Testing

### Running unit tests

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

### Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).
Before running the tests make sure you are serving the app via `ng serve`.

### Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).
