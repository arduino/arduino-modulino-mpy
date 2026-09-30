# Modulino Motors

![Modulino Motors](../assets/modulinos/motors.svg){ .modulino-illustration }

Control DC and stepper motors.

```python
from modulino import ModulinoMotors

motors = ModulinoMotors()
```

## Examples

=== "motors_basic.py"

    ```python
    --8<-- "examples/motors_basic.py"
    ```

=== "motors_frequency.py"

    ```python
    --8<-- "examples/motors_frequency.py"
    ```

=== "motors_stepper.py"

    ```python
    --8<-- "examples/motors_stepper.py"
    ```

=== "motors_telemetry.py"

    ```python
    --8<-- "examples/motors_telemetry.py"
    ```

Run an example with `mpremote connect mount src run examples/<name>.py`.

## API reference

::: modulino.motors.ModulinoMotors

::: modulino.motors.DecayMode
    options:
      show_if_no_docstring: true
