
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
--------------------------  larkinlab  ---------------------------
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

! pip3 install larkinlab

This library contains the functions I have created or come accross that I find myself using often. 

I will be adding functions as I create and find them, so be sure to update to the latest version. Check the CHANGELOG for release info.


~~~~~~~  In The Future  ~~~~~~~

-long description for pypi
-


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-------------------------  Code Descriptions  ------------------------------
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import larkinlab as ll

---------  Subpackages  --------

larkinlab.explore
larkinlab.machinelearning

--------------------------------


=========================  EXPLORE  =============================

to import: 

from larkinlab import explore as llex
import larkinlab.explore as llex

# this subpackage is build for exploring data. Contains functions that help you get an understanding of the data at hand quickly.

-------------------------------------
llex.dframe_ex(df)

The dframe_ex function takes a dataframe and returns a few things
- The number of rows, columns, and total data points
- The names of the columns, limited to the first 60 if more than 60 exist
- Displays up to the first 5 rows of the dataframe via the df.head method
        
Params:
df - pandas DataFrame

-------------------------------------    
llex.vcount_ex(df)

The vcount_ex function returns the value counts and normalized value counts 
for all of columns in the dataframe passed through it.
        
Params:
df - pandas DataFrame

-------------------------------------
llex.scat_ex(df)
        
The scat_ex function returns a scatterplot representing the value counts and 
thier respective occurances for each column in the dataframe passed through it. 

Params:
df - pandas DataFrame

-------------------------------------


-------------------------------------


-------------------------------------


-------------------------------------



=========================  MACHINELEARNING  =============================
    
to import:

from larkinlab import machinelearning as llml
import larkinlab.machinelearning as llml

-------------------------------------


-------------------------------------


-------------------------------------


-------------------------------------



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-------------------------------------------------------------------------------------------------------------------------
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Created By: Conor Larkin

email: conor.larkin16@gmail.com
GitHub: github.com/clarkin16
LinkedIn: linkedin.com/in/clarkin16

Thanks for checking this out!
