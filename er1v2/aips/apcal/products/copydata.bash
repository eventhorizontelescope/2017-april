rm -f *.uvfits

FILES=`ls ../aips/*/*.uvfits | grep -v tasav | grep -v splat`
for FILE in $FILES
do
  rsync -av $FILE .
done
