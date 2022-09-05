# 构建测试镜像
sh docker/build_dev.sh
build_status=$?
if [ $build_status -ne 0 ]
then
    echo "build dev image fail!"
    exit 1
fi

# 在测试镜像运行单元测试
container_name=api-segment
image_name=api-segment:dev
echo "run unit test"
docker stop $container_name && docker rm $container_name
docker run --name $container_name $image_name
test_status=$?
docker cp $container_name:/data/app/TestReport.html ../TestReport.html
docker stop $container_name && docker rm $container_name

# 测试成功，push测试镜像；测试失败，退出
if [ ${test_status} -eq 0 ]; then
    echo "unit test success, push dev image"
    docker push $image_name
else
    echo "unit test fail, exit"
    exit 1
fi