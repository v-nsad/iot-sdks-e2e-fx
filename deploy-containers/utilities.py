# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.
import subprocess
import os
import socket
import random
import string
from iothub_service_helper import IoTHubServiceHelper
from horton_settings import settings


def is_windows():
    return ("OS" in os.environ) and (os.environ["OS"] == "Windows_NT")

def is_pi():
    return (not is_windows()) and (run_shell_command("uname -m")[0] == "armv7l")


def sudo_prefix():
    if is_windows():
        return ""
    else:
        return "sudo -n "


def run_shell_command(cmd):
    cmd_with_prefix = sudo_prefix() + cmd
    print("running [{}]".format(cmd_with_prefix))
    try:
        return (
            subprocess.check_output(cmd_with_prefix.split(" "))
            .decode("utf-8")
            .splitlines()
        )
    except subprocess.CalledProcessError as e:
        print("Error spawning {}".format(e.cmd))
        print("Process returned {}".format(e.returncode))
        print("process output: {}".format(e.output))
        raise


def get_computer_name():
    if "COMPUTERNAME" in os.environ:
        return os.environ["COMPUTERNAME"]
    else:
        return socket.gethostname()


def get_random_device_name(extension=""):
    return (
        get_computer_name()
        + "_"
        + "".join(random.choice(string.ascii_uppercase) for _ in range(3))
        + "_"
        + str(random.randint(100, 999))
        + extension
    )


def get_cp_from_language(language):
    port_map = {
        "node": 8080,
        "c": 8082,
        "csharp": 80,
        "java": 8080,
        "pythonv2": 8080,
    }
    return port_map[language]


def get_language_from_image_name(image):
    if "default-friend-module" in image:
        return "node"
    languages = ["pythonv2", "java", "csharp", "node", "c"]
    for language in languages:
        if language + "-e2e" in image:
            return language
    raise Exception(
        "Error: could not determine language from image name {}".format(image)
    )


def set_args_from_image(obj, image):
    obj.language = get_language_from_image_name(image)
    obj.container_port = get_cp_from_language(obj.language)
    obj.adapter_address = "http://{}:{}".format("localhost", obj.host_port)
    obj.image = image


def remove_instance(settings_object):
    iothub_service_helper = IoTHubServiceHelper(settings.iothub.connection_string)

    if settings_object.device_id:
        iothub_service_helper.try_delete_device(settings_object.device_id)
        print(
            "Removed {} device with id {}".format(
                settings_object.name, settings_object.device_id
            )
        )

    settings.clear_object(settings_object)
    settings.save()


def try_remove_container(container_name):
    try:
        run_shell_command("docker stop {}".format(container_name))
    except subprocess.CalledProcessError:
        print("Ignoring failure")
    try:
        run_shell_command("docker rm {}".format(container_name))
    except subprocess.CalledProcessError:
        print("Ignoring failure")


def remove_old_instances():
    if not is_windows():
        try:
            run_shell_command("systemctl stop iotedge")
        except subprocess.CalledProcessError:
            print("Ignoring failure")

    if settings.test_module.container_name:
        try_remove_container(settings.test_module.container_name)

    remove_instance(settings.test_module)
    remove_instance(settings.friend_module)
    remove_instance(settings.iotedge)
    remove_instance(settings.test_device)
    remove_instance(settings.leaf_device)


def create_docker_container(obj):
    try_remove_container(obj.container_name)

    # hp_x = host port (port as seen by host OS)
    # cp_x = container port (port as exposed from app inside container)
    run_shell_command(
        "docker run -d -p {hp_1}:{cp_1} -p {hp_2}:{cp_2} -p {hp_3}:{cp_3} --name {name} --restart=on-failure:10 --cap-add NET_ADMIN --cap-add NET_RAW {image}".format(
            hp_1=obj.host_port,
            cp_1=obj.container_port,
            hp_2=obj.host_port + 100,
            cp_2=22,
            hp_3=8140,
            cp_3=8040,
            name=obj.container_name,
            image=obj.image,
        )
    )
