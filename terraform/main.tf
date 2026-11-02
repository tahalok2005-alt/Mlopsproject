terraform {
  required_version = ">= 1.5"
  required_providers {
    kind = {
      source  = "tehcyx/kind"
      version = "~> 0.8"
    }
  }
}

provider "kind" {}

resource "kind_cluster" "this" {
  name           = var.cluster_name
  wait_for_ready = true
}

# kind nodes can't see images on the host, so the local build is copied in.
resource "terraform_data" "load_image" {
  triggers_replace = [kind_cluster.this.id, var.image]

  provisioner "local-exec" {
    command = "kind load docker-image ${var.image} --name ${var.cluster_name}"
  }
}

# Re-applies whenever a manifest changes.
resource "terraform_data" "deploy" {
  triggers_replace = [
    terraform_data.load_image.id,
    sha1(join("", [
      for f in sort(fileset("${path.module}/..", "{k8s,k8s-local,monitoring}/**")) :
      filesha1("${path.module}/../${f}")
    ])),
  ]

  provisioner "local-exec" {
    command = "kubectl --context kind-${var.cluster_name} apply -k ${path.module}/../k8s-local"
  }
}
