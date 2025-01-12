import docker

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
                "traefik.http.routers.dind.rule": f"HostRegexp(`{username}.dind.localhost:{{port:[0-9]+}}`)",
                "traefik.http.services.dind.loadbalancer.server.scheme": "http",
                "traefik.http.services.dind.loadbalancer.server.port": "{port}",
                "traefik.http.middlewares.dind-replacepathregex.replacepathregex.regex": "^/.*",
                "traefik.http.middlewares.dind-replacepathregex.replacepathregex.replacement": "/"
            },
            detach=True
        )
        print(f"Container '{container.name}' started with ID: {container.id}")
    except docker.errors.APIError as e:
        print(f"An error occurred: {e}")

def run_docker_compose(container_name, repo_name):
    client = docker.from_env()
    # container = client.containers.list()
    container = client.containers.get(container_name)
    command = f"git clone https://github.com/your/repo.git && \ cd repo && \ docker-compose up -d"
    exec_code, output = container.exec_run(command, detach=True)
    print(f"Code: {exec_code}")
    print("Output:", output.decode("utf-8"))

if __name__ == "__main__":
    NUM_CONTAINERS = 1
    username = input("Enter your username: ")
    run_container(NUM_CONTAINERS, "")
    run_docker_compose(f"dind-{NUM_CONTAINERS}", )