# Predictive-Airport-Signage

Proof of concept application which gets incoming arrivals at airports and predicts the most appropriate signage to display based on the nationality of arrivals, distance from gate and more.

## General Requirements (Most to least important)

- Retrieve and store incoming arrivals data for airpots
- Predict the likely nationalities of passengers and by association sign language
- Provide a REST API to provide access to the data
- Provide a basic webpage to view data from the API (Mock sign)
- Build and deploy the application as a container
- Provide a WebSocket for ongoing updates to the signage data
- Retrieve and provide data on estimated number of passengers (possibly from plane type)
- Update information based on passenger travel times from landing to departure hall (could include walking distance, delays for immigration and baggage relclaim)
