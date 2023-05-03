# BOChaMM
**B**ayesian **O**ptimisation for the **Cha**racterisation of **M**ixed **M**odes.


## Accessing the repository and code
Execute the following to your base directory of choice:

```bash
git clone https://github.com/jsk389/BOChaMM.git
```

## Main directories
1. `peakbag/` -- Contains the peakbagged modes for all red giants examined in our study.
2. `notebooks/` -- Contains two notebooks detailing our method of measuring mixed-mode parameters. Visit these to learn how to use our data products and code.
3. `results/images/` -- Contains plots of stretched echelle diagrams of our fits. 
4. `results/samples/` -- Contains samples from the Bayesian optimizer for the forward modelling step. See the notebooks on how to use these.
5. `results/tables/` -- Summary of results from the paper.


### Due to the large volume of the data products (peakbagged modes, BayesOpt samples, etc.), we have migrated the full dataset to Zenodo, with a few examples in the existing repo folders. Get the full data [here](https://zenodo.org/record/7888633).

## Visualization

The following schematic demonstrates the optimization procedures involved in BoCHaMM. 

<img src="assets/flowchart.png" alt= “” width=380 height=680>


BOChaMM uses the [TuRBO](https://github.com/uber-research/TuRBO) algorithm for optimization, with a quick preview on how it applies to the PSxPS task shown in the following: 

![Turbo turbo turbo wheeeeee.](https://thumbs.gfycat.com/LinedPleasantHypsilophodon-size_restricted.gif)


## To-do-list

- [ ] High-level version of notebooks
- [ ] Notebook for producing plots in paper
- [ ] Proper import to `sloscillations` repo
- [ ] Package code and make docs
- [ ] Binder notebooks

## Reference

Paper upcoming and in review!
