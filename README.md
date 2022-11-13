<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/cryxnet/crawnet">
    <img src="docs/assets/logo.png" alt="Logo">
  </a>

  <h1 align="center">CRAWNET</h1>

  <p align="center">
     Graph based domain discovery toolkit
    <br />
    <a href="https://github.com/cryxnet/crawnet"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/cryxnet/crawnet/issues">Report Bug</a>
    ·
    <a href="https://github.com/cryxnet/crawnet/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#conclusion-&-reflection">Conclusion & Reflection</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

CRAWNET is a graph based domain discovery tool to gather information about domains and potential relationships with other actors.
With help of Graph Databases each node represents a domain and their attributes like records, ips, services related with the ip and much more.
This tool should be used for ethical and educational purposes only.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Screenshots

![Screenshot](/docs/assets/screenshots/screenshot1.png)
![Screenshot](/docs/assets/screenshots/screenshot2.png)
![Screenshot](/docs/assets/screenshots/screenshot3.png)

### Built With

- [Neo4j](https://neo4j.com)
- [Python](https://www.python.org/)
- [IPIFY](https://www.ipify.org/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

1. `git clone https://github.com/cryxnet/crawnet.git`
2. `cd crawnet`
3. `python src/main.py`
4. Enter a Menu Number
5. Follow the instructions
6. If `Done!` is in the output without any errors exists the query was run successfully
7. Go to Neo4j Desktop and run the query `MATCH (n) RETURN n` to see all datas and relationships

### Prerequisites

- Neo4j Database
- Python 3.x

### Installation

1. Install Python Packages

```sh
pip install python-dotenv
pip install requests
pip install neo4j
pip install json
pip install python-whois
pip install dnspython
```

2. Install Neo4j Database
3. Create a .env file and configure the file with the corresponding [variables](#env-variables)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [ ] More nodes => divisions from the current one
- [ ] More detailed informations
- [ ] Full port scanning process
- [ ] Service Recognition
- [ ] OS Recognition
- [ ] Web based graph format

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Conclusion & Reflection

I have oriented myself to the Investigation Tool Maltego. I find it exciting how you can store data in a graph database. Normally you would store it in simple collons and reference the specific collons. However, with graph databases like neo4j, you can connect data using links to show connections between components. I also find it exciting how this technology can be implemented in cybersecurity. You can program much better investigation and information gathering tools and display data with relationships easier. I find the whole graph databases very interesting and will continue this project. See [Roadmap](#roadmap).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the Apache 2.0 License. See [`LICENSE`](LICENSE) for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Env Variables

| Name        | Description                   |
| ----------- | ----------------------------- |
| DB_URI      | URI for DB connection         |
| DB_USER     | Username of the db            |
| DB_PASSWORD | Password of the provided user |
