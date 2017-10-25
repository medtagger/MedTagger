Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.provision "shell", path: "initialize_machine.sh"
  config.vm.network "private_network", ip: "10.0.0.99"
  config.vm.provider "virtualbox" do |v|
    v.customize ["modifyvm", :id, "--memory", "3072"]
  end
  config.vm.provision "docker" do |d|
#    d.pull_images "sequenceiq/hadoop-docker"
    d.pull_images "dajobe/hbase"
    d.pull_images "rabbitmq:management"
# TODO: Enable when needed!
#    d.run "sequenceiq/hadoop-docker",
#      args: "-p 0.0.0.0:50010:50010 \
#             -p 0.0.0.0:50020:50020 \
#             -p 0.0.0.0:50070:50070 \
#             -p 0.0.0.0:50075:50075 \
#             -p 0.0.0.0:50090:50090 \
#             -p 0.0.0.0:9000:9000 \
#             -p 0.0.0.0:10020:10020 \
#             -p 0.0.0.0:19888:19888 \
#             -p 0.0.0.0:8030:8030 \
#             -p 0.0.0.0:8031:8031 \
#             -p 0.0.0.0:8032:8032 \
#             -p 0.0.0.0:8033:8033 \
#             -p 0.0.0.0:8040:8040 \
#             -p 0.0.0.0:8042:8042 \
#             -p 0.0.0.0:8088:8088 \
#             -p 0.0.0.0:49707:49707 \
#             -p 0.0.0.0:2122:2122"
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
  end
end
