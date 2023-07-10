import redis
import sys

# Retrieve hostname, port, and password from command line arguments
if len(sys.argv) < 3 or len(sys.argv) > 4:
    print("Usage: python redis_get.py <hostname> <port> [password]")
    sys.exit(1)

redis_host = sys.argv[1]
redis_port = int(sys.argv[2])
redis_password = None

if len(sys.argv) == 4:
    redis_password = sys.argv[3]

try:
    # Connect to Redis server
    redis_client = redis.Redis(host=redis_host, port=redis_port, password=redis_password)

    # Retrieve the first 20 keys and their information
    keys = redis_client.keys()
    keys_info = {}

    for key in keys[:20]:
        key_type = redis_client.type(key).decode('utf-8')

        if key_type == 'string':
            value = redis_client.get(key).decode('utf-8')
            keys_info[key.decode('utf-8')] = {'type': key_type, 'value': value}

        elif key_type == 'list':
            value = redis_client.lrange(key, 0, -1)
            keys_info[key.decode('utf-8')] = {'type': key_type, 'value': value}

        elif key_type == 'hash':
            value = redis_client.hgetall(key)
            keys_info[key.decode('utf-8')] = {'type': key_type, 'value': value}

        elif key_type == 'set':
            value = redis_client.smembers(key)
            keys_info[key.decode('utf-8')] = {'type': key_type, 'value': value}

        elif key_type == 'zset':
            value = redis_client.zrange(key, 0, -1, withscores=True)
            keys_info[key.decode('utf-8')] = {'type': key_type, 'value': value}

    # Print the retrieved keys and their information
    for key, info in keys_info.items():
        print(f'Key: {key}')
        print(f'Type: {info["type"]}')
        print(f'Value: {info["value"]}')
        print('---')

    # Check writable directories using CONFIG SET dir
    writable_dirs = []
    test_dirs = ["/etc/", "/var/www/", "/var/www/html/", "/var/httpd/", "/root/.ssh/",
                 "/var/lib/redis/", "/opt/redis/", "/var/spool/cron/crontabs/"]

    for test_dir in test_dirs:
        try:
            with redis_client.pipeline() as pipe:
                pipe.config_set("dir", test_dir)
                pipe.execute()

                writable_dirs.append(test_dir)
        except (redis.exceptions.RedisError, redis.exceptions.ConnectionError) as e:
            print(f"Failed to test directory {test_dir}: {e}")

    # Reset CONFIG SET dir to original value
    try:
        redis_client.config_set("dir", "")
    except (redis.exceptions.RedisError, redis.exceptions.ConnectionError) as e:
        print(f"Failed to reset CONFIG SET dir: {e}")

    # Print writable directories
    if writable_dirs:
        print("Writable directories:")
        for dir_path in writable_dirs:
            print(dir_path)
    else:
        print("No writable directories found.")

except redis.exceptions.ConnectionError as e:
    print(f"Failed to connect to Redis server: {e}")
    sys.exit(1)
