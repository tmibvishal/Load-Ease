import redis

# Run redis on main server
# We can also use proper distributed database for better fault tolerance
rds = redis.Redis()
