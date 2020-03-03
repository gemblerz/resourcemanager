FROM waggle/plugin-base-light:0.1.0

ENV WAGGLE_PLUGIN_ID="999"

LABEL "waggle.volumes.docker"="/var/run/docker.sock" \
      "waggle.volumes.configuration"="/wagglerw/config"

WORKDIR /plugin

COPY requirements.txt .
RUN pip3 --no-cache-dir install -r requirements.txt

RUN pywaggle_loc=$(pip3 show waggle | grep Location | cut -d ':' -f 2 | tr -d ' ') \
  && sed -i 's|localhost|rabbitmq|g' ${pywaggle_loc}/waggle/plugin/__init__.py

COPY src/plugin.* /plugin/
COPY src/plugin/* /plugin/plugin-bin/
CMD ["python3", "-u", "/plugin/plugin-bin/resourcemanager.py"]]
#ENTRYPOINT ["python3", "resourcemanager.py", "--config_dir", "/wagglerw/config"]
