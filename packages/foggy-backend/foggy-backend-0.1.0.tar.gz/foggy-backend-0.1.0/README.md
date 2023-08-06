# Foggy

Foggy keeps photos and videos shot with a smartphone in sync between devices. 
It does so without requiring a separate app to delete, update or add files. 
On an iPhone you will install the app and keep on using the built-in Photos
app to edit and sort your photos and videos. When space gets low on the device
you move the photos to an archive on the backend and clear the phone memory 
knowing that you have copies on the server.

The name foggy is a silly reference to fog as compared to cloud. Fog is
something that you can see and almost touch. A cloud is high up in the sky and
you have no idea what happens up there.

## Test it

At the moment Foggy is much a work in progress and requires more testing and 
development before it can be trusted as your only handler of photos and videos.
But you can try it out with your own server (mostly tested in Arch and Debian):

    python3 -m pip install --user foggy-backend
    
TODO: write more about how to do this since it's not yet on PYPI

After this you can build the Xcode-project from the `ios` folder and deploy it to
a simulator or physical device. The app should then connect to the server and you
should be able to sync the device with the server.


### Raspbian instruction

With a clean Raspbian installation here is what you do to get going. Login through
ssh or directly on the pi and add your user. E.g.:

    sudo useradd -m -G sudo mrfog
    sudo passwd mrfog

Logout and login with your new user. Run these commands to update and initiate the
system:

    sudo userdel pi
    sudo apt update ; sudo apt upgrade
    sudo apt install git
    
After that you can follow above instructions.


## Docker

In case you want to deploy your app with docker, here is an example 
`docker-compose.yaml` file:

    version: "3"
    services:
        backend:
            image: python:3.8
            container_name: foggy
            environment:
                PYTHONPATH: /foggy_backend
            command: python -m foggy
            ports:
                - 21210:21210
            logging:
                driver: journald
                options:
                    tag: "foggy"
            volumes:
                - ./backend:/backend
                - /etc/avahi/services/:/etc/avahi/services/

## Current limitations

Here are some limitations that needs to be taken into consideration:

- Use only one active backend server on the local network. There is no way to control
which backend is connected so you will not know which server gets connected.


# Developers documentation


## 1. Server and app connection

The connection between the server and the app is initiated with a 

## 2. Vendoring

There are two dependencies that have been vendored as compared to creating a
virtual environment or using system packages, see `backend/foggy/vendor`. The
reason for choosing this approach is a much simpler configuration. There is
really no need for docker or virtualenvs, just run it with `python -m...`.

## 3. Style and formatting

The code is formatted with *black* and linted with *pylint*.

Format all code with black:

    black  --target-version py38 --exclude 'vendor/*.?' rednas tests

## 4. Test packaging

    python3 setup.py sdist bdist_wheel
    python3 -m twine upload --repository testpypi dist/*