Cloudgenix Get Prisma
---------------------

#### Requirements
* Active CloudGenix Account
* Python >=3.7 (may work on lower)
* Python modules:
    * cloudgenix >= 5.4.1b1 - <https://github.com/CloudGenix/sdk-python>
    * cloudgenix_idname >= 2.0.1 - <https://github.com/ebob9/cloudgenix-idname>
    * tabulate == 0.8.7 - <https://github.com/astanin/python-tabulate>

#### License
MIT

#### Installation:
* Via PIP: `pip install --upgrade cloudgenix_get_prisma`
* Via download: Clone/Download, and from the directory run `./get_prisma_servicelinks.py`

#### Usage:
To authenticate, set AUTH_TOKEN in an environment variable
```bash
export AUTH_TOKEN="<Your AUTH_TOKEN text here>"
```
Otherwise, script will prompt you for username/password or SAML2 login info and log in interactively.

Once authenticated, if no arguments - will print table:
```bash
edwards-mbp-pro:cloudgenix_get_prisma aaron$ get_prisma_servicelinks 

Site      Element          Interface                             Element Online    Admin State    Operational State    Extended State    Prisma Remote On-boarding      Parent Interface
--------  ---------------  ------------------------------------  ----------------  -------------  -------------------  ----------------  ---------------------------  ------------------
Branch 3  Branch 3 ION 3K  AUTO-PRISMA_IPSEC-Tunnel_us-west-1_1  Online            True           up                   tunnel_up         AUTO-CGX_ecmp-3                               1
Branch 3  Branch 3 ION 3K  AUTO-PRISMA_IPSEC-Tunnel_us-west-1_4  Online            True           up                   tunnel_up         AUTO-CGX_ecmp-3                               4
Branch 2  Branch 2 ION 3K  AUTO-PRISMA_IPSEC-Tunnel_us-east-1_1  Online            True           up                   tunnel_up         AUTO-CGX_ecmp-2                               1
Branch 2  Branch 2 ION 3K  AUTO-PRISMA_IPSEC-Tunnel_us-east-1_4  Online            True           up                   tunnel_up         AUTO-CGX_ecmp-2                               4
Branch 1  Branch 1 ION 3K  AUTO-PRISMA_IPSEC-Tunnel_us-east-1_1  Online            True           up                   tunnel_up         AUTO-CGX_remotenet-1                          1
edwards-mbp-pro:cloudgenix_get_prisma aaron$
```

Can also use `--csv-output-file` command line switch to save output as CSV.

Full options available when run with `--help`.

#### Version
Version  | Changes
-------  | --------
**1.0.2**| Marked Statuses "Unknwon_Offline" that are stale when devices are offline.
**1.0.1**| Initial Release.