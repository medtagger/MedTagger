Development setup with Vagrant
------------------------------

Vagrant is the easiest way to prepare your dev environment. It will automatically create a VirtualBox virtual machine,
 which will have all of our dependencies inside of it.

**Important!** Vagrant setup requires at least 4GB RAM. For best overall experience we recommend using
 machine with 8GB RAM.

### Requirements 

Here is a list of things that you've got to install:

 - [VirtualBox](https://www.virtualbox.org),
 - [Vagrant](https://www.vagrantup.com).

### How to set it up?

Once you've installed your VirtualBox with Vagrant, it's time to clone this repository:

```bash
$ git clone git@github.com:medtagger/MedTagger.git
```

You can create virtual machine directly from command line or using Vagrant plugin inside of PyCharm:
- **Command line:**  Run `vagrant up` in the root directory of this repository,
- **PyCharm:** Open project in Pycharm and choose `Tools > Vagrant > Up`.

**Important:** It may take a while, because Vagrant needs to download box with Ubuntu image and then install
 all dependencies like Python and Docker with all needed containers.

Once Vagrant completed whole initialization try to SSH into the machine with `vagrant ssh`. Project files are located 
under `/vagrant` directory. 

### What's next?

Now, you can go further with development of the MedTagger. For more information, follow up with documentation
 inside of each projects:

 - [MedTagger Backend](/backend/docs/development_in_vagrant.md),
 - [MedTagger Frontend](/frontend/docs/development_in_vagrant.md).

