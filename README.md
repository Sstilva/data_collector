# Data collector app
## Quick overview
Application for scraping and parsing data from real estate seller's web platform. Using included JSON config file returns CSV file. 
## Installation guide
Download repository

```bash
git clone https://github.com/Sstilva/data_collector.git
```

Go into repo dir

```bash
cd data_collector
```

### Using Docker

Build Docker image

```bash
docker build -t repp:data_collector .
```

Run Docker container

```bash
docker run --name data_collector repp:data_collector
```

To extract collected data from container use

```bash
docker cp data_collector:/output/ .
```

### Using local environment

Install required packages

```bash
pip install -r requirements.txt
```

Run python app

```bash
python ./src/main.py
```

Collected data is located in `data_collector/output/` directory
