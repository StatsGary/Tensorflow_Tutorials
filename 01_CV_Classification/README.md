## Make virtual environment
To make the virtual environment we will need to install the version of Python we want to use. Once we have this - we want to open our CMD prompt or terminal to install the virtualenv package.

```{python}
pip install virtualenv
```

Once we have the virtual environment package we will use the following command to create a new virtual environment:

```
cd <folder_inside_your_project>
virtualenv --python C:\Users\garyh\AppData\Local\Programs\Python\Python39\python.exe venv
```

What this is doing is using the virtualenv command to link to our --python executable stored somewhere on our machine, this will change from distribution to distribution. Finally, we give it a name so we can detect the new virtual environment. 

## Activate the virtual environment

To activate the virtual environment use:

```
.\venv\Scripts\activate
```

## Deactivate the virtual environment

```
deactivate
```

## Export out our install packages in the environment

To export out the packages in our environment we can send them to a requirements.txt file:


```
pip freeze > requirements.txt
```

## Install from our requirements.txt when building a new environment

To install from a requirements.txt use:

```
pip install -r requirements.txt
```