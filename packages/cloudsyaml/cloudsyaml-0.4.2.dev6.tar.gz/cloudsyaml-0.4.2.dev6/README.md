# Simple library and CLI for explore the clouds.yaml

## List configured clouds
```
clouds list
admin
octavia
octavia-testos
```

## Get info about one cloud
```yaml
#clouds show admin
admin:
  auth:
    auth_url: https://cloud.example.com:5000
    password: '******'
    project_domain_name: Default
    project_name: admin
    user_domain_name: Default
    username: admin
  identity_api_verion: '3'
  region_name: SPB
```

## List configuration files used by SDK
```
clouds files
+-------------+--------------------------------------------------+
| name        | path                                             |
+-------------+--------------------------------------------------+
| clouds.yaml | /Users/igor.tiunov/.config/openstack/clouds.yaml |
+-------------+--------------------------------------------------+
```


## List configured clouds in format of export command for shell
```
clouds list --eval
export OS_CLOUD=admin
export OS_CLOUD=octavia
export OS_CLOUD=octavia-testos
```
