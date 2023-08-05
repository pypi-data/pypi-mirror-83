# Introduction

Finsights is a package to derive financial insights. It aims to covers the multi-facted areas associated with investment research. This includes getting of data from various sources, preprocessing of data, and analysis-related functions to obtain insights.

## Chapters

1. Data

The `Data` subpackage contains multiple modules used to obtain data. The modules are

- `dapis`: This module contains functions which allow us to obtain data from APIs.
- `events`: This module contains events which happened in financial history. While it only holds some events currently, more events will be added over time so they can be used for scenario analysis.
- `utils`: This module contains helper functions which make obtaining of data easier in general.

2. Analysis

The `Analysis` subpackage contains multiple modules used for analysis. The modules are

- `charting`: This module contains general functions that simplify the charting process, especially the more commonly used ones.
- `modelling`: This module contains functions that simplify the modelling process.
- `preprocessing`: This module contains functions that help in preprocessing. This is usually used before modelling.
- `distributions`: This module contains functions that help us to configure the distribution of a variable.

## Compatibility

This package needs at least Python 3.6 on MacOS.
