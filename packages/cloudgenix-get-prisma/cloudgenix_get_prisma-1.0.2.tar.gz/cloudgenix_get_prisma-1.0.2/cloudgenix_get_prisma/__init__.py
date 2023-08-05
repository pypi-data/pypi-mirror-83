import os
import sys
import csv
import re
import argparse

SCRIPT_NAME = "Get Prisma Servicelinks"

try:
    import cloudgenix
except ImportError:
    print("ERROR: CloudGenix Python SDK required (try 'pip install cloudgenix')")
    sys.exit(1)

try:
    import cloudgenix_idname
except ImportError:
    print("ERROR: CloudGenix IDName module required (try 'pip install cloudgenix_idname')")
    sys.exit(1)

try:
    from tabulate import tabulate
except ImportError:
    print("ERROR: Tabulate Python module required (try 'pip install tabulate')")
    sys.exit(1)

# Try getting AUTH_TOKEN
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

# regex
remotenet_re = re.compile(r'Prisma Access info on Panorama:\n {2}Remote Onboarding: (.*)\n {2}IPSEC')


def servicelinks(sdk=None, idname_obj=None, controller="https://api.elcapitan.cloudgenix.com", ssl_verify=True,
                 output_csv=False):

    if sdk is None:
        # need to instantiate
        sdk = cloudgenix.API(controller=controller, ssl_verify=ssl_verify)

    if not sdk.tenant_id:
        # need to login.
        if AUTH_TOKEN is None:
            sdk.interactive.login()
        else:
            sdk.interactive.use_token(AUTH_TOKEN)

    # gen id_name maps
    if idname_obj is None:
        id2n_obj = cloudgenix_idname.CloudGenixIDName(sdk)
    else:
        id2n_obj = idname_obj

    id2n_obj.update_sites_cache()
    id2n = id2n_obj.generate_sites_map()

    id2n_obj.update_elements_cache()
    id2n.update(id2n_obj.generate_elements_map())
    element_id2site = id2n_obj.generate_elements_map(key_val='id', value_val='site_id')
    element_id2connected = id2n_obj.generate_elements_map(key_val='id', value_val='connected')
    # cloudgenix.jd(element_id2connected)
    id2n_obj.update_interfaces_cache()
    id2n.update(id2n_obj.generate_interfaces_map())

    prisma_servicelinks = []
    for interface in id2n_obj.interfaces_cache:
        tags = interface.get('tags', [])
        if isinstance(tags, list) and 'AUTO-PRISMA_MANAGED' in tags:
            prisma_servicelinks.append(interface)

    servicelink_status_list = []

    for sl in prisma_servicelinks:
        description = sl.get('description', '')
        prisma_rno_list = remotenet_re.findall(description if description is not None else "")
        if len(prisma_rno_list) >= 1:
            prisma_rno = ";".join(prisma_rno_list)
        else:
            prisma_rno = "Unknown"

        element_id = sl.get('element_id')
        site_id = element_id2site.get(element_id, "Could not get site")
        element_connected = element_id2connected.get(element_id, False)
        interface_id = sl.get('id')
        parent_if_id = sl.get('parent')
        admin_state = sl.get('admin_up')

        resp = sdk.get.interfaces_status(site_id, element_id, interface_id)
        if not element_connected:
            # if element is not connected, status is stale.
            operational_state = "Unknown_Offline"
            extended_state = "Unknown_Offline"
        elif resp.cgx_status:
            operational_state = resp.cgx_content.get("operational_state")
            extended_state = resp.cgx_content.get("extended_state")
        else:
            operational_state = "Unknown"
            extended_state = "Unknown"

        site_name = id2n.get(site_id, site_id)
        element_name = id2n.get(element_id, element_id)
        interface_name = id2n.get(interface_id, interface_id)
        parent_if_name = id2n.get(parent_if_id, parent_if_id)

        servicelink_status_list.append({
            "Site": site_name,
            "Element": element_name,
            "Interface": interface_name,
            "Element Online": "Online" if element_connected else "Offline",
            "Admin State": str(admin_state),
            "Operational State": operational_state,
            "Extended State": extended_state,
            "Prisma Remote On-boarding": prisma_rno,
            "Parent Interface": parent_if_name
        })

    return servicelink_status_list


def go():
    ############################################################################
    # Begin Script, start login / argument handling.
    ############################################################################

    # Parse arguments
    parser = argparse.ArgumentParser(description="{0}.".format(SCRIPT_NAME))

    # Allow Controller modification and debug level sets.
    controller_group = parser.add_argument_group('API', 'These options change how this program connects to the API.')
    controller_group.add_argument("--controller", "-C",
                                  help="Controller URI, ex. https://api.elcapitan.cloudgenix.com",
                                  default="https://api.elcapitan.cloudgenix.com")

    controller_group.add_argument("--insecure", "-I", help="Disable SSL certificate and hostname verification",
                                  dest='verify', action='store_false', default=True)

    output_group = parser.add_argument_group('Output', 'These options change how the output is generated.')
    output_group.add_argument("--csv-output-file", help="Output as CSV to this specified file name",
                              type=str, default=None)

    args = vars(parser.parse_args())

    servicelink_statuses = servicelinks(controller=args['controller'], ssl_verify=args['verify'])

    header = servicelink_statuses[0].keys()
    rows = [servicelink.values() for servicelink in servicelink_statuses]

    if args['csv_output_file'] is None:
        print(tabulate(rows, header))
    else:
        # write CSV

        with open(args['csv_output_file'], 'wt') as csvfile:
            csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
            csv_writer.writerow(header)  # write header
            csv_writer.writerows(rows)
    return


if __name__ == "__main__":
    # Get prisma
    go()

