# Modulino Light

![Modulino Light](../assets/modulinos/light.svg){ .modulino-illustration }

Read ambient light intensity (lux), color (RGB), color temperature and infrared light.

```python
from modulino import ModulinoLight

light = ModulinoLight()
```

## Examples

=== "light.py"

    ```python
    --8<-- "examples/light.py"
    ```

=== "light_advanced.py"

    ```python
    --8<-- "examples/light_advanced.py"
    ```

Run an example with `mpremote connect mount src run examples/<name>.py`.

## API reference

::: modulino.light.ModulinoLight
