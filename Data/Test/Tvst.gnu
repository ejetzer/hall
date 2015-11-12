set nologscale
set xlabel "Time (minutes)"
set ylabel "Temperature (K)"
plot "<awk '{print $1/60,$2}' test.data.8" title ' ' with dots

