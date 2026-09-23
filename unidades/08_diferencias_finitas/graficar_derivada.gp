# Grafica en escala log-log los errores de las diferencias finitas.
# Primero corre: py diferencias_finitas.py
# Después corre: gnuplot graficar_derivada.gp

archivo = "datos/derivada_sin_x2.dat"
EPS = 2.220446049250313e-16
h_opt_adelante = sqrt(4.0 * EPS)
h_opt_central = (24.0 * EPS)**(1.0 / 3.0)

set title "Error de diferencias finitas vs. tamano de paso h"
set xlabel "h"
set ylabel "error relativo"
set logscale xy
set format x "10^{%L}"
set format y "10^{%L}"
set grid
set key top left

set arrow from h_opt_adelante, graph 0 to h_opt_adelante, graph 1 nohead lc rgb "red" dt 2
set arrow from h_opt_central, graph 0 to h_opt_central, graph 1 nohead lc rgb "blue" dt 2

plot archivo using 1:3 with linespoints lc rgb "red" pt 7 ps 0.5 title "adelante, O(h)", \
     archivo using 1:5 with linespoints lc rgb "blue" pt 7 ps 0.5 title "central, O(h^2)"

pause -1 "Presiona Enter para cerrar..."
