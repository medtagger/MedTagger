Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.provision "shell", path: "initialize_machine.sh"
  config.vm.network "private_network", ip: "10.0.0.99"
  config.vm.network "forwarded_port", guest: 5432, host: 5432
end
