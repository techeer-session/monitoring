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
                "traefik.http.services.dind.loadbalancer.server.port": "80",
                "traefik.http.middlewares.dind-replacepathregex.replacepathregex.regex": "^/.*",
                "traefik.http.middlewares.dind-replacepathregex.replacepathregex.replacement": "/"
            },
            detach=True
        )
        print(f"Container '{container.name}' started with ID: {container.id}")
    except docker.errors.APIError as e:
        print(f"An error occurred: {e}")

def run_docker_compose():
    client = docker.from_env()
    container = client.containers.list()
    for i in container:
        print(i.name)

if __name__ == "__main__":
    NUM_CONTAINERS = 1
    username = input("Enter your username: ")
    run_container(NUM_CONTAINERS, username)
    run_docker_compose()