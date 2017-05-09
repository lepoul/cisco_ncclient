## cisco_ncclient

This is a simple NETCONF over SSHv2 client for the CISCO IOS. 
Only the edit-config RPC is provided, and get-config works with "show run" command over plain SSH.

## manager

The cisco_ncclient.manager class provides high level use of the client. 

## Uses

cisco_ncclient is used to develop the [push_config](https://github.com/lepoul/ansible_modules/tree/master/cisco_ios) Ansible module.

## TODO

- XML-based construction of the NETCONF messages, instead of strings
- Support more operations



