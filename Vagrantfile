Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.network "private_network", ip: "10.0.0.99"
  config.vm.network "forwarded_port", guest: 5432, host: 5432
  config.vm.provider "virtualbox" do |v|
    v.customize ["modifyvm", :id, "--memory", "3072"]
  end

  config.vm.provision "docker" do |d|
    d.pull_images "dajobe/hbase"
    d.pull_images "rabbitmq:management"
    d.pull_images "postgres"
    d.run "dajobe/hbase",
      args: "-p 0.0.0.0:8080:8080 \
             -p 0.0.0.0:8085:8085 \
             -p 0.0.0.0:9090:9090 \
             -p 0.0.0.0:9095:9095 \
             -p 0.0.0.0:2181:2181 \
             -p 0.0.0.0:16010:16010"
    d.run "rabbitmq",
      args: "-p 0.0.0.0:4369:4369 \
             -p 0.0.0.0:5671:5671 \
             -p 0.0.0.0:5672:5672 \
             -p 0.0.0.0:15671:15671 \
             -p 0.0.0.0:15672:15672 \
             -p 0.0.0.0:25672:25672"
    d.run "postgres",
      args: "-p 0.0.0.0:5432:5432 \
             -e 'POSTGRES_DB=data_labeling' \
             -e 'POSTGRES_USER=backend_user' \
             -e 'POSTGRES_PASSWORD=DataLabelingAPI!'"
  config.vm.provision "shell", path: "initialize_machine.sh"
  end
end
