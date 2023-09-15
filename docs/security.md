# Security setup for SSH Script Dashboard

This document will list some options for securing your installation.

## Connect to the remote server

For *remote* and *remote-background* [execution models](environment.md), you will need to set up SSH keys. This guide assumes you have your remote server and its' scripts set up.

The default key location and name is *config/id-remote*, but this can be changed in the environment. A default key is already provided for testing purposes, but you shouldn't use it for any serious work - please regenerate it at your earliest convenience. You can do this in a variety of tools, here are the instructions for openssh's ssh-keygen. Place yourself in the directory, and type the following:

    ssh-keygen -f id-remote -C "ssh-script-dashboard"

Use empty passphrase. This command will re-create two files, *id-remote* (your private key) and *id-remote.pub* (your public key). Use ssh-copy-id to copy it to your remote server:

    ssh-copy-id -i id-remote remoteuser@remoteserver

Alternatively, you can manually add your public key on the remote server to the end of ~/.ssh/authorized_keys file.

authorized_keys file can be further secured with options that come in front of every public key line, such as "command=..." to restrict the login to run only certain [commands or scripts](commands.md), and "from=..." to restrict connections to only certain IP addresses or hostnames. See *man sshd* for more details.

## OpenID Connect

SSH Script Dashboard has been tested against Keycloak with OIDC, but any other OIDC solution should also work fine. Keycloak also comes as a docker image, and you can [set it up and test it](https://www.keycloak.org/getting-started/getting-started-docker) within minutes.

If your OIDC solution is integrated with your corporate login, using a shared realm, or public identity providers, you might not want to grant everyone access. Implementing further restrictions is required in that case.

And remember the rule of two - if your OIDC system is on http, this app should be as well. If it's on https, this app should be as well. Certificate trust must be established, or else there might be issues with authentication. This is typically not an issue if you're using commercial TLS certificates (or letsencrypt), but there could be issues with using internal CA. Included Dockerfile provides a sample CA bundle injection (commented out by default).

## Securing deployment and scalability

Ideally, if accessed by other people, this app should be exposed through a remote proxy, load balancer, kubernetes ingress or a similar technology. TLS should be implemented either on those, or on the app itself for complete end-to-end encryption.

If you followed these instructions or used the dockerfile, SSH Script Dashboard runs in a Flask development server. This should be sufficient for solo use, or very small deployments. If you wish to make it accessible to a large number of people, you should probably use a production WSGI server, such as gunicorn.

[Back to Readme](../README.md)