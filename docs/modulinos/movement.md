# Modulino Movement

![Modulino Movement](../assets/modulinos/movement.svg){ .modulino-illustration }

Measure acceleration and rotation with a 6-axis IMU, including a built-in pedometer.

```python
from modulino import ModulinoMovement

movement = ModulinoMovement()
```

## Examples

=== "movement.py"

    ```python
    --8<-- "examples/movement.py"
    ```

=== "movement_pedometer.py"

    ```python
    --8<-- "examples/movement_pedometer.py"
    ```

Run an example with `mpremote connect mount src run examples/<name>.py`.

## API reference

::: modulino.movement.ModulinoMovement
