### Cache for GET /accounts/{id}

Add a short-TTL cache to the response of the GET /accounts/{id} endpoint to improve performance and reduce load on the server. The cache should expire after a specified duration to ensure data freshness.

#### Implementation
- Use an in-memory store or a dedicated caching layer.
- Set appropriate cache headers in the response.
- Ensure cache invalidation on data updates.

### Example Response
```json
{
  "id": "123",
  "name": "John Doe",
  "balance": 1000,
  "cached_at": "2023-10-01T12:00:00Z"
}
```