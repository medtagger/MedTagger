Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.network "private_network", ip: "10.0.0.99"
  config.vm.network "forwarded_port", guest: 5432, host: 5432
  config.vm.provider "virtualbox" do |v|
    v.customize ["modifyvm", :id, "--memory", "3072"]
  end

  config.vm.provision "docker" do |d|
    config.vm.provision "shell", run: "always", path: "backend/initialize_machine.sh"
    config.vm.provision "shell", inline: "echo \"cd /vagrant/\" >> /home/vagrant/.bashrc"
  end
end
