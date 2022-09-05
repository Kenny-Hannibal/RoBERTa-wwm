img_tag=$1

# 用新镜像启动服务
container_name=api-segment
image_name=api-segment:$img_tag
docker stop $container_name && docker rm $container_name
docker run --name $container_name -d $image_name
docker ps | grep $container_name

# 在容器内进行api测试
sleep 60 # 等待服务启动
docker exec $container_name bash -c "cd /data/app && python -u tests/api_tests/test_api.py"

# 如果api测试通过，push镜像；否则，打印server日志
test_status=$?
if [ $test_status -eq 0 ]; then
    echo "api test success, push image"
    docker push $image_name
    docker stop $container_name && docker rm $container_name
else
    echo "api test fail, show logs"
    docker logs $container_name --tail 100
    docker stop $container_name && docker rm $container_name
    exit 1
fi
