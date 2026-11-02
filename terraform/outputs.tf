output "cluster_name" {
  value = kind_cluster.this.name
}

output "kubectl_context" {
  value = "kind-${var.cluster_name}"
}
