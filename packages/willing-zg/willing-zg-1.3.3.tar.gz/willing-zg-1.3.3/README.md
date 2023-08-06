# willing_zg

Willing specific plugins for Zygoat

<img src="https://user-images.githubusercontent.com/640862/81694571-7a08eb00-942f-11ea-87f9-c419cb4f8900.jpg" />

## How does it work?

`willing-zg` works by adding additional components for `zygoat` to use when installing or upgrading a repository. These are components that the Willing team wants in every application, but might not be appropriate for every `zygoat` application.

## How do I use it?

Make sure `zygoat` is installed. Then install `willing-zg`:

```bash
pip install --user --upgrade /path/to/willing-zg
```

Go to your application directory and update the `zygoat_settings.yml` file to include the additional components.

```
extras:
    - willing_zg:component_name
    - willing_zg:other_component_name
```

Then run a zygoat update to install the new components.

```bash
zg update
```
