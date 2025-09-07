# Manimations
A variety of mathematical animations using Manim

## Set Up

I followed the conda instructions from the [Manim Community Documentation](https://docs.manim.community/en/stable/installation/conda.html)

```
conda create manim
conda activate manim
conda install -c conda-forge manim
```

I also have any additional dependencies in a `requirements.txt` in each folder
```
pip install -r requirements.txt
```

## Run

Command to run when developing
```
manim -pql file_name.py ClassName
```

Command to render final animation
```
manim -pqh file_name.py ClassName --fps 60
```