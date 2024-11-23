## Holiday Planner

### During API development, my thought process is structured around creating an efficient, robust, and user-friendly system. Here's a breakdown of the stages involved:

1. Identify the API's Goal: I start by understanding the problem the API is meant to solve and define its core functionality, ensuring it aligns with the intended users' needs.
2. Set up the Docker and Django infrastructure.
3. Designing data models.
4  Design Endpoints: I then define the specific endpoints and their routes. These should be intuitive and RESTful, following best practices in API design.
5. Read through the library documentation and connect to the third api library.
6. Implement caching mechanism for effiency.
7. Error Handling: I include clear and informative error messages for common failure scenarios (e.g., 400 for bad requests, 404 for not found).
8. Testing


### Limitations:
1. I did not have prefined data for the destinations so we have to manually insert the latitude, longtitude and location name.
2. No Implementation for Authentication and Authorization.
3. No support for preference, the user does not have access to detailed weather forecast only to the temperature.
4. No rate limiting.
6. Cache limitation, we only cache for 1 hour. The user may not see the any change to the temperature until an hour lapses.
7. Dependency on redis to be readly available.
8. Dependency on third-party library.


### Known Bugs:

1. Rate Limiting Issues: Sometimes rate limiting doesn't work as expected, leading to either too strict or too lenient throttling, which can affect performance and reliability.

2. Edge Case Failures: Rare inputs or interactions (e.g., malformed data, unexpected API calls) can sometimes result in unpredictable behavior.

### Wishlist for Improvement:

1. Better Rate Limiting Control: More flexible and intelligent rate-limiting to handle various use cases without sacrificing performance or security.

2. GraphQL Support: Incorporating GraphQL into the system to allow clients to query exactly the data they need, improving efficiency in data retrieval.

3. Self-Healing Features: Automated systems to detect and resolve common issues (e.g., memory leaks, deadlocks, or database bottlenecks) to improve reliability.

4. Advanced Analytics: Providing built-in analytics to monitor API usage, detect patterns, and optimize based on real-time feedback.

5. Automatic Scaling: Dynamic scaling options that can automatically adjust resources based on API traffic without manual intervention.

### How to start up the application:

1. Open your preferred CMD terminal.
2. Navigate into the root directory of the project that you have downloaded from git.
3. Once you are in the project directory, run command ***docker compose build*** to build the containers.
4. Once the previous command has successfully ran, run command ***docker compose up -d*** to start the docket containers.

### Manually add destinations
Once the application is up and running locally, please use the following endpoint ***GET /api/destinations/*** to manually add destinations.

To get the temperature for the location, use the following endpoint ***GET /api/destinations/{pk}/weather/*** use the primary key from the destination table.
