cat $1 | grep cv_loss | awk '{print $9}' | sort -r
