# twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
# python setup.py sdist

# Basic
import warnings
warnings.filterwarnings('ignore') # supress warnings

from IPython.display import HTML, display, Markdown, clear_output

import sklearn
from sklearn import preprocessing

import pandas as pd


pd.set_option('display.max_columns', None) # Displaying all the columns in the dataset
pd.set_option('max_colwidth', None) # Displaying entire contents of columns
pd.set_option("max_rows", 100) # Displaying all rows
pd.set_option('max_seq_item', None) # Displaying everything in the list in the dataframe
pd.set_option('precision', 2) # Displaying precision to just 2 decimal places


# Treating Categorical Data

def ohe_prep(main_data, col_ohe, prefx):
    bridge_df = main_data[[col_ohe]]
    # generate binary values using get_dummies
    dum_df = pd.get_dummies(bridge_df, columns=[col_ohe], prefix=[prefx] )
    # merge with main df bridge_df on key values
    del main_data[col_ohe]
    return main_data.join(dum_df)

def ohe(df, col):
  for i in col:
    df = ohe_prep(df,i,i)
  return df

def le():
  return preprocessing.LabelEncoder()

def norm(x_train, x_test):
    min_max_scaler = preprocessing.MinMaxScaler()
    x_train_scaled = min_max_scaler.fit_transform(x_train.values)
    out = []
    out.append(x_train_scaled)
    for i in x_test:
        out.append(min_max_scaler.transform(i.values))
    return out


def read(path, sep, col, row, type):
    return pd.read_table(filepath_or_buffer = path, sep= sep, usecols= col, nrows= row, dtype= type)

def hide_code():
    return HTML('''<script>
            code_show=true; 
            function code_toggle() {
             if (code_show){
             $('div.input').hide();
             } else {
             $('div.input').show();
             }
             code_show = !code_show
            } 
            $( document ).ready(code_toggle);
            </script>
            <form action="javascript:code_toggle()"><input type="submit" value="Click here to toggle on/off the raw code."></form>''')

display(HTML("""
<style>
.output_png img {
    display: block;
    margin-left: auto;
    margin-right: auto;
}
 
.loader {
  border: 5px solid #f3f3f3;
  border-radius: 50%;
  border-top: 5px solid teal;
  border-right: 5px solid grey;
  border-bottom: 5px solid maroon;
  border-left: 5px solid tan;
  width: 20px;
  height: 20px;
  -webkit-animation: spin 1s linear infinite;
  animation: spin 1s linear infinite;
  float: left;`
}

@-webkit-keyframes spin {
  0% { -webkit-transform: rotate(0deg); }
  100% { -webkit-transform: rotate(360deg); }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

</style>
"""))

def load_icon():
    return display(Markdown('<div><div class="loader"></div><h3>&nbsp;LOADING</h3></div>'))
