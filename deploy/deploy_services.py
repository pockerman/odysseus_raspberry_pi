from  pyinfra.operations import files

files.download(
    name="Download mqtt js",
    src="https://unpkg.com/mqtt@5.7.0/dist/mqtt.esm.js",
    dest="robot_control/libs/mqtt.js"
)