#!/bin/bash

function run_query {
    sql_hyper hits.hyper $* 2>&1 | rg execution | sed 's/\(.\+median \)\([0-9]\+\.[0-9]\+\)\(.\+\)/\2/'
}

numcores=`nproc`
for query in q4*.sql; do
    # echo -n $query,0,
    # run_query --parallel=o $query
    # for n in 1 `seq 8 8 $numcores`; do
    for n in 12 20; do
        echo -n $query,$n,
        run_query --parallel=f --soft_concurrent_query_thread_limit=$n $query
    done
done

