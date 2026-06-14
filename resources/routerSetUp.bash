# test for internet ####################################

# Enable IP forwarding
#sudo sysctl -w net.ipv4.ip_forward=1

sudo ip addr add ip/24 dev eth0