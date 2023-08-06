[![PyPI 
version](https://img.shields.io/badge/pypi%20package-0.0.1-brightgreen)](https://img.shields.io/badge/pypi%20package-0.0.1-brightgreen)
[![Contributions 
welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/Maroussia/isnalyser/blob/master/README.md)
[![GitHub 
license](https://img.shields.io/badge/license-GNU-orange)](https://github.com/Maroussia/isnalyser/blob/master/LICENSE)

# Automated isnād tree visualisations

For scholars studying Ḥadīth texts, drawing an __isnād__ tree with more than 40 transmitters is a tidious work and finding the right medium to desplay it fully can even prove to be impossible. The `isnalyser` is a simple program for the automation of __isnād__ trees drawing and their customable display in handy formats.


  <img src="https://user-images.githubusercontent.com/12030245/95599970-13c1dc00-0a52-11eb-96e9-f9969fdd572f.png" width="350">



## The motivation behind the project

The `isnalyser` aims at facilitating the analysis of large quantity of __aḥādīth__ and more specifically their chains of transmiters or __asānid__ by allowing scholars to visualise these chains of transmitters quickly in a complete graph that includes geo-spatial and chronological information.

## Who is it for?

The `isnalyser` is open-source and publicly available. It is meant for scholars in Ḥadīth studies who are analysing a great number of __aḥādīth__ and need to visualise their chains of transmitters in a single graph. The program can also be used by any scholars in Islamic studies or else who want to visualise the transmission of a text or its recension history. All data that follows the pattern of numerous chains of transmitters/scribes/citations/etc. can serve as input for the present program. 

## How?

Isnalyser can be installed easily and is ready to use within seconds.

### Installation
```bash
pip install isnalyser
```
### Usage
- A nice function of isnalyser is *view_graph*. Let's import it!

```python
from isnalyser import view_graph
```
- Now, if you already **have some data** available that you want to display as an Isnad tree, you can use the function we just imported like so:

```python
view_graph(
	'/path/to/your/data/transmitters.csv', # path to transmitters file
	'/path/to/your/data/transmissions.csv', # path to transmissions file
	15) # step size of timeline
```

- If you **don't have any data yet**, or just want to get a feel for it, we provided some examples. By looking at them, you can also find out how the data needs to be structured for isnalyser to work.

```python
view_graph(
	'', # you can write anyting here, as we don't need it
	'', # same is true here
	15, # 15 is a good step size for the example
	use_example=True) # use example data
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

