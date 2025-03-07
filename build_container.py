import os
import subprocess

# Define file names
input_file = "dockerfile_template"
env_file = "envfile.txt"
output_file = "Dockerfile"

# Check if envfile.txt exists, exit if not found
if not os.path.exists(env_file):
    print(f"❌ Error: {env_file} not found. Please provide the file and try again.")
    sys.exit(1)

# Delete Dockerfile if it already exists
if os.path.exists(output_file):
    os.remove(output_file)
    print(f"🗑️ Deleted existing {output_file}")

# Read the original Dockerfile
with open(input_file, "r") as dockerfile:
    lines = dockerfile.readlines()

# Read the environment variables and add "ENV" in front of each variable
with open(env_file, "r") as envfile:
    env_lines = envfile.readlines()
    formatted_env_lines = [f"ENV {line.strip()}\n" for line in env_lines if line.strip()]  # Add "ENV" and remove empty lines

# Write the new Dockerfile
with open(output_file, "w") as new_dockerfile:
    for line in lines:
        new_dockerfile.write(line)
        if "#ENVHERE" in line:  # Append env variables after this line
            new_dockerfile.writelines(formatted_env_lines)

print("✅ Dockerfile updated successfully!")

# Run the podman-compose build command
try:
    print("🚀 Building and starting the container with podman-compose...")
    subprocess.run(["podman-compose", "-f", "podman-compose.yml", "up", "-d"], check=True)
    print("✅ Container built and started successfully!")
    # Delete Dockerfile after the container is built
    if os.path.exists(output_file):
        os.remove(output_file)
except subprocess.CalledProcessError as e:
    print("❌ Error: Failed to build and start the container.")
    print(e)
