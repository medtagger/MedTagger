[app_hosts]
${app_host_ip} ansible_user=${default_user} ansible_ssh_private_key_file=${app_key_name} ansible_python_interpreter=/usr/bin/python3

[db_hosts]
${db_host_ip} ansible_user=${default_user} ansible_ssh_private_key_file=${db_key_name} ansible_python_interpreter=/usr/bin/python3

[db_hosts:vars]
ansible_ssh_common_args='\'-o ProxyCommand=\"ssh -i ${app_key_name} -W %h:%p ${default_user}@${app_host_ip}\"\''