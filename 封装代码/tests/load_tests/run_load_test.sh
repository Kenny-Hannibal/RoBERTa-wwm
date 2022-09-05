img_tag=$1
if [ ! $img_tag ]; then
    echo -e "ERROR!\n        Usage: sh run_load_test.sh <image-tag>\n"
    exit 1
fi

# 1. 通过容器启动server
service_name=api-segment
image_name=api-segment:$img_tag  # 镜像版本需自定义

docker pull $image_name

docker stop ${service_name} && docker rm ${service_name}
docker run -tid --name ${service_name} --memory=2g --cpus=2 -p $port:8000 $image_name  # 运行命令需自定义（cpu mem 显卡）

docker ps | grep ${service_name}


sleep 10  # 等待服务启动
# 2. 压测
report_name=load_test_report.txt
echo "start" > $report_name
for text_len in 200 500 1000 2000  # 文本长度需自定义
do
  echo "text_len = $text_len -----------------------------------------------------------------------" >> $report_name
  python3 gen_request_json.py $text_len
  for concurrency in 1 2 4 6 8 10  # 并发数需自定义
  do
    echo "concurrency = $concurrency ------------" >> $report_name
    siege -c $concurrency -t 1M --content-type "application/json" "http://127.0.0.1:8800/seg POST <request.json" >> $report_name
  done
done


# 3. 清理测试容器
docker stop ${service_name} && docker rm ${service_name}

# 4. 请不断top查看cpu和mem、nvidia-smi查看显存变化情况，评估单个容器最大cpu、最大mem、最大显存，以及确保不存在内存泄漏