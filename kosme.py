import csv
import argparse
import sys
from kubernetes import client, config

def get_vmi_metadata(export_format, output_file):
    # Load local kubeconfig
    try:
        config.load_kube_config()
    except Exception as e:
        print(f"Kubeconfig error: {e}")
        sys.exit(1)

    custom_api = client.CustomObjectsApi()
    
    # KubeVirt API Details
    group = "kubevirt.io"
    version = "v1"
    plural = "virtualmachineinstances"
    
    data_list = []

    print(f"Scanning cluster for VMIs...")

    try:
        # Fetch all VMIs across all namespaces
        vmis = custom_api.list_cluster_custom_object(group, version, plural)
        
        for vmi in vmis.get('items', []):
            name = vmi['metadata']['name']
            namespace = vmi['metadata']['namespace']
            
            # Extract OS info from the .status field populated by Guest Agent
            status = vmi.get('status', {})
            guest_info = status.get('guestOSInfo', {})
            
            # Check for Agent connectivity via conditions
            conditions = status.get('conditions', [])
            agent_ready = any(c.get('type') == 'AgentConnected' and c.get('status') == 'True' for c in conditions)
            
            row = {
                "Namespace": namespace,
                "VM_Name": name,
                "OS_Name": guest_info.get("name", "N/A"),
                "OS_Version": guest_info.get("version", "N/A"),
                "Kernel": guest_info.get("kernelRelease", "N/A"),
                "Agent_Connected": "Connected" if agent_ready else "Disconnected"
            }
            data_list.append(row)

    except Exception as e:
        print(f"Error accessing KubeVirt API: {e}")
        sys.exit(1)

    if not data_list:
        print("No VMIs found.")
        return

    # Export Logic
    headers = ["Namespace", "VM_Name", "OS_Name", "OS_Version", "Kernel", "Agent_Connected"]

    if export_format == 'csv':
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data_list)
    
    elif export_format == 'md':
        with open(output_file, 'w') as f:
            f.write("# OpenShift Virtualization OS Report\n\n")
            f.write(f"| {' | '.join(headers)} |\n")
            f.write(f"| {' | '.join(['---'] * len(headers))} |\n")
            for row in data_list:
                f.write(f"| {' | '.join(str(row[h]) for h in headers)} |\n")

    print(f"Successfully exported {len(data_list)} records to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export KubeVirt VMI metadata.")
    
    parser.add_argument(
        "-f", "--format", 
        choices=['csv', 'md'], 
        required=True,
        help="Export format: 'csv' or 'md'"
    )
    
    parser.add_argument(
        "-o", "--output", 
        required=True,
        help="The name/path of the output file (e.g. report.csv or inventory.md)"
    )
    
    args = parser.parse_args()
    
    # Simple validation to ensure extension matches format
    if not args.output.lower().endswith(f".{args.format}"):
        print(f"Warning: Output filename '{args.output}' does not match format '{args.format}'.")

    get_vmi_metadata(args.format, args.output)
