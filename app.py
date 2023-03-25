from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
import subprocess
import paramiko
import socket


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/getMac', methods=['GET'])
def get_mac_address():
    ip_address = request.args.get('ip')
    cmd = f"arp -a {ip_address}"
    result = subprocess.check_output(cmd, shell=True)
    print(result)
    mac_address = result.decode().split()[3]
    return render_template("index.html", mac_address=mac_address)


#get ram status
@app.route('/ram/<ip_address>')
def ram_status(ip_address):
    # SSH connection details
    ssh_username = 'kali'
    ssh_password = 'kali'
    ssh_port = 22
    
    # Connect to remote device using SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, port=ssh_port, username=ssh_username, 
                    password=ssh_password)
    
    # Execute the `free` command on the remote device
    stdin, stdout, stderr = ssh.exec_command('free -h')
    
    # Parse the output of the `free` command
    output = stdout.read().decode('utf-8')
    lines = output.split('\n')
    mem_info = lines[1].split()
    total_mem = mem_info[1]
    used_mem = mem_info[2]
    free_mem = mem_info[3]
    
    # Close the SSH connection
    ssh.close()
    
    # Return the RAM status
    return render_template("index.html", total_mem=total_mem,used_mem=used_mem,
                        free_mem=free_mem)
    



#this is not working because the option to expose hardware-assisted virtualization features 
#to the guest operating system is not available for my virtual machine due to Hardware compatibility.
#or  software configuration for my virtual machine may not allow for the hardware-assisted 
#virtualization features to be exposed to the guest operating system. or Operating system compatibility 
@app.route('/temperature/<ip_address>')
def processor_temperature(ip_address):
    # SSH connection details
    ssh_username = 'kali'
    ssh_password = 'kali'
    ssh_port = 22
    
    # Connect to remote device using SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_address, port=ssh_port, username=ssh_username, password=ssh_password)
    
    # Execute the `sensors` command on the remote device
    stdin, stdout, stderr = ssh.exec_command('sensors')
    print(stdout)
    
    # Parse the output of the `sensors` command
    output = stdout.read().decode('utf-8')
  
    lines = output.split('\n')
    for line in lines:
        if line.startswith('Core 0:'):
            temperature = line.split()[2][1:]
            ssh.close()
            return render_template("index.html", temperature=temperature)
    
    # Close the SSH connection
    ssh.close()
    
    return 'Could not retrieve processor temperature'





if __name__ == '__main__':
    app.run(debug=True)
