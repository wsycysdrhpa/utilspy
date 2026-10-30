ps -ef | grep run.sh | awk '{print $2}' | xargs kill -9
ps -ef | grep wenet | grep train | awk '{print $2}' | xargs kill -9
