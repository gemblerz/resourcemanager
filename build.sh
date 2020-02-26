#! /bin/bash

name=waggle/plugin-rm
version=0.1.0

docker build -t ${name}:${version} .
