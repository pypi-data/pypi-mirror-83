# Conductor Core

Common Python libraries for Conductor Cloud rendering service.

## Install


**To install the latest version.**
```bash
pip install --upgrade ciocore --target=$HOME/Conductor
```

**To install a specific version, for example 0.1.0.**
```bash
pip install --upgrade --force-reinstall ciocore==0.1.0 --target=$HOME/Conductor
```
**Then tell Clarisse how to find the plugin on startup.** 

If you want to use the Python API, set the PYTHONPATH as follows.

```bash
export PYTHONPATH=${HOME}/Conductor
```


## Contributing

For help setting up your dev environment please visit [https://docs.conductortech.com/dev/contributing](https://docs.conductortech.com/dev/contributing)

Pull requests are welcome. For major changes, please [open an issue](https://github.com/AtomicConductor/conductor-core/issues) to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit)