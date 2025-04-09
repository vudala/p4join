BENCHMARK=$1
SF=$2

if [[ "$BENCHMARK" != "tpch" && $BENCHMARK != "ssb" ]]; then
    echo 'No valid benchmark selected'
    echo "Usage: ./gen_dataset.sh tcph|ssb [scaling_factor]"
    exit 1
fi

echo Generating dataset for $BENCHMARK benchmark

if [ -z "$SF" ]; then
    echo 'No SF provided, using default (0.001)'
    SF=0.001
else
    echo Using SF $SF
fi

cd $BENCHMARK
./gen.sh $SF

exit 0
