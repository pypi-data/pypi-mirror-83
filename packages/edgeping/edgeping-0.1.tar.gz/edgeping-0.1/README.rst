edgeping
========

Implementation of https://docs.telemetry.mozilla.org/concepts/pipeline/http_edge_spec.html
for testing purpose.

The server will collect pings in memory, and you can call:

- **GET /pings** to get all the collected pings in a JSON payload
- **DELETE /pings** to delete the collected pings


