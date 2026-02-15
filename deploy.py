import yaml
import asyncio
from server import run_server
import sys

def load_config():
    with open("config.yml", "r") as f:
        return yaml.safe_load(f)
    
async def deploy_service(service_name):
    config = load_config()
    
    service = config["services"].get(service_name)
    if not service:
        print(f"Service {service_name} not found in config.")
        return
    
    print(f"Deploying {service_name} on port {service['port']}...")

    await run_server(service["servicer_module"], service["servicer_class"], service["port"] )


def main():
    if len(sys.argv) != 2:
        print("Usage: python deploy.py <service-name>")
        print("\nAvailable services:")
        config = load_config()
        for svc_name, svc_config in config['services'].items():
            print(f"  - {svc_name}: {svc_config['name']} (port {svc_config['port']})")
        sys.exit(1)
    
    service_name = sys.argv[1]
    asyncio.run(deploy_service(service_name))


if __name__ == "__main__":
    main()