# Test on GCP

## find which compute engine is free

- [official doc](https://cloud.google.com/free/docs/free-cloud-features#compute)

we will pick `Oregon: us-west1`, `us-west1-b`

## setup ssh config on ubuntu

[ref video](https://www.youtube.com/watch?v=4F9W4_JHYUo)

### 1. create your local host public key

```shell
ssh-keygen -C ubuntu
```

### 2. copy the public key value

```shell
cat ~/.ssh/id_rsa.pub
```

### 3. paste the public key value to the GCP console

### 4. edit `~/.ssh/config`

add following content to `~/.ssh/config`

```
# >>>>>> GCP >>>>>>

Host your-vm-name
  HostName your-vm-ip 
  User ubuntu
  Port 22
  IdentityFile ~/.ssh/id_rsa

# <<<<<< GCP <<<<<<
```

## check http is accessible

```shell
sudo apt update && sudo apt install -y apache2 && \
sudo systemctl status apache2 && \
echo '<!doctype html><html><body><h1>Sunacchi is alive on GCP VM!</h1></body></html>' | sudo tee /var/www/html/index.html
```

then check on your browser

```shell
http://your-vm-ip
```


