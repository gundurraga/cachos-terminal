# cachos-terminal

Terminal-Cachos: Juego de dados tradicional chileno implementado en Python para jugar en la terminal contra oponentes IA.

# Reglas del Juego de Cachos

## Objetivo

Evitar perder todos los dados y ser el último jugador con dados en la mesa.

## Preparación

- **Número de jugadores:** 2 o más
- **Materiales:** Cada jugador recibe 5 dados y un cacho.
- **Dados en juego:** El total inicial de dados en juego es el número de jugadores multiplicado por 5.

## Nomenclatura de las pintas

- **1:** As
- **2:** Tonto
- **3:** Tren
- **4:** Cuadra
- **5:** Quina
- **6:** Sexta

## Inicio del juego

1. Cada jugador tira un dado.
2. El jugador que saca la pinta mayor comienza (el as es el número menor).
3. En caso de empate, se repite la tirada hasta desempatar.

## Dinámica del juego

- Se juega por rondas.
- La primera ronda la inicia quien sacó la pinta mayor.
- Las siguientes rondas las inicia quien perdió o recuperó un dado en la ronda anterior.
- El juego termina cuando solo queda un jugador con dados.

## Desarrollo de una ronda

1. Los jugadores agitan y tiran sus dados sin mostrarlos.
2. Si un dado queda montado, se anuncia y se vuelve a tirar.
3. El jugador inicial hace una apuesta sobre el número de veces que se repite una pinta en el total de dados.
4. Si se inicia con ases, es partida falsa y el siguiente jugador juega libremente.
5. El sentido del juego lo determina el jugador inicial.

## Opciones de juego

### Subir

- Aumentar el número o el valor de la pinta.
- De ases a otra pinta: doble más uno (Ej: 2 ases -> 5 cuadras).

### Bajar

- Solo se puede bajar a ases.
- Se dice la mitad de la cantidad redondeada hacia arriba.

### Dudar

- Todos muestran sus dados y se cuentan.
- Si hay igual o mayor cantidad de la pinta apostada, pierde quien dudó.
- Si hay menos, pierde quien fue dudado.

### Calzar

- Solo si quedan la mitad o más dados en juego.
- Si hay exactamente la cantidad apostada, quien calzó recupera un dado.
- Si no, quien calzó pierde un dado.

### Pasar

- La apuesta se transfiere al siguiente jugador.
- Válido con 5 dados y una de estas condiciones:
  - a) Todos los dados diferentes.
  - b) Todos los dados iguales.
  - c) Full house (3 de una pinta + 2 de otra).
- Solo se puede pasar una vez por ronda.
- Si es dudado y no es válido, pierde quien pasó.

## Reglas especiales

- **Ases como comodines:** Los ases son comodines (excepto en el pase y en Modo Obligo).
- **Modo Obligo:** Cuando un jugador queda con 1 dado.
  - Dura una ronda.
  - Solo se puede subir o dudar.
  - No se cambia la pinta ni se baja a ases.
  - **Tipos de Obligo:**
    - a) **Obligo cerrado:** Solo ven sus dados quien obliga y los que tienen 1 dado.
    - b) **Obligo abierto:** Todos los jugadores ven los dados de los demás, pero no los suyos propios.
  - Se puede obligar solo una vez por juego.

### Modalidad 1 vs 1

- Cuando quedan dos jugadores:
  - No se puede calzar, pasar ni obligar.

## Reglas adicionales

- **La Siciliana:** Dudar una apuesta inicial muy alta.

  - El perdedor pierde dos dados.
  - Los ases no cuentan como comodín.
  - No válida si algún jugador tiene solo un dado.

- **Partida Falsa:** Cuando se inicia con ases.
  - Deshabilita esos ases para esa ronda.
