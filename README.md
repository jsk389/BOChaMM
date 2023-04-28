# BOChaMM
**B**ayesian **O**ptimisation for the **Cha**racterisation of **M**ixed **M**odes.


## Accessing the code and repository

### This branch includes all data for the entire sample. Run the following:
```bash
git clone https://github.com/jsk389/BOChaMM.git --branch main --single-branch
```

### If you do not want to download all data products (i.e., peakbagged modes, samples from BayesOpt), access the alternate branch by running the following:
```bash
git clone https://github.com/jsk389/BOChaMM.git --branch devel --single-branch
```

## Main directories
1. `peakbag/` -- Contains the peakbagged modes for all red giants examined in our study.
2. `notebooks/` -- Contains two notebooks detailing our method of measuring mixed-mode parameters. Visit these to learn how to use our data products and code.
3. `results/images/` -- Contains plots of stretched echelle diagrams of our fits. 
4. `results/samples/` -- Contains samples from the Bayesian optimizer for the forward modelling step. See the notebooks on how to use these.
5. `results/tables/` -- Summary of results from the paper.

## Visualization

The following schematic demonstrates the optimization procedures involved in BoCHaMM. 

<img src="assets/flowchart.png" alt= “” width=380 height=680>


BOChaMM uses the [TuRBO](https://github.com/uber-research/TuRBO) algorithm for optimization, with a quick preview on how it applies to the PSxPS task shown in the following: 

![Turbo turbo turbo wheeeeee.](https://thumbs.gfycat.com/LinedPleasantHypsilophodon-size_restricted.gif)


## To-do-list

- [ ] Binder notebook
- [ ] Package code and make docs
- [ ] Proper import to `sloscillations` repo
- [ ] Git LFS support
- [ ] High-level version of notebooks

## Reference

Paper upcoming and in review!
