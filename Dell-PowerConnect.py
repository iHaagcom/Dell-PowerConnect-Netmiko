from netmiko import ConnectHandler
from netmiko import NetmikoTimeoutException
from paramiko.ssh_exception import SSHException
from paramiko.ssh_exception import AuthenticationException
import time
import datetime
from paramiko import SSHClient, BadAuthenticationType
from netmiko.dell import DellForce10SSH
from netmiko.dell import DellPowerConnectSSH
from netmiko import SSHDetect, ConnectHandler
import time
import datetime


##Dell PowerConnect
TNOW = datetime.datetime.now().replace(microsecond=0)
IP_LIST = open('DellPowerConnect_devices')
TNOW=TNOW.strftime("%d%b%Y")
for IP in IP_LIST:
    print ('\n #### Connecting to the Switch '+ IP.strip() + ' #### \n' )
    RTR = {
    'device_type': 'autodetect',
    'host':   IP,
    'username': 'root',
    'password': 'Password',
    }
    try:
        guesser = SSHDetect(**RTR)
        best_match = guesser.autodetect()
        print('Dell Device Detected is:', best_match)
        net_connect = ConnectHandler(**RTR)
    except NetmikoTimeoutException:
        print ('Device not reachable')
        continue
    except AuthenticationException:
        print ('Failed to Authenticate')
        continue
    except SSHException:
        print ("Make sure SSH is enabled in device.")
        continue

    print ('Initiating backup')
    IP=IP.strip()
    SAVE_FILE = open(IP +'_'+TNOW,'w')
    #net_connect = ConnectHandler(**RTR)
    net_connect.write_channel("en\n")
    net_connect.write_channel("Password\n")
    #net_connect.write_channel("config\n")
    #net_connect.write_channel(f'snmp-server contact "Testing User"\n')
    #net_connect.write_channel("exit\n")
    time.sleep(1)
    #output = net_connect.read_channel()
    net_connect.write_channel('terminal length 0\n')
    # write channel
    net_connect.write_channel('show running\n')
    time.sleep(2) # this is needed for the device to send response. Yoiu may adjust timing depending on your end device
    output = net_connect.read_channel()
    #if '--More-- or (q)uit' in output:
    #        net_connect.write_channel('dell\r\n')
    #        time.sleep(1)
    #        output = net_connect.read_channel()
    SAVE_FILE.write(output)
    SAVE_FILE.close
    print(output)
    net_connect.disconnect()
