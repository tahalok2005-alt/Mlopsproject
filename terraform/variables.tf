variable "cluster_name" {
  description = "Name of the local kind cluster"
  type        = string
  default     = "wine-mlops"
}

variable "image" {
  description = "Local Docker image to load into the cluster"
  type        = string
  default     = "wine-api:local"
}
