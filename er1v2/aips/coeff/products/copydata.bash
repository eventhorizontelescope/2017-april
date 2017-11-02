rm -f *.fittp *.uvfits

FILES=`ls ../2nd_run/*/*.fittp | grep -v tasav | grep -v splat`
for FILE in $FILES
do
  rsync -av $FILE .
done

FILES=`ls *.fittp`
for FILE in $FILES
do
  FILE2=${FILE:0:9}.coeff.${FILE:13:100}
  FILE3=${FILE2/fittp/uvfits}
  mv $FILE $FILE3
done
