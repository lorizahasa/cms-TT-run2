
mgDir=$PWD/genproductions/bin/MadGraph5_aMCatNLO
cardDir=$mgDir/cards/TpTp_production
echo $mgDir

cp top32.tgz $mgDir
cp gridpack_generation_LOCAL_CONDOR.sh $mgDir
cp gridpack_generation.sh $mgDir

mkdir -p $cardDir
cp pairProduction_ttaaChannel.py $cardDir
cp pairProduction_ttgaChannel.py $cardDir
cp pairProduction_ttggChannel.py $cardDir
cd $cardDir
python pairProduction_ttaaChannel.py
python pairProduction_ttgaChannel.py
python pairProduction_ttggChannel.py
ls
cd $mgDir
