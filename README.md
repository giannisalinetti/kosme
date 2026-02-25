# KOSME - KubeVirt OS Metadata Exporter

A utility for exporting KubeVirt Virtual Machine Instance (VMI) metadata from OpenShift Virtualization clusters.

## Description

KOSME scans your OpenShift/Kubernetes cluster for KubeVirt Virtual Machine Instances and exports detailed OS information in CSV or Markdown format. It retrieves guest OS details populated by the KubeVirt guest agent, including:

- Operating System name and version
- Kernel release information
- Guest agent connectivity status
- Namespace and VM name

## Features

- **Cluster-wide scanning**: Queries all VMIs across all namespaces
- **Guest OS info**: Retrieves OS details from KubeVirt guest agent metadata
- **Agent connectivity**: Checks agent connection status for each VM
- **Multiple export formats**: Supports CSV and Markdown output
- **Kubeconfig integration**: Uses local kubeconfig for cluster authentication

## Requirements

- Python 3.x
- Kubernetes Python client library
- KubeVirt guest agent installed on VMs (for full OS metadata)
- Valid kubeconfig configured for cluster access

## Usage

```bash
python kosme.py -f <format> -o <output_file>
```

### Arguments

- `-f, --format`: Export format (required)
  - `csv` - Comma-separated values format
  - `md` - Markdown table format
- `-o, --output`: Output file path (required)
  - Example: `report.csv` or `inventory.md`

### Examples

Export VMI metadata as CSV:
```bash
python kosme.py -f csv -o vmi_report.csv
```

Export VMI metadata as Markdown:
```bash
python kosme.py -f md -o vmi_inventory.md
```

## Output Columns

The exported data includes the following columns:

| Column | Description |
|--------|-------------|
| Namespace | Kubernetes namespace where the VMI resides |
| VM_Name | Name of the Virtual Machine Instance |
| OS_Name | Guest operating system name |
| OS_Version | Guest operating system version |
| Kernel | Kernel release information |
| Agent_Connected | KubeVirt guest agent connectivity status |

## Error Handling

- Validates kubeconfig connectivity before executing
- Handles KubeVirt API access errors gracefully
- Warns if output filename extension doesn't match the specified format
- Reports missing data as "N/A" when unavailable
