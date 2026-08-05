The assignment involves creating a shipment events service: ingest carrier tracking events idempotently (using FastAPI + PostgreSQL) and provide accurate shipment timelines. You'll receive only carrier_events.csv — a file containing around 1,000 events, intentionally including duplicates and out-of-order batches. Designing the webhook payload, replay tooling, and environment will be up to you, and these aspects are part of the evaluation. The full brief is attached. Key details:
##Timebox: 4–6 hours of work. If you reach the time limit, stop and outline your next steps — a thoughtful, incomplete solution is better than an over-engineered one.
##Due: 2 days, before the interview.
##AI tools are encouraged. Since we work AI-first, include a brief note on how you utilized them (details are in the brief).
##The demo is the deliverable. Provide one documented command to launch the service and database. After replaying all events, every timeline should be accurate. Don't forget to include the one-page ADR specified in the brief.

The evaluation criteria are outlined in the brief—there are no hidden expectations. If your submission advances, the final step will be a 60-minute interview, including a live demo, design defense under scaled constraints, and a discussion about leadership.
