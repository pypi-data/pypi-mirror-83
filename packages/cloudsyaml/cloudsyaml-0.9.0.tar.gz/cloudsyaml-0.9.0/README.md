# Simple library and CLI to explore the clouds.yaml

If you manage a big OpenStack cloud, you may find yourself in a situation with a lot of entries in your clouds.yaml file.
The problem is that you need to configure a separate cloud for each project.
Moreover, they multiplied by the count of regions in your deployment.
The `cloudsyaml` package, which provides simple `clouds` utility will simplify exploring such a yaml-based database.

## List configured clouds
```
$ clouds list
admin
octavia
octavia-testos
```

## Filter clouds by keywords
```
$ clouds list --grep octavia --grep testos
octavia-testos
```

## List configured clouds in format of export command for shell
```
$ clouds list --eval
export OS_CLOUD=admin
export OS_CLOUD=octavia
export OS_CLOUD=octavia-testos
```

## Get info about one cloud
```yaml
$ clouds show admin
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
$ clouds files
+-------------+--------------------------------------------------+
| name        | path                                             |
+-------------+--------------------------------------------------+
| clouds.yaml | /Users/igor.tiunov/.config/openstack/clouds.yaml |
| secure.yaml | /Users/igor.tiunov/.config/openstack/secure.yaml |
+-------------+--------------------------------------------------+
```
