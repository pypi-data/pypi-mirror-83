# DBKS - a Databricks CLI

## Environment variables
- DBC_HOST
- DBC_TOKEN

## Cluster definition YAML example
```yaml
---
cluster-1:
    cluster_name: cluster-1
    spark_version: 6.6.x-scala2.11
    node_type_id: c4.2xlarge
    driver_node_type_id: i3.xlarge
    autoscale:
        min_workers: 1
        max_workers: 8
    ...

cluster-2:
    cluster_name: cluster-2
    ...
```

## Cluster access control list YAML example
```yaml
---
cluster-1:
- user_name: jsmith@example.com
  permission_level: CAN_RESTART
- user_name: jcitizen@example.com
  permission_level: CAN_MANAGE
...

cluster-2:
- user_name: jdoe@example.com
  permission_level: CAN_RESTART
- user_name: jwhite@example.com
  permission_level: CAN_MANAGE
```

## Directory/Notebook access control list YAML example
```yaml
---
/path/to/object:
- user_name: user1@example.com
  permission_level: CAN_READ
- user_name: user2@example.com
  permission_level: CAN_RUN
- user_name: user3@example.com
  permission_level: CAN_EDIT
- user_name: user4@example.com
  permission_level: CAN_MANAGE
```
