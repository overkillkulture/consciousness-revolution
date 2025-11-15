# 🌩️ Cyclotron Cloud - 24/7 Brain Sync Service

Runs 24/7 even when your laptop is closed.

## 🚀 One-Click Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

Click the button above to deploy to Render in one click.

## Features

- ✅ Runs 24/7 in the cloud (survives laptop closing)
- ✅ RSS feeds for brain updates
- ✅ Zapier webhook integration
- ✅ Dropbox auto-sync
- ✅ Airtable backup
- ✅ REST API for querying brain state

## Endpoints

After deployment, your service will be available at `https://your-app.onrender.com`:

- `GET /api/brain` - Get complete brain state
- `GET /api/active-projects` - Get active projects only
- `GET /api/health` - Health check
- `GET /rss/brain-updates.xml` - RSS feed of brain updates
- `POST /webhook/brain-update` - Receive updates from Zapier/IFTTT
- `POST /webhook/zapier-trigger` - Trigger Zapier automations
- `GET /cron/sync-to-zapier` - Auto-sync to Zapier (runs every 5 min)

## Environment Variables

After deploying, set these in Render dashboard:

- `DROPBOX_ACCESS_TOKEN` - Get from https://www.dropbox.com/developers/apps
- `ZAPIER_WEBHOOK_URL` - Get from Zapier webhook trigger
- `AIRTABLE_API_KEY` - Get from Airtable account settings
- `AIRTABLE_BASE_ID` - Your Airtable base ID

## Cost

**FREE** - Render free tier includes 750 hours/month (enough for 24/7 operation)

## Documentation

See `CYCLOTRON_TRULY_AUTOMATIC_GUIDE.md` for complete documentation including:
- Zapier automation examples
- RSS feed setup
- API usage
- Troubleshooting
