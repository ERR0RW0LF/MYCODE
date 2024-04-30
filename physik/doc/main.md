# Physik

## Einleitung

Physik ist wird ein Simulationsprogramm um die Einflüsse von Kräften auf Körper zu simulieren und später auch AI in die Simulation zu integrieren als simple Lebensformen.

## Installation

## Benutzung

## Dokumentation

### .sim Dateien

#### Aufbau

Eine .sim Datei besteht aus einer Liste von Körpern und Kräften. Jeder Körper hat eine Masse, eine Position, eine Geschwindigkeit und eine Form. Jede Kraft hat eine Stärke und eine Richtung. Die Datei wird in JSON geschrieben. 

#### Beispiel

```json
{
    "bodies": [
        {
            "mass": 1,
            "position": [0, 0],
            "velocity": [0, 0],
            "shape": "circle"
        },
        {
            "mass": 1,
            "position": [1, 0],
            "velocity": [0, 0],
            "shape": "circle"
        }
    ],
    "forces": [
        {
            "strength": 1,
            "direction": [1, 0]
        }
    ]
}
```

### Simulation

#### Aufbau

Die Simulation besteht aus einem Array der den simulierten Raum darstellt. Jeder Eintrag beschreibt einen Punkt im Raum. Alle Punkte werden in einem 5D Array gespeichert. Die ersten drei Dimensionen sind die Position im Raum, die vierte Dimension beschreibt ein Objekt und seine Eigenschaften und die fünfte Dimension beschreibt die Veränderungen die in einem Zeitschritt passieren. 

Die Simulation soll deterministisch sein, das heißt, dass die Simulation bei gleichen Eingaben immer das gleiche Ergebnis liefern soll.
