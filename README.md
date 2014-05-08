# Shred - slash commands for Slack

## Metro

`/metro` returns prediction times for upcoming trains at the Dupont Circle metro station.

## Weather

`/weather` returns current weather conditions and the upcoming weather within the next hour.

## Using Shred

Shred is built for Heroku.

Install requirements via [pip](https://pypi.python.org/pypi/pip):

    pip install -r requirements.txt

Run with [foreman](http://rubygems.org/gems/foreman):

    foreman start

## Configuration

Shred is configured via environment variables. All variables are required, unless otherwise noted.

### Slack

| ENV | Description |
|-----|-------------|
| MBTA_TOKEN | Slack token for the /mbta command integration |
| METRO_TOKEN | Slack token for the /metro command integration |
| TCAMP_TOKEN | Slack token for the /tcamp command integration |
| WEATHER_TOKEN | Slack token for the /weather command integration |

### External Services

| ENV | Description |
|-----|-------------|
| FORECASTIO_KEY | Forecast.io API key |
| WMATA_KEY | WMATA API key |


