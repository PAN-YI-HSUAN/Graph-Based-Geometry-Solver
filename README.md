# Graph-Based-Geometry-Solver
```
├── Graph-Based-Geometry-Solver
│   ├── Graph2Tree
│   │   ├── math23k
│   │   ├── README.md
│   │   └── requirement.txt
│   ├── Graph2Tree_on_our_data
│   │   ├── __pycache__
│   │   ├── data
│   │   ├── GCN.py
│   │   ├── graph.py
│   │   ├── GraphConvolution.py
│   │   ├── model_traintest
│   │   ├── out
│   │   ├── prev_out.txt
│   │   ├── readme
│   │   ├── run_seq2tree_graph.py
│   │   ├── run_seq2tree_train.py
│   │   ├── run_seq2tree.py
│   │   └── src
│   └── Data_processing
│       ├── data
│       ├── geometry_mwps_filter.py
│       ├── parse_for_sentence.py
│       └── problem_type_analysis.ipynb
└──
```
## Graph2Tree
This model is from [https://github.com/2003pro/Graph2Tree](https://) by the authors Zhang, Jipeng and Wang, Lei and Lee, Roy Ka-Wei and Bin, Yi and Shao, Jie and Lim, Ee-Peng. We mainly run the run_seq2tree_graph.py to test their module.

## Graph2Tree_on_our_data
In this folder, there are our processed data including geometry_mwps.json and Math23K_geometry.json. In run_seq2tree_graph.py, we load geometry math word problems to train and test this graph2tree model. And there are consequences of experiments in 'out' directory.

## Data_processing
This folder includs all we need code to make our data feasible on graph2tee model. Aiming to focus on geometric math word problems, geometry_mwps_filter.py can load Math_23K dataset and filter out the problems about geometry. The code parse_for_sentence.py can be used to get the relevant word about cardinal numbers from any  chinese contexts, and the method is using stanford corenlp toolkit to parsing the POS of each sentence. According to the technique report, we analize the problems in Math_23K by problem_type_analysis.ipynb.
