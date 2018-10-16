# Installation of packages for text categorization

TEM501 - Text mining course

In this document, I give instruction of how to install
necessary python packages for text categorization.

## Step-by-step of installation

**Install Anaconda**

- Download Anaconda for Python 3 from [https://www.anaconda.com/download](https://www.anaconda.com/download)
- Install Anaconda
- Export Path to Anaconda's python
    + In Linux, you may want to export by adding following line to file `~/.bashrc`
        * `export PATH="<path_to_anaconda3>/bin:$PATH"` (replace <path_to_anaconda3> with the appropriate path)

**Create conda environment**

```
conda create -n tem
```

Then activate the environment. Each time you want to use
the environment, you need to activate that.

```
source activate tem
```

**Install scikit-learn and other packages**

```
conda install scikit-learn ipython jupyter scipy pandas
conda install nltk
```

**Install tensorflow 1.5 and keras 2**

```
pip install tensorflow==1.5.0
pip install -U keras
```

**Test your installation**

Type `python` and then following statements in the
python shell

```
import tensorflow
tensorflow.__version__
import keras
keras.__version__
```

