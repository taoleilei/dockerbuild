#### back
1. docker-compose -f docker-compose.yaml up -d
2. docker-compose -f docker-compose-slave.yaml up -d
3. docker-compose -f docker-compose-lb.yml up -d
4. docker-compose -f docker-compose-redis.yml up -d

#### front
##### 主服务执行docker-compose up -d
##### 从服务执行docker-compose-slave up -d

#### proxy
1. docker-compose up -d