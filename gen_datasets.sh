echo Compiling ssb-dbgen
cd ssb-dbgen
cmake . > /dev/null && cmake --build . > /dev/null

rm -f *.tbl

SF=$1

echo Generating datasets
if [ -z "$SF" ]; then
    echo 'No SF provided, using default (0.001)'
    SF=0.001
else
    echo Using SF $SF
fi

./dbgen -s $SF 1> /dev/null 2> /dev/null

mv lineorder.tbl ../datasets/lineorder.csv
mv customer.tbl ../datasets/customers.csv
mv part.tbl ../datasets/part.csv
mv supplier.tbl ../datasets/supplier.csv
mv date.tbl ../datasets/date.csv

echo Done!
