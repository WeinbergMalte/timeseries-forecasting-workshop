# Timeseries Forecasting Workshop
An introduction into time series forecasting basics, challenges, best practices.

## Getting Started &#x2705;
This workshop is designed to be run within [GitHub Codespaces](https://github.com/features/codespaces).

1. Go to the [repository](https://github.com/WeinbergMalte/timeseries-forecasting-workshop)
2. Click on `"Code"` and select `"Codespaces"`
3. Click `"Create codespace on main"`
4. Wait. A new docker image with your own cloud-development environment should is spun up (should be visible in a new browser window). This may take a while.
5. Wait some more. Even after the VS-Code IDE is loaded, it takes some time to install plugins and set everything up. This should be shown in the terminal, but sometimes you'll just have to wait until the clock symbol in the extensions disappears.
6. After the IDE is properly loaded in the browser, check if everything is set up correctly by running `poetry run pytest` in the terminal.
7. Go to the `/notebooks` folder and open the `01-Introduction.ipynb` notebook.
8. Select `.venv` as the Python interpreter in the top right corner.

## Local Setup
Instead of working in Codespaces, you could just as well clone the repository and set up a local development environment. This is how you do it:

1. Clone the repository
2. Have Python installed and install [Poetry](https://python-poetry.org/docs/#installation)
3. Run `poetry install` in the root folder of the repository
4. Run `poetry run pytest` to check if everything is set up correctly

## Resources &#x1F913;

- [Udemy](https://www.udemy.com/): Parts of this workshop is built upon the excellent Udemy course on [Feature Engineering for Time Series Forecasting](https://www.udemy.com/course/feature-engineering-for-time-series-forecasting/). It's an older course but it checks out. Instead of an academic approach it has lots of great hands-on examples and explanations how stuff is actuall done in production.
- [GitHub Codespaces](https://github.com/features/codespaces): Pre-configured dev environments in the cloud!
- [VisualStudio Code](https://vscode.dev) A lightweight and awesome interactive development envrionment. GitHub, VSCode, Copilot... How did we all become Microsoft fanpeople?
- [Jupyter](https://jupyter.org) Sort of an IDE (not really?) that's great for data science analysis and early-stage development. Beware of cell execution order, though.
- [Poetry](https://python-poetry.org): The hands down best dependency management and packaging tool for Python. Yes, dependency management in Python is super messy and annoying. With Poetry it's a bit less messy (but still annoying).
