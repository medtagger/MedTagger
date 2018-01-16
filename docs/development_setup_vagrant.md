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

### How set it up?

Once you've install your VirtualBox with Vagrant, it's time to clone this repository:

```bash
$ git clone git@github.com:jpowie01/MedTagger.git
```

Then you will be able to open it inside PyCharm and use Vagrant plugin to boot up your machine. To do this
 you can choose `Tools > Vagrant > Up` or use command `vagrant up` in the root directory of this repository. 

**Important:** It may take a while, because Vagrant needs to download box with Ubuntu image and then install
 all dependencies like Python and Docker with all needed containers.

Once Vagrant completed whole initialization try to SSH into the machine with `vagrant ssh` and make sure that
 you're inside `/vagrant` directory. 

### What's next?

Now, you can go further with development of the MedTagger. For more information, follow up with documentation
 inside of each projects:

 - [MedTagger Backend](/backend/docs/development_in_vagrant.md),
 - MedTagger Frontend - does not support setup with Vagrant yet.

