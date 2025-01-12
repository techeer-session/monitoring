import docker
import time

global NUM_CONTAINERS

def run_container(num_containers, username):
    client = docker.from_env()
    try:
        container = client.containers.run(
            image="docker:dind",
            name=f"dind-{num_containers}",
            # ports={
            #     "2375/tcp": 2375,
            # },
            privileged=True,
            # volumes={
            #     ".": {"bind": "/app", "mode": "rw"}
            # },
            network="dind-network",
            labels = {
                "traefik.enable": "true",
                "traefik.http.routers.dind.rule": "HostRegexp(`"+username+".dind.localhost:{port:[0-9]+}`)",
                "traefik.http.services.dind.loadbalancer.server.scheme": "http",
                # "traefik.http.services.dind.loadbalancer.server.port": "{port}",
                "traefik.http.middlewares.dind-replacepathregex.replacepathregex.regex": "^/.*",
                "traefik.http.middlewares.dind-replacepathregex.replacepathregex.replacement": "/"
            },
            detach=True
        )
        print(f"Container '{container.name}' started with ID: {container.id}")
    except docker.errors.APIError as e:
        print(f"An error occurred: {e}")

def run_docker_compose(container_name, repo_name, git_url):
    client = docker.from_env()
    container = client.containers.get(container_name)
    command1 = f"git clone {git_url}"
    exec_code = container.exec_run(command1, tty=True, privileged=True)
    print(f"Output: {exec_code.output.decode()}")
    time.sleep(5)
    exec3 = container.exec_run(f"docker-compose -f {repo_name}/docker-compose.yml up -d", tty=True, privileged=True)
    print(f"Output: {exec3.output.decode()}")

if __name__ == "__main__":
    NUM_CONTAINERS = 1
    username = input("Enter your username: ")
    run_container(NUM_CONTAINERS, username)
    run_docker_compose(f"dind-{NUM_CONTAINERS}", "monitoring", "https://github.com/techeer-session/monitoring")