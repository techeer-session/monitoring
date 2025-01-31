provider "google" {
    credentials = file("central-bulwark-448318-g0-0ff77d3c79e2.json")
    project = "central-bulwark-448318-g0"
    region  = "us-central1"  
    zone    = "us-central1-c" 
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
    name   = "session-static-ip"
    region = "us-central1"
}


resource "google_compute_firewall" "main-ssh-icmp" {
    name    = "main-ssh-icmp"
    network = google_compute_network.vpc_network.name

    allow {
        protocol = "tcp"
        ports    = ["22", "80", "443", "8000", "7946", "3000", "9090"]  # SSH port
    }

    allow {
        protocol = "icmp"
    }

    source_ranges = ["0.0.0.0/0"]
    target_tags = ["main-firewall"]
}

# 백엔드 메인 서버 
resource "google_compute_instance" "vm_instance1" {
    name         = "session-instance2"
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
        startup-script = file("docker.sh")
    }
}
