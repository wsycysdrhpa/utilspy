exp_dir=$1

cd $exp_dir
mkdir tmp
readlink -f final.pt | xargs -i mv {} tmp/
mv final.pt tmp/
mv pre_training.pt tmp/
mv global_cmvn tmp/
mv *.log tmp/
mv train.yaml tmp/

ls | grep ".pt" | xargs -i rm {}
ls | grep ".yaml" | xargs -i rm {}
rm ddp_init
rm init.zip

mv tmp/* .
rm -rf tmp

cd -
