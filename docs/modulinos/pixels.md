# Modulino Pixels

![Modulino Pixels](../assets/modulinos/pixels.svg){ .modulino-illustration }

Eight individually addressable RGB LEDs.

```python
from modulino import ModulinoPixels

pixels = ModulinoPixels()
```

## Examples

=== "pixels.py"

    ```python
    --8<-- "examples/pixels.py"
    ```

=== "pixels_thermo.py"

    ```python
    --8<-- "examples/pixels_thermo.py"
    ```

Run an example with `mpremote connect mount src run examples/<name>.py`.

## API reference

::: modulino.pixels.ModulinoPixels

::: modulino.pixels.ModulinoColor
