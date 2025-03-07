# PODMAN Installation and execution of Realtime API Agents Demo
The project uses Alpine linux with NodeJS image for the podman container. The project was built on windows laptop so all instructions are for windows command prompt. If you are non-windows user, all these commands will work on Linux or Mac with minor alterations like folder path and addresses mentioned for setup. The code itself will not need any change.

Refer original repo for more app related documentation: https://github.com/openai/openai-realtime-agents.git

The code changes are done for deployment on Podman or Docker container

## Setups
### *Step 1: Clone the repo*
```
git clone https://github.com/kprobyte/openai-agent.git
```

### *Step 2: Install podman*
Podman is a daemonless, open-source tool designed to manage and run Open Container Initiative (OCI) containers and pods, making it an alternative to Docker.

https://podman.io/get-started

Podman will expect to install WSL. Once podman is downloaded and installed. Run the following commands.
Run this command to initiate the machine. It will download and setup the podman machine instance along with the Linux variant for WSL.
This is a one time process.
```
podman machine init
```
then,
```
podman machine start
```
Next time after a reboot you can just use these commands to podman machine start or stop.


### *Step 3: Install python and podman-compose*
Podman Compose is a tool that allows you to run docker-compose.yml files using Podman containers. It is an implementation of the Compose specification with a Podman backend. Unlike Docker, Podman operates without a daemon, directly executing commands. This makes it a rootless and daemon-less process model. Pip is a package installer for python.
If python is not already installed, please do install it by downloading from https://www.python.org/downloads/
```
pip install podman-compose
```
then add Script location to the Environment variable PATH
```
%USERPROFILE%\AppData\Roaming\Python\Python313\Scripts
```
Now, check if podman-compose is setup on the path and executable. Open a new terminal window and run the command.
```
podman-compose --version
```

### *Step 4: Generate API key*
Signup to OpenAi and generate a key to use. We are using the model gpt-4o-mini-realtime-preview-2024-12-17 for this project. This is a paid model and will not be accessible without cash balance. The model gpt-4o-realtime-preview-2024-12-17 has much better response but way more expensive than mini
```
The model can be changed in these files.
    openai-realtime-agents\src\app\api\session\route.ts
    openai-realtime-agents\src\app\lib\realtimeConnection.ts
```

Now get an OpenAi Key from 
https://platform.openai.com/settings/organization/api-keys

### *Step 5: Pass the key as environment variable*
Store the generated api key and save it in a file and name it envfile.txt
The variable name OPENAI_API_KEY should contain your api key value.
Create the envfile.txt file in the folder where you have your build_container.py file.
You can store all the environment variables that you want to share to the application in this file.

Content of **envfile.txt**
```
OPENAI_API_KEY=sk-THISISTHEKEYYOUGENERATEDFORYOURSELFATOPENAIQA
```
This OPENAI_API_KEY will added to docker file and will be available as an environment varialble for the application. The api_key will be used to generate a session for the app to interact with the browser. Refer route.ts

To see the environment variables set in you container use this command.
```
podman exec openai-agent env
```
env is a linux command. You can type any linux command after the container name, like, ls pwd etc

### *Step 6: Build the contaner*
Execute the python script build_container.py
The script creates a Dockerfile combining the Dockerfile.ori and envfile.txt.
The "podman-compose -f podman-compose.yml up -d" command is executed which builds a podman container using alpine image and then installs the dependencies for the NodeJS project. The dependencies are listed in the package*.json files within the project folder.
```
py build_container.py
```
After successful build the container will start and the application will be availabe on port 3000

### *Step 7: Open the app*
The application exposes port 3000 from the container and the NodeJS app listens to this port.
```
http://localhost:3000
```

At the end of successful execution, you should have to images generated.
```
REPOSITORY                   TAG         SIZE
localhost/openai-agent_app  latest      954 MB
docker.io/library/node      18-alpine   129 MB
```
Use the following command to view the images
```
podmain images
```

You can start/stop the container with following commands
```
podman start openai-agent
podman stop openai-agent
```
You can check if the agent is running by using this command
```
podman ps -a
```

## In case of a build failure
Check the Dockerfile without the extension for errors.
Update Dockerfile.ori and the Yaml file to make any changes you need.

You may want to delete the generated image for a fresh build. You dont have to delete the 18-alpine image. Only delete the latest image that was created. Usually the name will be <none>. On successful generation the repository name will be the <build foldername_app>
```
podman rmi -f <IMAGE ID>
```
