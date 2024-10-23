# Run Sunacchi Web Server on GCP

for version < `1.0.0`, there are no docker deployment available. You can deploy the server on GCP by following the steps
below.

## Available VM Types

## Firewall Setup

### 1. create network firewall policy

#### create allowed `TCP` ports

i named the policy `nfwp-sunacchi-web-server`

```shell
80,8080,8888,3690,7777,9999,16888
```

example:
![firewall policy_example](https://hackmd.io/_uploads/HkcP-NLxJe.png)

### 2. associate created firewall to network interface

