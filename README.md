# CRAWNET

CRAWNET is a graph-based domain discovery tool by CRYXNET that helps you gather information
about domains and potential relationships with other actors.
With the power of graph databases, each node in the graph represents a domain and its attributes, such as DNS records, IP addresses, and services related to the IP.

## Installation

To install the project and its dependencies, follow these steps:

**Make sure you have docker installed!**

1. Clone the repository to your local machine:

```bash
git clone https://github.com/cryxnet/crawnet.git
```

2. Go to the directory

```bash
cd crawnet
```

3. Rename (to `.env`) and edit the [configuration file](/sample.env)

```bash
mv sample.env .env
&& sed -i 's/NEO4J_PASSWORD=CHANGEME/NEO4J_PASSWORD=your_password_here/' .env \
&& sed -i 's/FLASK_APP_URL=http:\/\/CHANGEME:5000/FLASK_APP_URL=http:\/\/your_machine_ip_or_localhost:5000/' .env \
&& sed -i 's/FLASK_DEBUG=1/FLASK_DEBUG=0/' .env
```

4. Start the docker stack

```bash
docker compose up
```

## Roadmap

-   [x] First Version Release
-   [ ] Threat Intelligence Data
-   [ ] Email Recon
-   [ ] Better UI/UX

## Intelligence Data

The Intelligence Service is using the following sources:

-   [Cert Fingerprint | CRT.SH](https://crt.sh/)
-   [IP Information | IPAPI.CO](https://ipapi.co/IPADDRESS/json/)
-   [Python | WHOIS](https://pypi.org/project/python-whois/)

## Disclaimer

YOUR USAGE OF THIS PROJECT CONSTITUTES YOUR AGREEMENT TO THE FOLLOWING TERMS:

    THE MISUSE OF THE DATA PROVIDED BY THIS PROJECT AND ITS MALWARES MAY LEAD TO CRIMINAL CHARGES AGAINST THE PERSONS CONCERNED.

    I DO NOT TAKE ANY RESPONSIBILITY FOR THE CASE. USE THIS PROJECT ONLY FOR RESEARCH PURPOSES, EDUCATIONAL PURPOSES & ETHICAL ONLY.

    CRAWNET is a project related to Computer Security and for Educational Purposes and not a project that promotes illegal activities.

    Don't use this Project for any illegal activities.

    If something happens, we do not take any liability.

    CRAWNET should be considered as a project for educational purposes.

## Author

Created by [cryxnet](https://cryxnet.com/)

If you find this project helpful, please give it a ⭐️ on GitHub to show your support.
I would also appreciate it if you shared it with others who might find it useful!
