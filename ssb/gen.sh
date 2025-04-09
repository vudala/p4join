SF=$1

if [ -z "$SF" ]; then
    echo 'No SF provided, using default (0.001)'
    SF=0.001
fi

echo Compiling ssb-dbgen
cd ssb-dbgen
cmake . > /dev/null && cmake --build . > /dev/null

rm -f *.tbl

echo Generating ssb dataset
./dbgen -s $SF 1> /dev/null 2> /dev/null

mv lineorder.tbl ../../datasets/ssb/lineorder.csv
mv customer.tbl ../../datasets/ssb/customer.csv
mv part.tbl ../../datasets/ssb/part.csv
mv supplier.tbl ../../datasets/ssb/supplier.csv
mv date.tbl ../../datasets/ssb/date.csv

echo Done!
