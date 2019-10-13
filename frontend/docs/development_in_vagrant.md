Running MedTagger Frontend with Vagrant
---------------------------------------

Here you can find more information about running MedTagger Frontend with Vagrant.

### Requirements 

Make sure that you've got [NodeJS 8](https://nodejs.org/en/download/releases/) installed with NPM.

Please follow the documentation about setting up Vagrant [here](/docs/development_setup_vagrant.md).
 
**Note:** Keep in mind that Frontend will no work properly without Backend. To set it up follow
 the instructions [here](/backend/docs/development_in_vagrant.md).

### How to run Frontend?

Sadly, NPM does not work inside of a Vagrant, so we need to run Frontend locally. It can be installed
 on any operating system with:
 
```bash
$ npm install
```

Then, run our frontend:

```bash
$ ng serve
```

And that's all! You should be able to see MedTagger UI on `http://localhost:4200`. 

### How to log in?

There is default account for development purposes:
 - email: `admin@medtagger`,
 - password: `medtagger`.
