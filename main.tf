provider "google" {
    credentials = file("~/Documents/Hogwarts/techeerism-94823f84d155.json")
    project = "session-example2"
    region  = "us-central1"  
    zone    = "us-central1-c" 
}

variable "project_id" {
  type        = string
  description = "Google Cloud 프로젝트 ID"
}

variable "ssh_key" {
    type        = string
    description = "SSH public key"
}

resource "google_compute_network" "vpc_network" {
    name                    = "session-vpc-network"
    auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
    name          = "session-subnet"
    ip_cidr_range = "10.0.0.0/16"
    network       = google_compute_network.vpc_network.id
    region        = "us-central1"
}

resource "google_compute_address" "static_ip1" {
    name   = "hogwarts-main-static-ip"
    region = "us-central1"
}


resource "google_compute_firewall" "main-ssh-icmp" {
    name    = "main-ssh-icmp"
    network = google_compute_network.vpc_network.name

    allow {
        protocol = "tcp"
        ports    = ["22", "443", "2377", "7946"]  # SSH port
    }

    allow {
        protocol = "udp"
        ports = ["4789","7946"]
    }

    allow {
        protocol = "icmp"
    }

    source_ranges = ["0.0.0.0/0"]
    target_tags = ["main-firewall"]
}

# 백엔드 메인 서버 
resource "google_compute_instance" "vm_instance1" {
    name         = "hogwarts-main-instance"
    machine_type = "e2-medium"  # 2 vCPUs, 4GB memory
    zone         = "us-central1-c"
    allow_stopping_for_update = true

    boot_disk {
    initialize_params {
        image  = "ubuntu-os-cloud/ubuntu-2004-lts"
        size   = 25  # 25 GB disk size
        type   = "pd-balanced"
        }
    }

    network_interface {
        subnetwork = google_compute_subnetwork.subnet.id
        access_config {
            nat_ip = google_compute_address.static_ip1.address
        }
    }

    tags = ["http-server", "https-server", "main-firewall"]

    metadata = {
        ssh-keys = "ubuntu:${var.ssh_key}"
        startup-script = <<-EOF
            #!/bin/bash
            # Cloud SQL Proxy 설치
            wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
            chmod +x cloud_sql_proxy
            
            # Cloud SQL Proxy 실행
            ./cloud_sql_proxy -instances=${var.project_id}:us-central1:hogwarts-postgres-instance=tcp:5432 &

            # Docker 및 NestJS 설정 실행
            bash ~/Documents/Hogwarts/infra/docker.sh
        EOF
    }
}
