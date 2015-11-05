
# Lab Outline

Tasks and things to do, to write, etc.

To add to it, use [Markdown](http://www.facebook.com/l.php?u=http%3A%2F%2Fmarkdowntutorial.com%2F&h=8AQGIPO_0). To write down equations, use dollar signs, and $\LaTeX$ syntax. You can use Python in code blocks.

## Goals

From the manual:
> - Measure the resistivity of germanium as a function of temperature and deduce conclusions regarding the conduction mechanism;
> - Measure the dependence of the Hall voltage across the sample on temperature;
> - Measure the magneto-resistance of the sample as a function of the magnetic field intensity;
> - **(optional)** Be creative! You may for instance study the dependence of the magneto-resistance effect on the orientation of the sample, study the heating rate of the sample, or do whatever else that may come to mind.

I propose that the optional part be spent on measuring the heating rate of the sample, as it brings together the temperature and magnetism aspect of the experiment. Still two weeks to think about, though. No worries.

## Theory behind the Hall effect

- See `References` for a nice [Youtube tutorial](https://www.facebook.com/l.php?u=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DfZoFnKo-bwk&h=8AQGIPO_0) (thanks Nico!)

### What we should get

- **All** of the equations we will use later in the lab, numbered
- Clear diagrams of the physics

### Equations from the manual

Each item in the list is for what I think should be one block for an equation in the final report. If it makes it.

<small>(To remove things, use double tildes like so: ~~removed~~. To add them, just append them in the place where they'd be most useful.)</small>

1. $ R = \frac{\rho L}{S} $ where $R$ is the *electrical resistance* for a material of length *L*, cross sectional area *S* and *resistivity* $\rho$. $\rho$ is dependant on temperature for a given material.
2. $\rho = \sigma^{-1}$ and $\vec{J}=\sigma\vec{E}$, where $\sigma$ is the conductivity, $\vec{J}$ is the vectorial current density and $\vec{E}$ is the electric field. For electrons (negative charge carriers) we have $\vec{J}=e^-n\vec{v}$ where $\vec{v}$ is the mean velocity of electrons and $n$ their density in the material.
3. 

## Apparatus

### What we should get

- A list and description of the equipment
- A schematic of the experimental setup **Émile**
- A diagram of how the information is processed (not just *computer*) **Émile**
- Precisions on which steps are delicate for specific things

### Constant Current Power Supply

### Variable DC Power Supply

### Thermocouple System (with cold-junction compensator)

### Magnet

### Magnetic Field Measurements with the Hall probe

### Keithley Digital Voltmeter

### Software

See Appendix C from the manual, and the page on [Hall programs](http://www.ugrad.physics.mcgill.ca/wiki/index.php/Software:Hall_Effect) on the wiki. There's also `Manual/hall-effect-guide.pdf` by Mark that explains a lot about the software.

#### `hall` program for data acquisition

#### `hall_process` program for preparing data for plotting

#### Data manipulation programs

- `hall_add`
- `hall_subtract`
- `hall_product`
- `hall_quotient`

#### Analysis software that we use

These should all be in the `Programs/` folder of the Git repository. We'll use `spinmob` as the main module for the analysis.

### Block diagram for the magnets and stuff

See Fig. 3 from the manual. I'll reproduce it in OmniGraffle or with LaTeX, and include the electronics.

I'll also produce a software diagram, so that we can easily show how we did the analysis. This can only be done at the end, though.

We'll also need a diagram like Fig. 4 from the manual for the sample holder.

### Delicate steps and things

- Do *not* exceed a *sample* temperature of $383\,\mathrm{K}$ (110°C)
- Be careful with the sample when it is very cold or close to $383\,\mathrm{K}$
- The sample and its wiring are *very* fragile
- Turn off the power sources when we leave, unless we're takign data
- Make sure cooling water is running when using the magnet
- Make sure the cold-junction compensator is switched **on** when used and **off** when unused

## Measurement of the sample's relevant dimensions

### What we should get

- A table of the sample dimensions
- Labels of the dimensions on the diagram of the sample holder

### Actual measurement

Apparently, we will **not** be measuring the sample ourselves, instead using pictures taken by Dominic or Mark. The sample is too fragile to be manipulated by our impure hands ;P We also **don't** need the dimensions for most of the experiment. To paraphrase Dominic: the dimensions of the sample are only useful to get the resistivity, carrier density or charge. We rarely need those, so whenever we can, we should use the **resistance** instead of the resistivity, to reduce our uncertainties in the other sections of the experiment. I'll check, but this may mean that we can **completely scrap this part of the experiment**.

## ~~Resistivity~~ _Resistance_ as a function of temperature

### What we should get out

- A graph
- A fit, with uncertainties and chi-square

## Hall coefficient as a function of temperature

### What we should get out

- A graph
- A fit, with uncertainties and chi-square

## Magneto-resistance against magnetic field intensity

### What we should get out

- A graph
- A fit with uncertainties and chi-square


    
