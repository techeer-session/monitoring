import docker
import time

global NUM_CONTAINERS

def run_container(num_containers, username, service_name="grafana"):
    m = {"grafana": "3000", "prometheus": "9090"}
    port = m[service_name]
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
                f"traefik.http.routers.{username}.rule": f"HostRegexp(`{username}.localhost`)",
                f"traefik.http.services.{username}.loadbalancer.server.scheme": "http",
                f"traefik.http.services.{username}.loadbalancer.server.port": port,
                f"traefik.http.middlewares.{username}-replacepathregex.replacepathregex.regex": "^/.*",
                f"traefik.http.middlewares.{username}-replacepathregex.replacepathregex.replacement": "/"
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
    NUM_CONTAINERS = 2
    username = input("Enter your username: ")
    service_name = input("Enter the service name: ")
    run_container(NUM_CONTAINERS, username, service_name)
    run_docker_compose(f"dind-{NUM_CONTAINERS}", "monitoring", "https://github.com/techeer-session/monitoring")