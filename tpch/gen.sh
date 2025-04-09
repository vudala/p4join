SF=$1

if [ -z "$SF" ]; then
    echo 'No SF provided, using default (0.001)'
    SF=0.001
fi

echo Compiling tpch-dbgen
cd tpch-dbgen
cmake . > /dev/null && cmake --build . > /dev/null

rm -f *.tbl

echo Generating tpch dataset
./dbgen -s $SF 1> /dev/null 2> /dev/null

mv customer.tbl ../../datasets/tpch/customer.csv
mv lineitem.tbl ../../datasets/tpch/lineitem.csv
mv nation.tbl ../../datasets/tpch/nation.csv
mv orders.tbl ../../datasets/tpch/orders.csv
mv partsupp.tbl ../../datasets/tpch/partsupp.csv
mv part.tbl ../../datasets/tpch/part.csv
mv region.tbl ../../datasets/tpch/region.csv
mv supplier.tbl ../../datasets/tpch/supplier.csv

echo Done!
