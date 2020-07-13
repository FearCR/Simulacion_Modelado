# Queuing Network Simulation (espanol):

## Modelo a simular:  
  
En una empresa que fabrica mascarillas para prevenir infectar e infectarse del Covid-19, hay 2
diferentes secciones: la 1 y 2. La 1 sección 1 recibe las mascarillas ya confeccionadas una a
una para desinfectarse también una a una. Ya desinfectadas se envían también una a una a la
sección 2 en donde se preparan paquetes con 2 mascarillas, para ser luego repartidas en
diferentes lugares del país.  
  
En la sección 1 hay un encargado, ahí el tiempo entre arribos de las mascarillas sigue una
distribución D1, el tiempo que tarda este encargado desinfectando cada mascarilla sigue una
distribución D2, para luego enviarla a la sección 2 tardando 1 minuto en llegar, siempre y
cuando no la destruya, lo cual ocurre el 10% de las veces.  
  
En la sección 2 hay dos encargados cada uno preparando paquetes de dos mascarillas,
ninguno comienza a preparar un paquete, mientras aún no tenga dos mascarillas. El encargado 1
tarda un tiempo con distribución D3 preparando un paquete, pero el encargado 2 tarda un
tiempo con distribución D4. Una vez gastado este tiempo, puede ocurrir que el paquete deba
botarse, porque hubo errores de empaque, lo cual ocurre el 5% de las veces para el encargado
1, pero 15% de las veces para el encargado 2, y otras en las que el encargado decide que se
deben desinfectar de nuevo, por lo que envía las 2 mascarillas a las sección, esto pasa el
20% de las veces con el encargado 1 y el 25% de las veces con el encargado 2, el restante
porcentaje se da por listo. Las 2 mascarillas tardan 2 minutos en llegar a la sección 1, tanto
cuando las envía el encargado 1 como cuando lo hace el encargado 2.
