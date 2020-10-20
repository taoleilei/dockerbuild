#! /usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   topology.py
@Time    :   2020/05/18 14:56:35
@Author  :   taoleilei 
@Version :   1.0
@Contact :   taoleilei6176@163.com
@License :   (C)Copyright 2019-2020
@Desc    :   None
'''

import sys
import docker

client = docker.DockerClient(base_url="tcp://192.168.119.134:2375")


def create():
    ipam_pool = docker.types.IPAMPool(
        subnet="10.0.28.0/24", gateway="10.0.28.254")
    ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
    try:
        net = client.networks.get("test-net", None)
        if net is None:
            net = client.networks.create("test-net", ipam=ipam_config, attachable=True, check_duplicate=True)
    except docker.errors.APIError as e:
        print(e.explanation)
        sys.exit(0)
    else:
        image = client.images.get("alpine:latest")
        for index in range(1, 3):
            client.containers.run(image, command="sleep 1d",
                                  detach=True, name="a%s" % index, network=net.name)


def remove():
    try:
        network = client.networks.get("test-net")
    except docker.errors.NotFound as e:
        print(e.explanation)
        sys.exit(0)
    else:
        containers_list = network.containers
        for container in containers_list:
            container.stop()
            container.remove()
        network.remove()

if __name__ == "__main__":
    # remove()
    create()
    #pass
