# yakkity-govhack17
The API.AI bot, Kylie, built for the 2017 GovHack competition.

## Kylie - The Friendly Face of Government Services - Tourism Bot
### http://swiftartapp.com/kylietourism/

Meet Kylie. Kylie is the friendly front door to government data, delivering a wide range of information in an easy to use messaging interface. APA.AI is a conversation platform that’s able to deploy to many messaging platforms with the click of a button. Instead of government departments each maintaining their own collection of different messaging bots, they can all be serviced by Kylie.

## Services Used

We have relied on services provided by Google throughout this project. We have used API.AI to provide responses using the Google Assistant. This is deployed via *Actions on Google*. We have deployed our Google Assistant bot on Facebook, Twitter, Slack, and on the web. We have also tested our bot on the Google Home device. Our webhook is hosted on Google Cloud Storage. Our database is on Cloud SQL. Our Kylie server is hosted on a VM instance running on the Google Compute Engine. It's running Debian 8 "Jessie." The Cloud Storage, SQL, and Compute Engine are all available via the Google Cloud Platform, and API.AI and *Actions on Google* can be linked to the Cloud platform. 

## Code

__api_ai_agent/__

Folder contains the intents and entities used in our agent. These files can be placed in a Zip and *Restored* or *Imported* into API.AI. The files `agent.json`, `customDomainsResponses.json` and folders `entities`, `intents` should be at the top level of the Zip. 

__kylie_server/kylie.py__

Simple server to handle GET requests. It will query a database, and respond with JSON output. 
* Requires configuration of database host, database name, and the username and password to connect to it.

__kylie_server/kylie.service__

systemd unit file for running the Kylie server as a service. 
* More information: https://wiki.archlinux.org/index.php/systemd

__kylie_server/KylieDatabaseGovHack2017.sql__

Dump of the database queried by the Kylie server. 

__api_ai_webhook/index.js__

Webhook for connecting to the hosted Kylie server (kylie.py). 
Will send a GET request to the API provided by the server. 
This needs to be added as "Fulfillment" on API.AI.

* Requires configuration of the host and port variables, from which the Kylie server is available. 
* More information: https://api.ai/docs/getting-started/basic-fulfillment-conversation


## Commands

__Webhook__

Command to deploy the webhook to Google Storage. This relies on the [Google Cloud SDK](https://cloud.google.com/sdk/downloads). 
> gcloud beta functions deploy govhackWebhook --stage-bucket govhack2017 --trigger-http

Note: `deploy govhackWebhook` is a reference to `exports.govhackWebhook` in index.js. 



