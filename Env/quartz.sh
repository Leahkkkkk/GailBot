IP=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')

echo $IP

xhost + $IP

export IP=${IP}