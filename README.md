# PODMAN Installation and execution of Realtime API Agents Demo
The project uses Alpine linux with NodeJS image for the podman container. The project was built on windows laptop so all instructions are for windows command prompt. If you are non-windows user, all these commands will work on Linux or Mac with minor alterations like folder path and addresses mentioned for setup. The code itself will not need any change.
```
Original repo for more app related documentation:
https://github.com/openai/openai-realtime-agents.git
```
The code changes are done for deployment on Podman or Docker container

## Setups
### *Step 1: Clone the repo*
```git clone https://github.com/kprobyte/openai-agent.git```

### *Step 2: Install podman*
Podman is a daemonless, open-source tool designed to manage and run Open Container Initiative (OCI) containers and pods, making it an alternative to Docker.
```https://podman.io/get-started```

### *Step 3: Install python and podman-compose*
pip install podman-compose
add “%USERPROFILE%\AppData\Roaming\Python\Python313\Scripts” to PATH
```https://www.python.org/downloads/```

### *Step 4: Generate API key*
Signup to OpenAi and generate a key to use. We are using the model gpt-4o-mini-realtime-preview-2024-12-17 for this project. It can be changed in these files
    openai-realtime-agents\src\app\api\session\route.ts
    openai-realtime-agents\src\app\lib\realtimeConnection.ts

```https://platform.openai.com/settings/organization/api-keys```

### *Step 5: Pass the key as environment variable*
Store the generated api key and save it in a file and name it envfile.txt
The variable name OPENAI_API_KEY should contain your api key value.
Create the envfile.txt file in the folder where you have your build_container batch file and save the key in it.

Content of envfile.txt
```
OPENAI_API_KEY=sk-THISISTHEKEYYOUGENERATEDFORYOURSELFATOPENAIQA
```
This OPENAI_API_KEY will added to docker file and will be available as an environment varialble for the application. The api_key will be used to generate a session for the app to interact with the browser. Refer route.ts

### *Step 6: Build the contaner*
Execute the python script build_container.py
The script creates a Dockerfile combining the Dockerfile.ori and envfile.txt.
The "podman-compose -f podman-compose.yml up -d" command is executed which builds a podman container using alpine image and then installs the dependencies for the NodeJS project. The dependencies are listed in the package*.json files within the project folder.
```py build_container.py```
After successful build the container will start and the application will be availabe on port 3000

### *Step 7: Open the app*
The application exposes port 3000 from the container and the NodeJS app listens to this port.
```http://localhost:3000```

At the end of successful execution, you should have to images generated.
REPOSITORY                   TAG         SIZE
localhost/openai-agent_app  latest      954 MB
docker.io/library/node       18-alpine   129 MB

Use the following command to view the images
```podmain images```

You can start/stop the container with following commands
```
podman start openai-agent
podman stop openai-agent
```

## In case of a build failure
Check the Dockerfile without the extension for errors.
Update Dockerfile.ori and the Yaml file to make any changes you need.

You may want to delete the generated image for a fresh build. You dont have to delete the 18-alpine image. Only delete the latest image that was created. Usually the name will be <none>. On successful generation the repository name will be the <build foldername_app>
```
podman rmi -f <IMAGE ID>
```
