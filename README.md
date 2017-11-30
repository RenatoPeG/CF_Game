# Ingeniería de Software 2 - 801
**Trabajo Ingeniería de Software 2 - Juego en Python**

## Tarea 4
- (Requisito) Seguir los pasos de la Wiki (ver más abajo) antes de continuar
- Las pruebas del desarrollo de la integración se encuentran en la carpeta Documentación/Integración, la url del repositorio es [esta](https://app.codeship.com/cholo-fighter)
- Para ejecutar las pruebas unitarias, estando en la carpeta raiz, ejecutar el comando `python -m unittest UnitTests`

## Wiki

Para ejecutar el juego seguir las siguientes instrucciones:
- En primer lugar asegurese de que se esté ejecutando el servidor
- Instalar pygame con el comando `python -m pip install pygame --user` (Si no resulta, ejecutar `py -m pip install pygame --user`)
- Clonar el repositorio en una carpeta local
- Situarse en la carpeta Vendor y ejecutar el comando `git clone https://github.com/requests/requests.git`
- Situarse en la carpeta Vendor/requests y ejecutar el comando `pip install requests`
- Volver a la carpeta raiz y ejecutar el comando `python CholoFighter.py` (Si no resulta, ejecutar `py CholoFighter.py`)

## Sobre el trabajo

Integrantes:
* Córdova Renato
* Changa Christian
* Marroquín Juan
* Perez Renato
* Rosales Gianfranco

Este trabajo es parte del curso Ingeniería de Software II sección 801, el cual consiste en desarrollar un juego utilizando Python, Pygame y Django entre las principales herramientas. Este proyecto se desarrollará a lo largo del ciclo académico, siendo este proyecto entregado en la última semana (n. 16) del ciclo.

El Product Backlog del trabajo se encuentra [aquí](https://docs.google.com/spreadsheets/d/1vUY-xtefyPXVdKVG4LdZoNn1RjQs8y5NZqC8PksGkvo/edit?usp=sharing).

### Descripción del producto
El juego consiste en peleas por turnos entre dos personajes, los cuales tendrán ciertas características tales como vida, stamina, y objetos utilizables. Los personajes serán en su mayoría personas celebres de la farándula peruana (ex. Melcocha, Peluchin, el Cuto, etc.). El propósito del jugador es poder pasar todos los niveles presentados hasta llegar a un jefe final; un estilo muy parecido a clásicos de la industria como _Tekken_ o _Street Fighter_. El diseño que el juego tendrá es estilo retro ya que es tendencia en estos tiempos. El nombre del juego mientras su desarrollo será **_NOMBRE CLAVE_** el cual será cambiado posteriormente para la salida de la versión final del juego (nombre comercial). El juego presentara dos modalidades: modo historia y modo arcade. El modo historia consistirá en 11 niveles en donde el jugador enfrentará personajes elegidos aleatoriamente, cada nivel siendo más difícil que el anterior. El modo arcade consistirá en peleas con personajes elegidos aleatoriamente hasta que el jugador pierda, cada nivel presentará una dificultad mayor al anterior.

### Necesidad del producto
Este juego tiene la intención de dar al usuario una buena forma de entretenerse sin necesidad de pasar una gran cantidad de horas para poder acabar el juego, a diferencia de la tendencia actual en donde la duración es mayor a las 30 horas. Además, se ofrece una tonalidad cómica y satírica de los sucesos contemporáneos de nuestro país, dándole la oportunidad al usuario de jugar como un político peculiar o como un futbolista sin reparo. Asimismo, hemos optado por elegir un juego de lucha (fighting game) ya que hoy en día no se encuentran muchos en el mercado a excepción de franquicias con juegos AAA. Para poder diferenciar nuestro producto de estos juegos con recepción internacional, le daremos un enfoque no habitual en torno a la estética y diseño artístico del juego respecto a los juegos típicos de este género; tomaremos un enfoque que hoy en día se le conoce como _retro_.

### Clientes potenciales
El público objetivo para este juego son las personas mayores de 20 años de origen peruano, ya que de esta manera podrán disfrutar de todas las referencias hacia nuestra realidad como país. Esto no quiere decir que será exclusivamente para ellos, tenemos en cuenta que algunos de los usuarios jugaran por el hecho de ser un juego de lucha y en cierta manera arcade, lo que no les demandaría muchas horas. El juego es relativamente sencillo respecto a la jugabilidad que deberá aprender el usuario. Tendrá una curva de aprendizaje pequeña en donde todas las mecánicas del juego serán presentadas en un tutorial y no serán progresivas. Es decir, todas las mecánicas disponibles en el juego estarán disponibles para el usuario desde el primer nivel a diferencia de otros juegos en donde las mecánicas se desbloquean dependiendo del avance del jugador dentro de la historia del juego. De esta manera, **_Nombre Clave_** podría ser catalogado como un arcade o juego casual.
Debido a que la mayoría de personas que usarán este juego son jóvenes, se espera que su nivel de sofisticación técnica sea alto, esto hará que se les haga más fácil aprender a jugar. Además, captará más su atención, haciendo que se vuelva popular entre ellos e incrementando así la popularidad del juego. Si bien las personas adultas no son parte del público objetivo, se espera también que, luego de notar que **_Nombre Clave_** resulta ser educativo hasta cierto punto (al enseñarle a los jóvenes un poco de los personajes célebres del Perú) hablen del juego a sus conocidos, haciendo que incremente su popularidad aún más. Aunque no tanto como en los jóvenes, que son los que más le dedican su tiempo a jugar videojuegos. Es por ello que resulta muy conveniente que ellos sean nuestro principal público objetivo.

### Competencia
Actualmente existen pocos juegos que entren bajo la categoría de lucha, los pocos que existen en el mercado son juegos AAA. No se tiene la intención de competir con estas franquicias grandes ya que el público objetivo no es el mismo. Además, hay que tomar en cuenta que este juego se basa en turnos por lo que la mezcla de lucha y turnos no es habitual hoy en día, siendo más difícil encontrar competidores directos. La competencia se reduce aún más cuando nos centramos en el hecho de que los personajes tienen una temática local, por lo que en el mercado peruano la existencia de competidores es casi inexistente o nula.

### Manejo de riesgos
En el desarrollo del videojuego podemos encontrarnos con riesgos en la programación, uno de esos casos sería la falta de conocimientos en el lenguaje de programación a utilizar. ¿Qué se puede hacer para resolverlo? Primero, se buscaría las bases del lenguaje seguido de tutoriales los cuales nos ayudarán a enriquecer más nuestro conocimiento; además, se asistiría a las asesorías del profesor para cualquier consulta.
Otro caso que se puede encontrar sería en el momento de probar el juego puede ocurrir que no funcionen todas las características. ¿Cómo se puede prevenir esto? Se harán pruebas a cada versión nueva del videojuego y revisiones antes de terminar la implementación. ¿Qué se medidas se tomarán si ocurre esto? Se comenzará con la evaluación de todo el juego, partiendo desde lo principal hasta lo más específico revisando los cambios hechos entre las versiones de desarrollo.
Con respecto a temas de ausencia de información o errores en integración de las herramientas utilizadas en el desarrollo, podremos contar con el apoyo de los profesores de la asignatura para la resolución de nuestras dudas en el transcurso del desarrollo del proyecto.

### Requerimientos de recursos
Son de necesidad ciertos recursos para poder construir lo que proponemos. En primer lugar, consideramos como recursos claves el hecho de que los cinco integrantes del equipo aporten con el desarrollo del software. Por lo que, si alguno del equipo no está en la capacidad al cien por ciento de aportar lo que se necesita, este deberá enfocarse y emplear horas a desarrollar las capacidades que sean necesarias para la implementación.
También, necesitaremos cómo recursos las tecnologías en la nube necesarias para montar el generador de configuraciones y, por un deseo del equipo, un Raspberry y Joysticks probar lo que se implemente. Cabe mencionar que estos últimos no se presentan como inconveniente de ser adquiridos ya que un miembro del equipo puede pedir prestado dichos equipos.