# Modulino LED Matrix

![Modulino LED Matrix](../assets/modulinos/led-matrix.svg){ .modulino-illustration }

A 12×8 LED matrix with drawing primitives, text, grayscale mode and animations.

```python
from modulino import ModulinoLEDMatrix

led_matrix = ModulinoLEDMatrix()
```

## Examples

=== "led_matrix.py"

    ```python
    --8<-- "examples/led_matrix.py"
    ```

=== "led_matrix_animation.py"

    ```python
    --8<-- "examples/led_matrix_animation.py"
    ```

=== "led_matrix_fps_animation.py"

    ```python
    --8<-- "examples/led_matrix_fps_animation.py"
    ```

=== "led_matrix_grayscale.py"

    ```python
    --8<-- "examples/led_matrix_grayscale.py"
    ```

=== "led_matrix_mpj_file.py"

    ```python
    --8<-- "examples/led_matrix_mpj_file.py"
    ```

=== "led_matrix_multiple.py"

    ```python
    --8<-- "examples/led_matrix_multiple.py"
    ```

Run an example with `mpremote connect mount src run examples/<name>.py`.

## API reference

::: modulino.led_matrix.ModulinoLEDMatrix

::: modulino.led_matrix.Animation

::: modulino.led_matrix.FPSAnimation

::: modulino.led_matrix.MPJAnimation
