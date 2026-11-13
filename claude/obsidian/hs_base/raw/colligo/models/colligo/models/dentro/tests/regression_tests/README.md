## Regression tests 

This folder contains regression tests for Dentro.

These are tests designed to check that the **output of the model** did not change. They are heavier than integration tests in that they run either a whole tree or an individual model over a variety of inputs and check the outputs for changes. 

A failing regression test indicates that something about the model has changed, whether that be due to a dependency upgrade or a change in the weights. 

This is necessary because in the past we have dealt with changing output of Dentro trees over time without understanding why; these tests should alert us to when significant model changes occur.