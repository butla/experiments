# Notes

- briefcase can be installed with pipx
- briefcase needs some dependencies on Linux for `briefcase dev` to work:
  https://docs.beeware.org/en/latest/tutorial/tutorial-0.html#install-dependencies
- running in virtualenv is only possible, if it's using the same version as the system Python,
  because Toga links system's GTK Python bindings into the virtualenv
- run `pip install --pre toga-gtk` in the virtualenv to run the samples

