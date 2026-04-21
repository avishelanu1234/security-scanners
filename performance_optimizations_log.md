# Note on Performance Optimizations

## Caching the Compiled Regex
- The regex for username validation is now compiled once and cached as a global variable `USERNAME_REGEX` to improve performance when validating user input.

## Maintaining a Single Database Connection
- A single database connection is now maintained within the `get_user_data` function, reducing the overhead of establishing a new connection for each call. This is done by checking if the connection already exists using a function attribute.
