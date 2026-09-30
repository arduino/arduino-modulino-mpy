# Modulino Hub

![Modulino Hub](../assets/modulinos/hub.svg){ .modulino-illustration }

An I2C multiplexer that lets you connect multiple Modulinos of the same type on separate ports.

```python
from modulino import ModulinoHub

hub = ModulinoHub()
```

## Examples

=== "hub.py"

    ```python
    --8<-- "examples/hub.py"
    ```

=== "hub_3rd_party.py"

    ```python
    --8<-- "examples/hub_3rd_party.py"
    ```

Run an example with `mpremote connect mount src run examples/<name>.py`.

## API reference

::: modulino.hub.ModulinoHub

::: modulino.hub.ModulinoHubPort
    options:
      show_if_no_docstring: true
