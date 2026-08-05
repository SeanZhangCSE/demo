# README additions: examples and notes

## Examples

Create a shipment:

curl -X POST http://localhost:8000/shipments/ -H "Content-Type: application/json" -d '{"external_id":"S-123","status":"created"}'

Create an event with idempotency:

curl -X POST http://localhost:8000/shipments/<SHIPMENT_ID>/events -H "Content-Type: application/json" -d '{"event_type":"pickup","payload":{"loc":"wh"},"idempotency_key":"abc-123"}'

Query events (global):

curl -X GET 'http://localhost:8000/events?event_type=pickup&limit=50'

Notes:
- The service supports optional `idempotency_key` on events to avoid duplicates when re-sending the same event.
- Pagination uses limit/offset query params.
