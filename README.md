# Developer relationship graph visualization  

## Modules

### Loader 
A module that allows you to upload data using requests to the GitHub API.  

*Short description of the data:*
Files are obtained by converting the json response to a Pandas DataFrame and writing it to csv files. It is important that nested json structures are not processed and are stored as rows in a column.  

*Files:*
* Users - a file containing the 50 most active developers in the repository and information about them; 
* Commits - information about developer commits. Name format {developer_name}_commits.csv;
* Files - information about changes in the files received for each commit from the user. Name format {developer_name}_files.csv.

Dataset loading will remain out of consideration. Instead, a ready dataset will be used below.

----

### Graph vizualization 
The functionality of the module is implemented in the file [graph_visualization.jpynb](https://github.com/MaEgV/developer-relationship-graph/blob/main/graph_visualization.ipynb) in which the technical details are commented and the pipeline structure is marked up.  

*Specific tools:*
* [Networkx](https://networkx.org/documentation/stable/index.html) - to build and proccess graph;
* [Plotly](https://plotly.com/python/network-graphs/) - for interactive graph rendering.

*Research pipeline (according to the code-file):*
1) **Import, helper functions implementation and constants defining**
In this part, the necessary libraries are imported. Functions  that simplify the solution of problems in the lower cells are implemented. Also, here are all the parameters that regulate the operation of the program.  
Description of parameters:
    * ```python min_value_for_edge``` - the lower threshold of the weight value for adding an edge to the drawing. Allows you to filter insignificant links in the graph;
    * ```python weights_params = {'file_coef': ..., 'time_coef': ...}``` - a dictionary with coefficients of a linear combination of features to form a vector of weights;
    * ```python node_size_coef, edge_width_coef``` - sizes of nodes and edges for rendering;
    * ```python first_date``` - repository creation day;
    * ```python last_date``` - data upload day;
    * ```python sigma_num``` - the number of standard deviations from the mean in the interval;
    * ```python users_filename ``` - file that contains information about developers;
    * ```python changes_path ``` - path to files with information about changes in files from each developer;
    * ```python commits_path``` - path to files with information about commits of developers.
2) **Graph creating**
Creating an instance of the Graph class of the Network package and adding nodes for each developer.
3) **Data proccessing**
    3.1) Data reading, parsing and converting in pre-feature condition
    Read commit files and modified files for all users, and prepare information for creating new attributes. The prepared data is a set of files that the developer changed, and a normalized interval of the main activity. Many files are created by simply reading the corresponding. csv file. And the main activity interval is calculated by displaying all the dates of changes in the interval [0,1]. Next, the interval is taken (mean-std * sigma_num, mean + sigma_num *std).  
    
    3.2) Feature creating
    Creating numeric features for edges from the prepared data.
    
    **Feature of the work contexts intersections** calculated as the number of files that were changed by both developers, divided by the sum of the number of occurrences of each file in the contexts of the other developers. The division is necessary to prevent the appearance of links in developers who work in different contexts, but for example, once corrected readme. This way, the popular repository files will lower the link weight.
    
    **Feature of the intersection of activity intervals** is calculated as thesum of modules of differences of corresponding boundaries (|a1-a2|+|b1-b2|). This feature allows you to bring together developers whose activity time is the same. This may correspond to simultaneous recruitment for a project or active development of a feature. On the other hand, if a developer is equally active for the entire lifetime of the repository, then often he will be far from those who were active for a short time. In addition, those who were active for a short time, but at different intervals, will also be far from each other.
    
4) **Adding fetures in graph**
In this part, a linear combination of features is compiled and those that pass the minimum threshold are selected. They are added to the graph with the weight label. Weights are normilized to [0,1] interval.
5) **Graph rendering**
Technical preparation for drawing the graph and visualization itself. It is better to analyze the examples.

----
----

## Examples
As examples, consider several html results of the program with different input parameters, the values of which can be seen on the graphs:

* [Balanced parameters](https://maegv.github.io/developer-relationship-graph/balanced_example)
* [Same coeffs](https://maegv.github.io/developer-relationship-graph/same_coeff)
* [Files impact](https://maegv.github.io/developer-relationship-graph/just_files)
* [Times impact](https://maegv.github.io/developer-relationship-graph/just_time)
* [Low threshold](https://maegv.github.io/developer-relationship-graph/low_threshold)


----
----
